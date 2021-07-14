from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import ComponentPrepTaskInstance, Part, StackingTaskInstance, FormingTaskInstance, HeaderPlateTaskInstance, PitchingTaskInstance, WireCutTaskInstance, DeburrTaskInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm

def index(request):
    """View for the home page of the website"""
    
    #Generate counts for soe of the main objetcs
    num_CpTasks = ComponentPrepTaskInstance.objects.all().count()
    num_Stacking_Tasks = StackingTaskInstance.objects.all().count()
    
    #avalible tasks remaining
    tasks_remaning = ComponentPrepTaskInstance.objects.exclude(status__exact="c").count()
    
    #all() is implied by default
    num_parts = Part.objects.all().count()
    
    #Number of site visits by the current user    
    context = {
        "num_CpTasks": num_CpTasks,
        "num_parts": num_parts,  
        "tasks_remaning":tasks_remaning,
        "num_Stacking_Tasks": num_Stacking_Tasks,
        }
    
    #Render the HTML template index.html with the data in the context vairable
    return render(request, "index.html", context = context)

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
        #Component Prep Tasks for each individual part
        part = None
        Completedict = {}
        for task in ComponentPrepTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "c":
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != "c":
                     Completedict[task.part] = "Not Complete"
                     
        #Stacking Tasks for each individual part
        partst = None
        StackingCompletedict = {}
        for task in StackingTaskInstance.objects.all():
             if task.part != partst:
                 partst = task.part
                 if task.status != "c":
                     StackingCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "c":
                     StackingCompletedict[task.part] = "Not Complete"
        #Forming Tasks for each individual part
        partfo = None
        FormingCompletedict = {}
        for task in FormingTaskInstance.objects.all():
             if task.part != partfo:
                 partfo = task.part
                 if task.status != "c":
                     FormingCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "c":
                     FormingCompletedict[task.part] = "Not Complete"
                     
        #Wire Cut Tasks for each individual part
        partwc = None
        WCCompletedict = {}
        for task in WireCutTaskInstance.objects.all():
             if task.part != partwc:
                 partwc = task.part
                 if task.status != "c":
                     WCCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "c":
                     WCCompletedict[task.part] = "Not Complete" 
                     
        #Pitching Tasks for each individual part
        partpt = None
        PitchCompletedict = {}
        for task in PitchingTaskInstance.objects.all():
             if task.part != partpt:
                 partpt = task.part
                 if task.status != "c":
                     PitchCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "c":
                     PitchCompletedict[task.part] = "Not Complete" 
                     
        #Hp Machining Tasks for each individual part
        parthp = None
        HPCompletedict = {}
        for task in HeaderPlateTaskInstance.objects.all():
             if task.part != parthp:
                 parthp = task.part
                 if task.status != "c":
                     HPCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "c":
                     HPCompletedict[task.part] = "Not Complete"
                     
        #Deburr Tasks for each individual part
        partdb = None
        DeburrCompletedict = {}
        for task in DeburrTaskInstance.objects.all():
             if task.part != partdb:
                 partdb = task.part
                 if task.status != "c":
                     DeburrCompletedict[task.part] = "Not Complete"
             else:
                if task.status != "c":
                     DeburrCompletedict[task.part] = "Not Complete"
        context["component_prep_tasks_not_completed"] = Completedict
        context["stacking_tasks_not_completed"] = StackingCompletedict
        context["forming_tasks_not_completed"] = FormingCompletedict
        context["HP_tasks_not_completed"] = HPCompletedict
        context["pitching_tasks_not_completed"] = PitchCompletedict
        context["wire_cut_tasks_not_completed"] = WCCompletedict
        context["deburr_tasks_not_completed"] = DeburrCompletedict
        
        context["part_component_prep_tasks"] = part_component_prep_tasks
        context["part_stacking_tasks"] = part_stacking_tasks
        context["part_forming_tasks"] = part_forming_tasks
        context["part_wire_cut_tasks"] = part_wire_cut_tasks
        context["part_pitching_tasks"] = part_pitching_tasks
        context["part_header_plate_tasks"] = part_header_plate_tasks
        context["part_deburr_tasks"] = part_deburr_tasks
        
        return context

class PartCreate(LoginRequiredMixin,CreateView):
    model = Part 
    fields = ['title','serial', 'team', 'Component_Prep_tasks','Stacking_tasks',
              'Forming_tasks','Header_Plate_tasks','Pitching_tasks',
              'Wire_Cut_tasks','Deburr_tasks','pub_date']
    initial = {'pub_date': timezone.now}
    success_url = reverse_lazy('parts')
    
class PartUpdate(LoginRequiredMixin,UpdateView):
    model = Part 
    fields = '__all__'
    success_url = reverse_lazy('parts')
    
class PartDelete(LoginRequiredMixin,DeleteView):
    model = Part 
    success_url = reverse_lazy('parts')

#Component Prep Classes
class CpTaskListView(generic.ListView):
    model = ComponentPrepTaskInstance
    context_object_name = "cptask_list"
    template_name = "cptask_list.html"
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_tasks_not_started = ComponentPrepTaskInstance.objects.filter(status__exact="a").count()
        tasks_remaining = ComponentPrepTaskInstance.objects.exclude(status__exact="c").count()
        tasks_complete = ComponentPrepTaskInstance.objects.filter(status__exact="c").count()
        tasks_on_hold = ComponentPrepTaskInstance.objects.filter(status__exact="h").count()
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
    Task.status = "p"
    Task.save()
    return HttpResponseRedirect(reverse('cptasks'))

def FinishCPTask(request, pk):
    Task = ComponentPrepTaskInstance.objects.get(pk = pk)
    Task.status = "c"
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
         tasks_remaining = StackingTaskInstance.objects.exclude(status__exact="c").count()
         part = None
         Completedict = {}
         for task in ComponentPrepTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "c":
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != "c":
                     Completedict[task.part] = "Not Complete"
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
                if task.status != "c":
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != "c":
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
    Task.status = "p"
    Task.save()
    return HttpResponseRedirect(reverse('stackingtasks'))

def FinishStackTask(request, pk):
    Task = StackingTaskInstance.objects.get(pk = pk)
    Task.status = "c"
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
         tasks_remaining = FormingTaskInstance.objects.exclude(status__exact="c").count()
         num_tasks_not_started = FormingTaskInstance.objects.filter(status__exact="a").count()
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
    Task.status = "p"
    Task.save()
    return HttpResponseRedirect(reverse('formingtasks'))

def FinishFormingTask(request, pk):
    Task = FormingTaskInstance.objects.get(pk = pk)
    Task.status = "c"
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
         tasks_remaining = HeaderPlateTaskInstance.objects.exclude(status__exact="c").count()
         num_tasks_not_started = HeaderPlateTaskInstance.objects.filter(status__exact="a").count()
         part = None
         Completedict = {}
         for task in PitchingTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "c":
                     Completedict[task.part] = "Not Complete"
             else:
                 if task.status != "c":
                    Completedict[task.part] = "Not Complete"
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
    Task.status = "p"
    Task.save()
    return HttpResponseRedirect(reverse('headerplatetasks'))

def FinishHeaderPlateTask(request, pk):
    Task = HeaderPlateTaskInstance.objects.get(pk = pk)
    Task.status = "c"
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
         tasks_remaining = PitchingTaskInstance.objects.exclude(status__exact="c").count()
         part = None
         Completedict = {}
         for task in WireCutTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "c":
                     Completedict[task.part] = "Not Complete"
             else:
                 if task.status != "c":
                    Completedict[task.part] = "Not Complete"
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
                if task.status != "c":
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != "c":
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
    Task.status = "p"
    Task.save()
    return HttpResponseRedirect(reverse('pitchingtasks'))

def FinishPitchingTask(request, pk):
    Task = PitchingTaskInstance.objects.get(pk = pk)
    Task.status = "c"
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
         tasks_remaining = WireCutTaskInstance.objects.exclude(status__exact="c").count()
         part = None
         Completedict = {}
         for task in StackingTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "c":
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != "c":
                     Completedict[task.part] = "Not Complete"
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
                if task.status != "c":
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != "c":
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
    Task.status = "p"
    Task.save()
    return HttpResponseRedirect(reverse('wirecuttasks'))

def FinishWireCutTask(request, pk):
    Task = WireCutTaskInstance.objects.get(pk = pk)
    Task.status = "c"
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
         tasks_remaining = DeburrTaskInstance.objects.exclude(status__exact="c").count()
         part = None
         Completedict = {}
         for task in HeaderPlateTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != "c":
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != "c":
                     Completedict[task.part] = "Not Complete"
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
                if task.status != "c":
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != "c":
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
    Task.status = "p"
    Task.save()
    return HttpResponseRedirect(reverse('deburrtasks'))

def FinishDeburrTask(request, pk):
    Task = DeburrTaskInstance.objects.get(pk = pk)
    Task.status = "c"
    Task.save()
    return HttpResponseRedirect(reverse('deburrtasks'))