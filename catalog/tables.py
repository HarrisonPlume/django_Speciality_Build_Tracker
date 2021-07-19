# tutorial/tables.py
import django_tables2 as tables
from .models import Part

class PartTable(tables.Table):
    class Meta:
        model = Part
        template_name = "django_tables2/bootstrap.html"
        fields = ("title","serial","team","Component_Prep_tasks",
                  "Stacking_tasks","Forming_tasks","Header_Plate_tasks",
                  "Pitching_tasks","Wire_Cut_tasks","Deburr_tasks",
                  "Plating_tasks")