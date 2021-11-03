import datetime
from .models import Part, Component_Prep_Task, Team, Stacking_Task, Forming_Task, Header_Plate_Task, Pitching_Task, Wire_Cut_Task, Deburr_Task, Plating_Task
from django import forms
from django.core.exceptions import ValidationError



class PartForm(forms.ModelForm):
    title = forms.CharField(max_length=15, label="Part Number")
    serial = forms.CharField(max_length=20,label="Serials To Create")
    core_type = forms.ChoiceField(label="Core Type", choices = (("Radiator", "Radiator"), ("Intercooler", "Intercooler"),
                  ("Oilcooler", "Oilcooler"),("ERS cooler", "ERS cooler")))
    Work_Order = forms.CharField(max_length = 20, label= "Work Order")
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label = "Team")
    Component_Prep_tasks = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
                                                          queryset=Component_Prep_Task.objects.all(),
                                                          label = "Component Prep Tasks",
                                                          required = True)
    Stacking_tasks = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
                                                          queryset=Stacking_Task.objects.all(),
                                                          label = "Stacking Tasks",
                                                          required = True)
    Forming_tasks = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
                                                          queryset=Forming_Task.objects.all(),
                                                          label = "Header Plate Forming Tasks",
                                                          required = True)
    Header_Plate_tasks = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
                                                          queryset=Header_Plate_Task.objects.all(),
                                                          label = "Header Plate Machining Tasks",
                                                          required = True)
    Pitching_tasks = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
                                                          queryset=Pitching_Task.objects.all(),
                                                          label = "Pitching Tasks",
                                                          required = True)
    Wire_Cut_tasks = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
                                                          queryset=Wire_Cut_Task.objects.all(),
                                                          label = "Wire Cut Tasks",
                                                          required = True)
    Deburr_tasks = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
                                                          queryset=Deburr_Task.objects.all(),
                                                          label = "Deburring Tasks",
                                                          required = True)
    Plating_tasks = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,
                                                          queryset=Plating_Task.objects.all(),
                                                          label = "Plating Tasks",
                                                          required = True)
    
    class Meta:
        model = Part
        fields = ("title","serial","core_type","Work_Order","team","Component_Prep_tasks",
                  "Stacking_tasks", "Forming_tasks", "Header_Plate_tasks",
                  "Pitching_tasks", "Wire_Cut_tasks", "Deburr_tasks",
                  "Plating_tasks")
        
class ArchiveForm(forms.ModelForm):
    archive = forms.BooleanField(required = True,
                                 label = "Confirm Core is complete")
    
    class Meta:
        model = Part
        fields = ("archive",)