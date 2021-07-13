from django.contrib import admin
from .models import Component_Prep_Task, ComponentPrepTaskInstance, Part, Team, Stacking_Task, StackingTaskInstance, Forming_Task, FormingTaskInstance, Header_Plate_Task, HeaderPlateTaskInstance
# Register your models here.

class ComponentPrepTaskAdmin(admin.ModelAdmin):
    list_display = ("task","part","status")

admin.site.register(ComponentPrepTaskInstance, ComponentPrepTaskAdmin)
admin.site.register(Component_Prep_Task)
admin.site.register(Stacking_Task)
admin.site.register(StackingTaskInstance)
admin.site.register(Forming_Task)
admin.site.register(FormingTaskInstance)
admin.site.register(Header_Plate_Task)
admin.site.register(HeaderPlateTaskInstance)
admin.site.register(Part)
admin.site.register(Team)