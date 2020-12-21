from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from core.models import User, Variable, RangeVariableType, ChoiceVariableType, ChoiceVariableChoice, VariableInstance, \
    Report, RangeVariableTypeResponse, ChoiceVariableTypeResponse


class JWTSerializer(serializers.Serializer):
    access = serializers.CharField(source='access_token')
    refresh = serializers.CharField(source='refresh_token')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_doctor', 'is_patient']


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def handle_save(self, user):
        user.save()

    def save(self):
        user = User(email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user.set_password(password)
        self.handle_save(user)
        return user


class RangeVariableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RangeVariableType
        fields = '__all__'
        read_only_fields = ['variable']


class ChoiceVariableChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ChoiceVariableChoice
        fields = '__all__'
        read_only_fields = ['choice_type']


class ChoiceVariableTypeSerializer(serializers.ModelSerializer):
    choices = ChoiceVariableChoiceSerializer(many=True)

    class Meta:
        model = ChoiceVariableType
        fields = '__all__'
        read_only_fields = ['variable']


class VariableSerializer(serializers.ModelSerializer):
    range = RangeVariableTypeSerializer(source='get_range', allow_null=True)
    choice = ChoiceVariableTypeSerializer(source='get_choice', allow_null=True)
    used_by = serializers.PrimaryKeyRelatedField(source='get_used_by', many=True, read_only=True)

    class Meta:
        model = Variable
        fields = '__all__'
        read_only_fields = ['doctor']

    def to_representation(self, instance):
        types = ['range', 'choice']
        key = 'type'
        representation = super().to_representation(instance)
        # get first variable type which isnt none and put it into the type field for easy displaying
        for t in types:
            if representation[t] is not None:
                representation[key] = t
                break
        return representation

    def validate(self, attrs):
        range_data = attrs.get('get_range')
        choice_data = attrs.get('get_choice')
        if range_data is None and choice_data is None:
            raise serializers.ValidationError("Must supply either a range or choice type")
        if range_data is not None and choice_data is not None:
            raise serializers.ValidationError("Can't supply both a range and choice type")
        if choice_data is not None and len(choice_data.get('choices', [])) is 0:
            raise serializers.ValidationError("Must supply at least one choice")
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['doctor'] = self.context['request'].user.doctor
        range_data = validated_data.pop('get_range')
        choice_data = validated_data.pop('get_choice')
        variable = super().create(validated_data)
        if range_data is not None:
            range_type = RangeVariableType.objects.create(**range_data, variable=variable)
        if choice_data is not None:
            choices = choice_data.pop('choices')
            choice_type = ChoiceVariableType.objects.create(**choice_data, variable=variable)
            for choice in choices:
                choice = ChoiceVariableChoice.objects.create(**choice, choice_type=choice_type)
        return variable

    def update(self, instance, validated_data):
        range_data = validated_data.pop('get_range')
        choice_data = validated_data.pop('get_choice')
        variable = super().update(instance, validated_data)
        if range_data is not None:
            range_var = instance.rangevariabletype
            range_var.min_value = range_data.pop('min_value')
            range_var.max_value = range_data.pop('max_value')
            range_var.save()
        if choice_data is not None:
            choice_var = instance.choicevariabletype
            choices = choice_data.pop('choices')
            choice_mapping = {choice.id: choice for choice in choice_var.choices.all()}
            for choice in choices:
                choice_id = choice.get('id', None)
                if choice_id is None:
                    ChoiceVariableChoice.objects.create(choice_type=choice_var, **choice)
                else:
                    c = choice_mapping.get(choice_id, None)
                    c.value = choice.pop('value', None)
                    c.save()
            for choice_id, choice in choice_mapping.items():
                if choice_id not in [c.get('id', None) for c in choices]:
                    choice.delete()
        return variable


class VariableInstanceSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = VariableInstance
        fields = '__all__'
        expandable_fields = {
            'variable': VariableSerializer
        }


class RangeVariableTypeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RangeVariableTypeResponse
        fields = '__all__'
        read_only_fields = ['report']

    def validate(self, attrs):
        variable = attrs['variable']
        try:
            range_type = RangeVariableType.objects.get(variable=variable)
        except RangeVariableType.DoesNotExist:
            raise serializers.ValidationError("Can only submit a range response for a range variable")
        response = attrs['response']
        if response < range_type.min_value or response > range_type.max_value:
            raise serializers.ValidationError("Response out of range")
        return attrs


class ChoiceVariableTypeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceVariableTypeResponse
        fields = '__all__'
        read_only_fields = ['report']

    def validate(self, attrs):
        variable = attrs['variable']
        try:
            choice_type = ChoiceVariableType.objects.get(variable=variable)
        except ChoiceVariableType.DoesNotExist:
            raise serializers.ValidationError("Can only submit a choice response for a choice variable")

        response = attrs['response']
        if response.choice_type != choice_type:
            raise serializers.ValidationError("Invalid response & variable combination")
        return attrs


class ReportSerializer(serializers.ModelSerializer):
    range_responses = RangeVariableTypeResponseSerializer(many=True, source='get_range_responses', required=False)
    choice_responses = ChoiceVariableTypeResponseSerializer(many=True, source='get_choice_responses', required=False)

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['patient']

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user.patient
        range_responses = validated_data.pop('get_range_responses', [])
        choice_responses = validated_data.pop('get_choice_responses', [])
        report = super().create(validated_data)

        for range_response in range_responses:
            RangeVariableTypeResponse.objects.create(report=report, **range_response)

        for choice_response in choice_responses:
            ChoiceVariableTypeResponse.objects.create(report=report, **choice_response)

        return report
