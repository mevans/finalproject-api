from rest_framework import serializers

from core.models import User, Variable, RangeVariableType, ChoiceVariableType, ChoiceVariableChoice


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
