from django.contrib import admin
from .models import Component_Prep_Task, ComponentPrepTaskInstance, Part, Team, Stacking_Task, StackingTaskInstance, Sheet_Metal_Forming_Task, Sheet_Metal_Forming_Task_Instance
# Register your models here.

class ComponentPrepTaskAdmin(admin.ModelAdmin):
    list_display = ("task","part","status")

admin.site.register(ComponentPrepTaskInstance, ComponentPrepTaskAdmin)
admin.site.register(Component_Prep_Task)
admin.site.register(Stacking_Task)
admin.site.register(StackingTaskInstance)
admin.site.register(Sheet_Metal_Forming_Task)
admin.site.register(Sheet_Metal_Forming_Task_Instance)
admin.site.register(StackingTaskInstance)
admin.site.register(Part)
admin.site.register(Team)