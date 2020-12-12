from django.contrib import admin

# Register your models here.
from core.models import User, Patient, Doctor, Report, Variable, RangeVariableType, RangeVariableTypeResponse

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)

admin.site.register(Report)
admin.site.register(Variable)

admin.site.register(RangeVariableType)
admin.site.register(RangeVariableTypeResponse)
