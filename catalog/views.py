from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import ComponentPrepTaskInstance, Part, StackingTaskInstance, FormingTaskInstance, HeaderPlateTaskInstance, PitchingTaskInstance, WireCutTaskInstance, DeburrTaskInstance, PlatingTaskInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.template.defaulttags import register
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import PartTable
from catalog.forms import PartForm, ArchiveForm
from django import forms
from django.utils import timezone
import datetime, time

def index(request):
    """View for the home page of the website"""
    
    #Generate counts for soe of the main objetcs
    num_CpTasks = ComponentPrepTaskInstance.objects.exclude(status__exact="z").count()
    num_Forming_Tasks = FormingTaskInstance.objects.exclude(status__exact="z").count()
    num_Stacking_Tasks = StackingTaskInstance.objects.exclude(status__exact="z").count()
    num_Wire_Cut_Tasks = WireCutTaskInstance.objects.exclude(status__exact="z").count()
    num_Pitching_Tasks = PitchingTaskInstance.objects.exclude(status__exact="z").count()
    num_HP_Tasks = HeaderPlateTaskInstance.objects.exclude(status__exact="z").count()
    num_Deburr_Tasks = DeburrTaskInstance.objects.exclude(status__exact="z").count()
    num_Plating_Tasks = PlatingTaskInstance.objects.exclude(status__exact ="z").count()
    num_parts = Part.objects.filter(archive__exact = False).count()
    
    #Number of site visits by the current user    
    context = {
        "num_CpTasks": num_CpTasks,
        "num_parts": num_parts,  
        "num_Stacking_Tasks": num_Stacking_Tasks,
        "num_Forming_Tasks": num_Forming_Tasks,
        "num_Wire_Cut_Tasks": num_Wire_Cut_Tasks,
        "num_Pitching_Tasks" : num_Pitching_Tasks,
        "num_HP_Tasks" : num_HP_Tasks,
        "num_Deburr_Tasks" : num_Deburr_Tasks,
        "num_Plating_Tasks" : num_Plating_Tasks,
        }
    
    #Render the HTML template index.html with the data in the context vairable
    return render(request, "index.html", context = context)


class PartDashboardView(generic.ListView):
    model = Part
    context_object_name = "part_list"
    table_class = PartTable
    template_name = 'part_table.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part_component_prep_tasks = ComponentPrepTaskInstance.objects.exclude(part__archive__exact = True)
        part_stacking_tasks = StackingTaskInstance.objects.exclude(part__archive__exact = True)
        part_forming_tasks = FormingTaskInstance.objects.exclude(part__archive__exact = True)
        part_header_plate_tasks = HeaderPlateTaskInstance.objects.exclude(part__archive__exact = True)
        part_pitching_tasks = PitchingTaskInstance.objects.exclude(part__archive__exact = True)
        part_wire_cut_tasks = WireCutTaskInstance.objects.exclude(part__archive__exact = True)
        part_deburr_tasks = DeburrTaskInstance.objects.exclude(part__archive__exact = True)
        part_plating_tasks = PlatingTaskInstance.objects.exclude(part__archive__exact = True)
        #Component Prep Tasks for each individual part
        part = None
        Completedict = {}
        for task in ComponentPrepTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "z":
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     Completedict[task.part] = "Not Complete"
                     
        #Stacking Tasks for each individual part
        partst = None
        StackingCompletedict = {}
        for task in StackingTaskInstance.objects.all():
             if task.part != partst:
                 partst = task.part
                 if task.status != "z":
                     StackingCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     StackingCompletedict[task.part] = "Not Complete"
        #Forming Tasks for each individual part
        partfo = None
        FormingCompletedict = {}
        for task in FormingTaskInstance.objects.all():
             if task.part != partfo:
                 partfo = task.part
                 if task.status != "z":
                     FormingCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     FormingCompletedict[task.part] = "Not Complete"
                     
        #Wire Cut Tasks for each individual part
        partwc = None
        WCCompletedict = {}
        for task in WireCutTaskInstance.objects.all():
             if task.part != partwc:
                 partwc = task.part
                 if task.status != "z":
                     WCCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     WCCompletedict[task.part] = "Not Complete" 
                     
        #Pitching Tasks for each individual part
        partpt = None
        PitchCompletedict = {}
        for task in PitchingTaskInstance.objects.all():
             if task.part != partpt:
                 partpt = task.part
                 if task.status != "z":
                     PitchCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     PitchCompletedict[task.part] = "Not Complete" 
                     
        #Hp Machining Tasks for each individual part
        parthp = None
        HPCompletedict = {}
        for task in HeaderPlateTaskInstance.objects.all():
             if task.part != parthp:
                 parthp = task.part
                 if task.status != "z":
                     HPCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     HPCompletedict[task.part] = "Not Complete"
                     
        #Deburr Tasks for each individual part
        partdb = None
        DeburrCompletedict = {}
        for task in DeburrTaskInstance.objects.all():
             if task.part != partdb:
                 partdb = task.part
                 if task.status != "z":
                     DeburrCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     DeburrCompletedict[task.part] = "Not Complete"
                     
        #Plating Tasks for each individual part
        partpl = None
        PlatingCompletedict = {}
        for task in PlatingTaskInstance.objects.all():
             if task.part != partpl:
                 partpl = task.part
                 if task.status != "z":
                     PlatingCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     PlatingCompletedict[task.part] = "Not Complete"
                     
        Cores_not_in_Archive = Part.objects.filter(archive__exact = False).count()
        context["Cores_not_in_Archive"] = Cores_not_in_Archive
        context["component_prep_tasks_not_completed"] = Completedict
        context["stacking_tasks_not_completed"] = StackingCompletedict
        context["forming_tasks_not_completed"] = FormingCompletedict
        context["HP_tasks_not_completed"] = HPCompletedict
        context["pitching_tasks_not_completed"] = PitchCompletedict
        context["wire_cut_tasks_not_completed"] = WCCompletedict
        context["deburr_tasks_not_completed"] = DeburrCompletedict
        context["plating_tasks_not_completed"] = PlatingCompletedict
        
        context["part_component_prep_tasks"] = part_component_prep_tasks
        context["part_stacking_tasks"] = part_stacking_tasks
        context["part_forming_tasks"] = part_forming_tasks
        context["part_wire_cut_tasks"] = part_wire_cut_tasks
        context["part_pitching_tasks"] = part_pitching_tasks
        context["part_header_plate_tasks"] = part_header_plate_tasks
        context["part_deburr_tasks"] = part_deburr_tasks
        context["part_plating_tasks"] = part_plating_tasks
        
        return context
        

@login_required
def FinalChecks(request):
    """View for finalising the core and peforming final checks"""
    Parts =Part.objects.all()
    CompleteDict = {}
    for part in Parts:
        for task in ComponentPrepTaskInstance.objects.all():
            if task.status != "z":
                CompleteDict[task.part.title]= task.task
        for task in StackingTaskInstance.objects.all():
            if task.status != "z":
                CompleteDict[task.part.title]= task.task
        for task in WireCutTaskInstance.objects.all():
            if task.status != "z":
                CompleteDict[task.part.title]= task.task
        for task in PitchingTaskInstance.objects.all():
            if task.status != "z":
                CompleteDict[task.part.title]= task.task
        for task in HeaderPlateTaskInstance.objects.all():
            if task.status != "z":
                CompleteDict[task.part.title]= task.task
        for task in DeburrTaskInstance.objects.all():
            if task.status != "z":
                CompleteDict[task.part.title]= task.task
        for task in PlatingTaskInstance.objects.all():
            if task.status != "z":
                CompleteDict[task.part.title]= task.task
                
    Cores_not_in_Archive = Part.objects.filter(archive__exact = False).count()
    context = {"Parts": Parts,
               "Check_Tasks_Completed": CompleteDict,
               "Cores_not_in_Archive": Cores_not_in_Archive,
               }
    
    return render(request, "final_checks.html", context = context)

@login_required
def CoreArchive(request):
    Parts =Part.objects.all()
    context = {"Parts": Parts,}
    return render(request, "core_archive.html", context = context)

class CoreArchiveView(generic.ListView):
    model = Part
    context_object_name = "archive_part_list"
    template_name = "core_archive.html"
    
    
    
    def get_queryset(self):
        result = super(CoreArchiveView, self).get_queryset()
        query = self.request.GET.get("search")
        if query:
            postresult = Part.objects.filter(title__contains=query, archive__exact = True)
            result = postresult
        else:
            result = Part.objects.filter(archive__exact = True)
            
        return result
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         Archive_Parts = Part.objects.filter(archive__exact = True)
         context["Archive_Parts"] = Archive_Parts
         return context
        
        

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Part Classes
class PartListView(generic.ListView):
    model = Part
    context_object_name = "part_list"
    template_name = "parts/part_list.html"
    paginate_by = 10



class PartDetailView(generic.DetailView):
    model = Part
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part_component_prep_tasks = ComponentPrepTaskInstance.objects.all()
        part_stacking_tasks = StackingTaskInstance.objects.all()
        part_forming_tasks = FormingTaskInstance.objects.all()
        part_header_plate_tasks = HeaderPlateTaskInstance.objects.all()
        part_pitching_tasks = PitchingTaskInstance.objects.all()
        part_wire_cut_tasks = WireCutTaskInstance.objects.all()
        part_deburr_tasks = DeburrTaskInstance.objects.all()
        part_plating_tasks = PlatingTaskInstance.objects.all()
        #Component Prep Tasks for each individual part
        part = None
        Completedict = {}
        for task in ComponentPrepTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "z":
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     Completedict[task.part] = "Not Complete"
                     
        #Stacking Tasks for each individual part
        partst = None
        StackingCompletedict = {}
        for task in StackingTaskInstance.objects.all():
             if task.part != partst:
                 partst = task.part
                 if task.status != "z":
                     StackingCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     StackingCompletedict[task.part] = "Not Complete"
        #Forming Tasks for each individual part
        partfo = None
        FormingCompletedict = {}
        for task in FormingTaskInstance.objects.all():
             if task.part != partfo:
                 partfo = task.part
                 if task.status != "z":
                     FormingCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     FormingCompletedict[task.part] = "Not Complete"
                     
        #Wire Cut Tasks for each individual part
        partwc = None
        WCCompletedict = {}
        for task in WireCutTaskInstance.objects.all():
             if task.part != partwc:
                 partwc = task.part
                 if task.status != "z":
                     WCCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     WCCompletedict[task.part] = "Not Complete" 
                     
        #Pitching Tasks for each individual part
        partpt = None
        PitchCompletedict = {}
        for task in PitchingTaskInstance.objects.all():
             if task.part != partpt:
                 partpt = task.part
                 if task.status != "z":
                     PitchCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     PitchCompletedict[task.part] = "Not Complete" 
                     
        #Hp Machining Tasks for each individual part
        parthp = None
        HPCompletedict = {}
        for task in HeaderPlateTaskInstance.objects.all():
             if task.part != parthp:
                 parthp = task.part
                 if task.status != "z":
                     HPCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     HPCompletedict[task.part] = "Not Complete"
                     
        #Deburr Tasks for each individual part
        partdb = None
        DeburrCompletedict = {}
        for task in DeburrTaskInstance.objects.all():
             if task.part != partdb:
                 partdb = task.part
                 if task.status != "z":
                     DeburrCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     DeburrCompletedict[task.part] = "Not Complete"
                     
        #Plating Tasks for each individual part
        partpl = None
        PlatingCompletedict = {}
        for task in PlatingTaskInstance.objects.all():
             if task.part != partpl:
                 partpl = task.part
                 if task.status != "z":
                     PlatingCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     PlatingCompletedict[task.part] = "Not Complete"
        context["component_prep_tasks_not_completed"] = Completedict
        context["stacking_tasks_not_completed"] = StackingCompletedict
        context["forming_tasks_not_completed"] = FormingCompletedict
        context["HP_tasks_not_completed"] = HPCompletedict
        context["pitching_tasks_not_completed"] = PitchCompletedict
        context["wire_cut_tasks_not_completed"] = WCCompletedict
        context["deburr_tasks_not_completed"] = DeburrCompletedict
        context["plating_tasks_not_completed"] = PlatingCompletedict
        
        context["part_component_prep_tasks"] = part_component_prep_tasks
        context["part_stacking_tasks"] = part_stacking_tasks
        context["part_forming_tasks"] = part_forming_tasks
        context["part_wire_cut_tasks"] = part_wire_cut_tasks
        context["part_pitching_tasks"] = part_pitching_tasks
        context["part_header_plate_tasks"] = part_header_plate_tasks
        context["part_deburr_tasks"] = part_deburr_tasks
        context["part_plating_tasks"] = part_plating_tasks
        
        return context
    
@login_required
def PartCreate(request):
    model = Part 
    if request.method == 'POST':
        form = PartForm(request.POST or None)
        if form.is_valid():
            part = form.save(commit=False)
            part.poster = request.user
            Component_Prep_tasks = form.cleaned_data.get("Component_Prep_tasks")    
            Stacking_tasks = form.cleaned_data.get("Stacking_tasks") 
            Forming_tasks = form.cleaned_data.get("Forming_tasks") 
            Header_Plate_tasks = form.cleaned_data.get("Header_Plate_tasks") 
            Pitching_tasks = form.cleaned_data.get("Pitching_tasks") 
            Wire_Cut_tasks = form.cleaned_data.get("Wire_Cut_tasks")
            Deburr_tasks = form.cleaned_data.get("Deburr_tasks")
            Plating_tasks = form.cleaned_data.get("Plating_tasks")
            part.save()
            part.Component_Prep_tasks.set(Component_Prep_tasks)
            part.Stacking_tasks.set(Stacking_tasks)
            part.Forming_tasks.set(Forming_tasks)
            part.Header_Plate_tasks.set(Header_Plate_tasks)
            part.Pitching_tasks.set(Pitching_tasks)
            part.Wire_Cut_tasks.set(Wire_Cut_tasks)
            part.Deburr_tasks.set(Deburr_tasks)
            part.Plating_tasks.set(Plating_tasks)
            part.save()
            return HttpResponseRedirect(reverse('part-dashboard'))
    else:
        form = PartForm()
    
    return render(request, "catalog/part_form.html", {"form": form})
        

    
    
class PartUpdate(LoginRequiredMixin,UpdateView):
    model = Part 
    fields = '__all__'
    success_url = reverse_lazy('part-dashboard')
            
        
    
class PartDelete(LoginRequiredMixin,DeleteView):
    model = Part 
    success_url = reverse_lazy('part-dashboard')

#Component Prep Classes
class CpTaskListView(generic.ListView):
    model = ComponentPrepTaskInstance
    context_object_name = "cptask_list"
    template_name = "cptask_list.html"
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_tasks_not_started = ComponentPrepTaskInstance.objects.filter(status__exact="a").count()
        tasks_remaining = ComponentPrepTaskInstance.objects.exclude(status__exact="z").count()
        tasks_complete = ComponentPrepTaskInstance.objects.filter(status__exact="z", part__archive__exact = False).count()
        tasks_on_hold = ComponentPrepTaskInstance.objects.filter(status__exact="h").count()
        not_archived_tasks = ComponentPrepTaskInstance.objects.exclude(part__archive__exact = True).count()
        context["not_archived_tasks"] = not_archived_tasks
        context["num_tasks_not_started"] = num_tasks_not_started
        context["tasks_remaining"] = tasks_remaining
        context["tasks_complete"] = tasks_complete
        context["tasks_on_hold"] = tasks_on_hold
        return context
    
class CPTaskDetailView(generic.DetailView):
    model = ComponentPrepTaskInstance
    
class CPTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = ComponentPrepTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('cptasks')
    
class CPTaskDelete(LoginRequiredMixin,DeleteView):
    model = ComponentPrepTaskInstance 
    success_url = reverse_lazy('cptasks')
    
def StartCPTask(request, pk):
    Task = ComponentPrepTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.status = "b"
    Task.starttime = str_Time
    Task.starttimenum = time.time()
    start = float(Task.createtimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetostartstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('cptasks'))

def FinishCPTask(request, pk):
    Task = ComponentPrepTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.finishtime = str_Time
    Task.status = "z"
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('cptasks'))
  
#Stacking Classes  
class StackingTaskListView(generic.ListView):
    model = StackingTaskInstance
    context_object_name = "stackingtask_list"
    template_name = "stackingtask/stackingtaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         num_tasks_not_started = StackingTaskInstance.objects.filter(status__exact="a").count()
         tasks_remaining = StackingTaskInstance.objects.exclude(status__exact="z").count()
         part = None
         Completedict = {}
         for task in ComponentPrepTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "z":
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     Completedict[task.part] = "Not Complete"
         not_archived_tasks = StackingTaskInstance.objects.exclude(part__archive__exact = True).count()
         context["not_archived_tasks"] = not_archived_tasks                
         context["component_prep_tasks_not_completed"] = Completedict
         context["num_tasks_not_started"] = num_tasks_not_started
         context["tasks_remaining"] = tasks_remaining
         return context
     
class StackingTaskDetailView(generic.DetailView):
    model = StackingTaskInstance
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part = None
        Completedict = {}
        for task in ComponentPrepTaskInstance.objects.all():
            if task.part != part:
                part = task.part
                if task.status != "z":
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != "z":
                    Completedict[task.part] = "Not Complete"
        context["component_prep_tasks_not_completed"] = Completedict
        return context
    
class StackingTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = StackingTaskInstance
    fields = ['status'] 
    
class StackingTaskDelete(LoginRequiredMixin,DeleteView):
    model = StackingTaskInstance 
    success_url = reverse_lazy('stackingtasks')
    

def StartStackTask(request, pk):
    Task = StackingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.status = "b"
    Task.starttime = str_Time
    Task.starttimenum = time.time()
    start = float(Task.createtimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetostartstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('stackingtasks'))

def FinishStackTask(request, pk):
    Task = StackingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.finishtime = str_Time
    Task.status = "z"
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('stackingtasks'))    
    

 
# Sheet Metal Forming Classes
class FormingTaskInstanceListView(generic.ListView):
    model = FormingTaskInstance
    context_object_name = "formingtask_list"
    template_name = "formingtask/formingtaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         tasks_remaining = FormingTaskInstance.objects.exclude(status__exact="z").count()
         num_tasks_not_started = FormingTaskInstance.objects.filter(status__exact="a").count()
         not_archived_tasks = FormingTaskInstance.objects.exclude(part__archive__exact = True).count()
         context["not_archived_tasks"] = not_archived_tasks
         context["num_tasks_not_started"] = num_tasks_not_started
         context["tasks_remaining"] = tasks_remaining
         return context 
     
class FormingTaskInstanceDetailView(generic.DetailView):
    model = FormingTaskInstance
    
class FormingTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = FormingTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('formingtasks')
    
class FormingTaskDelete(LoginRequiredMixin,DeleteView):
    model = FormingTaskInstance 
    success_url = reverse_lazy('formingtasks')
    
def StartFormingTask(request, pk):
    Task = FormingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.status = "b"
    Task.starttime = str_Time
    Task.starttimenum = time.time()
    start = float(Task.createtimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetostartstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('formingtasks'))

def FinishFormingTask(request, pk):
    Task = FormingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.finishtime = str_Time
    Task.status = "z"
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('formingtasks'))
    
#Header Plate Views
class HeaderPlateTaskInstanceListView(generic.ListView):
    model = HeaderPlateTaskInstance
    context_object_name = "headerplatetask_list"
    template_name = "headerplatetask/headerplatetaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         tasks_remaining = HeaderPlateTaskInstance.objects.exclude(status__exact="z").count()
         num_tasks_not_started = HeaderPlateTaskInstance.objects.filter(status__exact="a").count()
         part = None
         Completedict = {}
         for task in PitchingTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "z":
                     Completedict[task.part] = "Not Complete"
             else:
                 if task.status != "z":
                    Completedict[task.part] = "Not Complete"
         not_archived_tasks = HeaderPlateTaskInstance.objects.exclude(part__archive__exact = True).count()
         context["not_archived_tasks"] = not_archived_tasks     
         context["pitching_tasks_not_completed"] = Completedict
         context["num_tasks_not_started"] = num_tasks_not_started
         context["tasks_remaining"] = tasks_remaining
         return context 

class HeaderPlateTaskInstanceDetailView(generic.DetailView):
    model = HeaderPlateTaskInstance

class HeaderPlateTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = HeaderPlateTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('headerplatetasks')
    
class HeaderPlateTaskDelete(LoginRequiredMixin,DeleteView):
    model = HeaderPlateTaskInstance 
    success_url = reverse_lazy('headerplatetasks')
    
def StartHeaderPlateTask(request, pk):
    Task = HeaderPlateTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.status = "b"
    Task.starttime = str_Time
    Task.starttimenum = time.time()
    start = float(Task.createtimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetostartstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('headerplatetasks'))

def FinishHeaderPlateTask(request, pk):
    Task = HeaderPlateTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.finishtime = str_Time
    Task.status = "z"
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('headerplatetasks'))

#Pitching Task Views
class PitchingTaskListView(generic.ListView):
    model = PitchingTaskInstance
    context_object_name = "pitchingtask_list"
    template_name = "pitchingtask/pitchingtaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         num_tasks_not_started = PitchingTaskInstance.objects.filter(status__exact="a").count()
         tasks_remaining = PitchingTaskInstance.objects.exclude(status__exact="z").count()
         part = None
         Completedict = {}
         for task in WireCutTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "z":
                     Completedict[task.part] = "Not Complete"
             else:
                 if task.status != "z":
                    Completedict[task.part] = "Not Complete"
         not_archived_tasks = PitchingTaskInstance.objects.exclude(part__archive__exact = True).count()
         context["not_archived_tasks"] = not_archived_tasks    
         context["wire_cut_tasks_not_completed"] = Completedict
         context["num_tasks_not_started"] = num_tasks_not_started
         context["tasks_remaining"] = tasks_remaining
         return context

class PitchingTaskDetailView(generic.DetailView):
    model = PitchingTaskInstance
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part = None
        Completedict = {}
        for task in WireCutTaskInstance.objects.all():
            if task.part != part:
                part = task.part
                if task.status != "z":
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != "z":
                    Completedict[task.part] = "Not Complete"
        context["wire_cut_tasks_not_completed"] = Completedict
        return context
    
class PitchingTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = PitchingTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('pitchingtasks')
    
class PitchingTaskDelete(LoginRequiredMixin,DeleteView):
    model = PitchingTaskInstance 
    success_url = reverse_lazy('pitchingtasks')
    
def StartPitchingTask(request, pk):
    Task = PitchingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.status = "b"
    Task.starttime = str_Time
    Task.starttimenum = time.time()
    start = float(Task.createtimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetostartstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('pitchingtasks'))

def FinishPitchingTask(request, pk):
    Task = PitchingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.finishtime = str_Time
    Task.status = "z"
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('pitchingtasks'))


#Wire Cut Task Views
class WireCutTaskListView(generic.ListView):
    model = WireCutTaskInstance
    context_object_name = "wirecuttask_list"
    template_name = "wirecuttask/wirecuttaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         num_tasks_not_started = WireCutTaskInstance.objects.filter(status__exact="a").count()
         tasks_remaining = WireCutTaskInstance.objects.exclude(status__exact="z").count()
         part = None
         Completedict = {}
         for task in StackingTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "z":
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     Completedict[task.part] = "Not Complete"
         not_archived_tasks = WireCutTaskInstance.objects.exclude(part__archive__exact = True).count()
         context["not_archived_tasks"] = not_archived_tasks  
         context["stacking_tasks_not_completed"] = Completedict
         context["num_tasks_not_started"] = num_tasks_not_started
         context["tasks_remaining"] = tasks_remaining
         return context

class WireCutTaskDetailView(generic.DetailView):
    model = WireCutTaskInstance
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part = None
        Completedict = {}
        for task in StackingTaskInstance.objects.all():
            if task.part != part:
                part = task.part
                if task.status != "z":
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != "z":
                    Completedict[task.part] = "Not Complete"
        context["stacking_tasks_not_completed"] = Completedict
        return context
    
class WireCutTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = WireCutTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('wirecuttasks')
    
class WireCutTaskDelete(LoginRequiredMixin,DeleteView):
    model = WireCutTaskInstance
    success_url = reverse_lazy('wirecuttasks')
    
def StartWireCutTask(request, pk):
    Task = WireCutTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.status = "b"
    Task.starttime = str_Time
    Task.starttimenum = time.time()
    start = float(Task.createtimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetostartstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('wirecuttasks'))

def FinishWireCutTask(request, pk):
    Task = WireCutTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.finishtime = str_Time
    Task.status = "z"
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('wirecuttasks'))


#Deburr Task Views
class DeburrTaskListView(generic.ListView):
    model = DeburrTaskInstance
    context_object_name = "deburrtask_list"
    template_name = "deburrtask/deburrtaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         num_tasks_not_started = DeburrTaskInstance.objects.filter(status__exact="a").count()
         tasks_remaining = DeburrTaskInstance.objects.exclude(status__exact="z").count()
         part = None
         Completedict = {}
         for task in HeaderPlateTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "z":
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     Completedict[task.part] = "Not Complete"
         not_archived_tasks = DeburrTaskInstance.objects.exclude(part__archive__exact = True).count()
         context["not_archived_tasks"] = not_archived_tasks  
         context["header_plate_tasks_not_completed"] = Completedict
         context["num_tasks_not_started"] = num_tasks_not_started
         context["tasks_remaining"] = tasks_remaining
         return context

class DeburrTaskDetailView(generic.DetailView):
    model = DeburrTaskInstance
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part = None
        Completedict = {}
        for task in HeaderPlateTaskInstance.objects.all():
            if task.part != part:
                part = task.part
                if task.status != "z":
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != "z":
                    Completedict[task.part] = "Not Complete"
        context["header_plate_tasks_not_completed"] = Completedict
        return context
    
class DeburrTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = DeburrTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('deburrtasks')
    
class DeburrTaskDelete(LoginRequiredMixin,DeleteView):
    model = DeburrTaskInstance
    success_url = reverse_lazy('deburrtasks')
    
def StartDeburrTask(request, pk):
    Task = DeburrTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.status = "b"
    Task.starttime = str_Time
    Task.starttimenum = time.time()
    start = float(Task.createtimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetostartstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('deburrtasks'))

def FinishDeburrTask(request, pk):
    Task = DeburrTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.finishtime = str_Time
    Task.status = "z"
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('deburrtasks'))

#Plating Task Views
class PlatingTaskListView(generic.ListView):
    model = PlatingTaskInstance
    context_object_name = "platingtask_list"
    template_name = "platingtask/platingtaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         num_tasks_not_started = PlatingTaskInstance.objects.filter(status__exact="a").count()
         tasks_remaining = PlatingTaskInstance.objects.exclude(status__exact="z").count()
         part = None
         Completedict = {}
         for task in DeburrTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "z":
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != "z":
                     Completedict[task.part] = "Not Complete"
         not_archived_tasks = PlatingTaskInstance.objects.exclude(part__archive__exact = True).count()
         context["not_archived_tasks"] = not_archived_tasks
         context["deburr_tasks_not_completed"] = Completedict
         context["num_tasks_not_started"] = num_tasks_not_started
         context["tasks_remaining"] = tasks_remaining
         return context

class PlatingTaskDetailView(generic.DetailView):
    model = PlatingTaskInstance
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part = None
        Completedict = {}
        for task in DeburrTaskInstance.objects.all():
            if task.part != part:
                part = task.part
                if task.status != "z":
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != "z":
                    Completedict[task.part] = "Not Complete"
        context["deburr_tasks_not_completed"] = Completedict
        return context
    
class PlatingTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = PlatingTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('platingtasks')
    
class PlatingTaskDelete(LoginRequiredMixin,DeleteView):
    model = PlatingTaskInstance
    success_url = reverse_lazy('platingtasks')
    
def StartPlatingTask(request, pk):
    Task = PlatingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.status = "b"
    Task.starttime = str_Time
    Task.starttimenum = time.time()
    start = float(Task.createtimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetostartstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('platingtasks'))

def FinishPlatingTask(request, pk):
    Task = PlatingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%x")
    Task.finishtime = str_Time
    Task.status = "z"
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days, {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('platingtasks'))

#Complete Core
@login_required 
def PartComplete(request, pk):
    instance = get_object_or_404(Part, pk = pk)
    form = ArchiveForm(request.POST or None, instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.poster = request.user
        archive = form.cleaned_data.get("archive")
        instance.archive = archive
        instance.save()
        return HttpResponseRedirect(reverse('part-dashboard'))
    
    return render(request, "catalog/part_confirm_complete.html", {"form": form})
    
