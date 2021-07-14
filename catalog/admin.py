from django.contrib import admin
from .models import Component_Prep_Task, ComponentPrepTaskInstance, Part, Team, Stacking_Task, StackingTaskInstance, Forming_Task, FormingTaskInstance, Header_Plate_Task, HeaderPlateTaskInstance, Pitching_Task, PitchingTaskInstance, Wire_Cut_Task, WireCutTaskInstance, Deburr_Task, DeburrTaskInstance, Plating_Task, PlatingTaskInstance
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
admin.site.register(Pitching_Task)
admin.site.register(PitchingTaskInstance)
admin.site.register(Wire_Cut_Task)
admin.site.register(WireCutTaskInstance)
admin.site.register(Deburr_Task)
admin.site.register(DeburrTaskInstance)
admin.site.register(Plating_Task)
admin.site.register(PlatingTaskInstance)