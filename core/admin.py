from django.contrib import admin

# Register your models here.
from core.models import User, Patient, Doctor, Report, Variable, RangeVariableType, RangeVariableTypeResponse, \
    VariableInstance, ChoiceVariableType, ChoiceVariableTypeResponse, ChoiceVariableChoice

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)

admin.site.register(Report)
admin.site.register(Variable)
admin.site.register(VariableInstance)

admin.site.register(RangeVariableType)
admin.site.register(RangeVariableTypeResponse)

admin.site.register(ChoiceVariableType)
admin.site.register(ChoiceVariableChoice)
admin.site.register(ChoiceVariableTypeResponse)
