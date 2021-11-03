from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import ComponentPrepTaskInstance, Part, StackingTaskInstance,\
    FormingTaskInstance, HeaderPlateTaskInstance, PitchingTaskInstance,\
        WireCutTaskInstance, DeburrTaskInstance, PlatingTaskInstance, Team, \
        Component_Prep_Task, Forming_Task, Stacking_Task, Wire_Cut_Task,\
        Pitching_Task, Header_Plate_Task, Deburr_Task, Plating_Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
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
from .signals import Part_Saved
from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
from catalog.camera import MaskDetect
import time

def index(request):
    """View for the home page of the website"""
    
    #Generate counts for soe of the main objetcs
    num_CpTasks = ComponentPrepTaskInstance.objects.exclude(status__exact=10).count()
    num_Forming_Tasks = FormingTaskInstance.objects.exclude(status__exact=10).count()
    num_Stacking_Tasks = StackingTaskInstance.objects.exclude(status__exact=10).count()
    num_Wire_Cut_Tasks = WireCutTaskInstance.objects.exclude(status__exact=10).count()
    num_Pitching_Tasks = PitchingTaskInstance.objects.exclude(status__exact=10).count()
    num_HP_Tasks = HeaderPlateTaskInstance.objects.exclude(status__exact=10).count()
    num_Deburr_Tasks = DeburrTaskInstance.objects.exclude(status__exact=10).count()
    num_Plating_Tasks = PlatingTaskInstance.objects.exclude(status__exact =10).count()
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



def ScanResult(request):
    """ Page For Scanning Work Orders"""  
    
    HPTasks = HeaderPlateTaskInstance.objects.exclude(status__exact =10, part__archive__exact = True)
    context = {"Barcode": barcodestr,
               "HPTasks": HPTasks}
    
    return render(request, "ScanDisplay.html", context = context)

def WorkOrderScan(request):
    """ Page For Scanning Work Orders"""
    barcode = next(gen(MaskDetect()))
    barcode = barcode[-30:]
    barcode = barcode.decode("utf-8")
    barcode = barcode.split("_")[1]
    
    context = {"Barcode": barcode}
    
    return render(request, "WorkOrderScan.html", context = context)


def gen(camera):
    while True:
        frame = camera.get_frame()
        barcode = barcode = camera.get_barcode()
        if barcode.decode("utf-8") != "_No Barcode Currently Scanned":
            global barcodestr
            barcodestr = barcode.decode("utf-8")
            print(barcodestr)
            break
            #return HttpResponseRedirect(reverse('index'))
        yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'+barcode)
        
    
        

def mask_feed(request):
    return StreamingHttpResponse(gen(MaskDetect()),
					content_type='multipart/x-mixed-replace; boundary=frame')


class PartDashboardView(generic.ListView):
    model = Part
    context_object_name = "part_list"
    table_class = PartTable
    template_name = 'part_table.html'
    paginate_by = 40
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Component_Prep_Tasks = Component_Prep_Task.objects.all()
        Forming_Tasks = Forming_Task.objects.all()
        Stacking_Tasks = Stacking_Task.objects.all()
        Wire_Cut_Tasks = Wire_Cut_Task.objects.all()
        Pitching_Tasks = Pitching_Task.objects.all()
        HP_Tasks = Header_Plate_Task.objects.all()
        Deburr_Tasks = Deburr_Task.objects.all()
        Plating_Tasks = Plating_Task.objects.all()
        
        Current_Part_List = Part.objects.exclude(archive__exact = True)
        
        part_component_prep_tasks = ComponentPrepTaskInstance.objects.exclude(part__archive__exact = True)
        part_stacking_tasks = StackingTaskInstance.objects.exclude(part__archive__exact = True)
        part_forming_tasks = FormingTaskInstance.objects.exclude(part__archive__exact = True)
        part_header_plate_tasks = HeaderPlateTaskInstance.objects.exclude(part__archive__exact = True)
        part_pitching_tasks = PitchingTaskInstance.objects.exclude(part__archive__exact = True)
        part_wire_cut_tasks = WireCutTaskInstance.objects.exclude(part__archive__exact = True)
        part_deburr_tasks = DeburrTaskInstance.objects.exclude(part__archive__exact = True)
        part_plating_tasks = PlatingTaskInstance.objects.exclude(part__archive__exact = True)
        #Component Prep Tasks for each individual part
                     
        #DisplayList For CP Tasks:
        CPDict = {} 
        for task in part_component_prep_tasks:
            part = task.part.title
            serial = task.part.serial
            CPDict[part+"_"+serial] = []
            
        for task in part_component_prep_tasks:
            part = task.part.title
            serial = task.part.serial
            taskname = task.task
            CPDict[part+"_"+serial].append(taskname)
            
        for PartSerial in CPDict:
            if "Linish Tube" in CPDict[PartSerial]:
                CPDict[PartSerial].append("Linish Tube")
            else:
                CPDict[PartSerial].append("-")
            if "Deburr Sheet Metal" in CPDict[PartSerial]:
                CPDict[PartSerial].append("Deburr Sheet Metal")
            else:
                CPDict[PartSerial].append("-" )
            if "Expand Tube" in CPDict[PartSerial]:
                CPDict[PartSerial].append("Expand Tube")
            else:
                CPDict[PartSerial].append("-")
                
            if "Prepare Turb" in CPDict[PartSerial]:
                CPDict[PartSerial].append("Prepare Turb")
            else:
                CPDict[PartSerial].append("-")
                
            if "Load Turb" in CPDict[PartSerial]:
                CPDict[PartSerial].append("Load Turb")
            else:
                CPDict[PartSerial].append("-")
                
            if "Roll Tube" in CPDict[PartSerial]:
                CPDict[PartSerial].append("Roll Tube")
            else:
                CPDict[PartSerial].append("-")
                
            if "Markout Tube" in CPDict[PartSerial]:
                CPDict[PartSerial].append("Markout Tube")
            else:
                CPDict[PartSerial].append("-")
            if "HyBraze Rub" in CPDict[PartSerial]:
                CPDict[PartSerial].append("HyBraze Rub")
            else:
                CPDict[PartSerial].append("-")
                
            if "Install Prewires" in CPDict[PartSerial]:
                CPDict[PartSerial].append("Install Prewires")
            else:
                CPDict[PartSerial].append("-")
            
            CPDict[PartSerial] = CPDict[PartSerial][-9:]
            
        CPpartlist =[]
        for part in CPDict:
            CPpartlist.append(CPDict[part])
        
                
        #DisplayList For Forming Tasks:
        FODict = {} 
        for task in part_forming_tasks:
            part = task.part.title
            serial = task.part.serial
            FODict[part+"_"+serial] = []
            
        for task in part_forming_tasks:
            part = task.part.title
            serial = task.part.serial
            taskname = task.task
            FODict[part+"_"+serial].append(taskname)
            
        for PartSerial in FODict:
            if "Form Header Plate" in FODict[PartSerial]:
                FODict[PartSerial].append("Form Header Plate")
            else:
                FODict[PartSerial].append("-")
            
            FODict[PartSerial] = FODict[PartSerial][-1:]
            
        FOpartlist =[]
        for part in FODict:
            FOpartlist.append(FODict[part])
            
            
        #DisplayList For Stacking Tasks:
        STDict = {} 
        for task in part_stacking_tasks:
            part = task.part.title
            serial = task.part.serial
            STDict[part+"_"+serial] = []
            
        for task in part_stacking_tasks:
            part = task.part.title
            serial = task.part.serial
            taskname = task.task
            STDict[part+"_"+serial].append(taskname)
            
        for PartSerial in STDict:
            if "Set up Table" in STDict[PartSerial]:
                STDict[PartSerial].append("Set up Table")
            else:
                STDict[PartSerial].append("-")
            if "Stack Core" in STDict[PartSerial]:
                STDict[PartSerial].append("Stack Core")
            else:
                STDict[PartSerial].append("-")
            if "Post Stacking Braze Check" in STDict[PartSerial]:
                STDict[PartSerial].append("Post Stacking Braze Check")
            else:
                STDict[PartSerial].append("-")
            
            STDict[PartSerial] = STDict[PartSerial][-3:]
            
        STpartlist =[]
        for part in STDict:
            STpartlist.append(STDict[part])
            
        
        #DisplayList For Wire Cut Tasks:
        WCDict = {} 
        for task in part_wire_cut_tasks:
            part = task.part.title
            serial = task.part.serial
            WCDict[part+"_"+serial] = []
            
        for task in part_wire_cut_tasks:
            part = task.part.title
            serial = task.part.serial
            taskname = task.task
            WCDict[part+"_"+serial].append(taskname)
            
        for PartSerial in WCDict:
            if "Wire Cut Core" in WCDict[PartSerial]:
                WCDict[PartSerial].append("Wire Cut Core")
            else:
                WCDict[PartSerial].append("-")
            
            WCDict[PartSerial] = WCDict[PartSerial][-1:]
            
        WCpartlist =[]
        for part in WCDict:
            WCpartlist.append(WCDict[part])
            
        
                #DisplayList For Pitching Tasks:
        PTDict = {} 
        for task in part_pitching_tasks:
            part = task.part.title
            serial = task.part.serial
            PTDict[part+"_"+serial] = []
            
        for task in part_pitching_tasks:
            part = task.part.title
            serial = task.part.serial
            taskname = task.task
            PTDict[part+"_"+serial].append(taskname)
            
        for PartSerial in PTDict:
            if "Pitch Core" in PTDict[PartSerial]:
                PTDict[PartSerial].append("Pitch Core")
            else:
                PTDict[PartSerial].append("-")
            if "Slot Generation" in PTDict[PartSerial]:
                PTDict[PartSerial].append("Slot Generation")
            else:
                PTDict[PartSerial].append("-")

            
            PTDict[PartSerial] = PTDict[PartSerial][-2:]
            
        PTpartlist =[]
        for part in PTDict:
            PTpartlist.append(PTDict[part])
            
            
            
                #DisplayList For HP Machining Tasks:
        HPDict = {} 
        for task in part_header_plate_tasks:
            part = task.part.title
            serial = task.part.serial
            HPDict[part+"_"+serial] = []
            
        for task in part_header_plate_tasks:
            part = task.part.title
            serial = task.part.serial
            taskname = task.task
            HPDict[part+"_"+serial].append(taskname)
            
        for PartSerial in HPDict:
            if "Program HP Machining" in HPDict[PartSerial]:
                HPDict[PartSerial].append("Program HP Machining")
            else:
                HPDict[PartSerial].append("-")
            if "Machine Header Plate" in HPDict[PartSerial]:
                HPDict[PartSerial].append("Machine Header Plate")
            else:
                HPDict[PartSerial].append("-")

            
            HPDict[PartSerial] = HPDict[PartSerial][-2:]
            
        HPpartlist =[]
        for part in HPDict:
            HPpartlist.append(HPDict[part])
            
            
                        #DisplayList For Deburr Tasks:
        DBDict = {} 
        for task in part_deburr_tasks:
            part = task.part.title
            serial = task.part.serial
            DBDict[part+"_"+serial] = []
            
        for task in part_deburr_tasks:
            part = task.part.title
            serial = task.part.serial
            taskname = task.task
            DBDict[part+"_"+serial].append(taskname)
            
        for PartSerial in DBDict:
            if "Deburr Core" in DBDict[PartSerial]:
                DBDict[PartSerial].append("Deburr Core")
            else:
                DBDict[PartSerial].append("-")
            if "Deburr Header Plate" in DBDict[PartSerial]:
                DBDict[PartSerial].append("Deburr Header Plate")
            else:
                DBDict[PartSerial].append("-")

            
            DBDict[PartSerial] = DBDict[PartSerial][-2:]
            
        DBpartlist =[]
        for part in DBDict:
            DBpartlist.append(DBDict[part])
            
            
        #DisplayList For PL Tasks:
        PLDict = {} 
        for task in part_plating_tasks:
            part = task.part.title
            serial = task.part.serial
            PLDict[part+"_"+serial] = []
            
        for task in part_plating_tasks:
            part = task.part.title
            serial = task.part.serial
            taskname = task.task
            PLDict[part+"_"+serial].append(taskname)
            
        for PartSerial in PLDict:
            if "Plate Core" in PLDict[PartSerial]:
                PLDict[PartSerial].append("Plate Core")
            else:
                PLDict[PartSerial].append("-")
            if "Install Baffles" in PLDict[PartSerial]:
                PLDict[PartSerial].append("Install Baffles")
            else:
                PLDict[PartSerial].append("-" )
            if "Scribe Header Plate" in PLDict[PartSerial]:
                PLDict[PartSerial].append("Scribe Header Plate")
            else:
                PLDict[PartSerial].append("-")
                
            if "Post Braze Check" in PLDict[PartSerial]:
                PLDict[PartSerial].append("Post Braze Check")
            else:
                PLDict[PartSerial].append("-")
            
            PLDict[PartSerial] = PLDict[PartSerial][-4:]
            
        PLpartlist =[]
        for part in PLDict:
            PLpartlist.append(PLDict[part])
       
                     
        Cores_not_in_Archive = Part.objects.filter(archive__exact = False).count()
        context["Cores_not_in_Archive"] = Cores_not_in_Archive
        
        context["part_component_prep_tasks"] = part_component_prep_tasks
        context["part_stacking_tasks"] = part_stacking_tasks
        context["part_forming_tasks"] = part_forming_tasks
        context["part_wire_cut_tasks"] = part_wire_cut_tasks
        context["part_pitching_tasks"] = part_pitching_tasks
        context["part_header_plate_tasks"] = part_header_plate_tasks
        context["part_deburr_tasks"] = part_deburr_tasks
        context["part_plating_tasks"] = part_plating_tasks
        
        context["Component_Prep_Tasks"] = Component_Prep_Tasks
        context["Forming_Tasks"] = Forming_Tasks
        context["Stacking_Tasks"] = Stacking_Tasks
        context["Wire_Cut_Tasks"] = Wire_Cut_Tasks
        context["Pitching_Tasks"] = Pitching_Tasks
        context["HP_Tasks"] = HP_Tasks
        context["Deburr_Tasks"] = Deburr_Tasks
        context["Plating_Tasks"] = Plating_Tasks    
        
        #DisplayLists
        context["CPpartlist"] = CPpartlist
        context["FOpartlist"] = FOpartlist
        context["STpartlist"] = STpartlist
        context["WCpartlist"] = WCpartlist
        context["PTpartlist"] = PTpartlist
        context["HPpartlist"] = HPpartlist
        context["DBpartlist"] = DBpartlist
        context["PLpartlist"] = PLpartlist
        
        context["Current_Part_List"] = Current_Part_List
        return context
        

@login_required
def FinalChecks(request):
    """View for finalising the core and peforming final checks"""
    Parts =Part.objects.all()
    CompleteDict = {}
    for part in Parts:
        Partkey = part.title+"s"+part.serial
        cptasks = ComponentPrepTaskInstance.objects.filter(part__title = part.title)
        for task in cptasks:
            if task.part.serial == part.serial:
                if task.status != 10:
                    CompleteDict[Partkey]= task.task
        stackingtasks = StackingTaskInstance.objects.filter(part__title = part.title)
        for task in stackingtasks:
            if task.part.serial == part.serial:
                if task.status != 10:
                    CompleteDict[Partkey]= task.task      
        formingtasks = FormingTaskInstance.objects.filter(part__title = part.title)
        for task in formingtasks:
            if task.part.serial == part.serial:
                if task.status != 10:
                    CompleteDict[Partkey]= task.task  
        WCtasks = WireCutTaskInstance.objects.filter(part__title = part.title)
        for task in WCtasks:
            if task.part.serial == part.serial:
                if task.status != 10:
                    CompleteDict[Partkey]= task.task 
        Pitchingtasks = PitchingTaskInstance.objects.filter(part__title = part.title)
        for task in WCtasks:
            if task.part.serial == part.serial:
                if task.status != 10:
                    CompleteDict[Partkey]= task.task 
        HPtasks = HeaderPlateTaskInstance.objects.filter(part__title = part.title)
        for task in HPtasks:
            if task.part.serial == part.serial:
                if task.status != 10:
                    CompleteDict[Partkey]= task.task 
        Deburrtasks = DeburrTaskInstance.objects.filter(part__title = part.title)
        for task in Deburrtasks:
            if task.part.serial == part.serial:
                if task.status != 10:
                    CompleteDict[Partkey]= task.task
        Platingtasks = PlatingTaskInstance.objects.filter(part__title = part.title)
        for task in Platingtasks:
            if task.part.serial == part.serial:
                if task.status != 10:
                    CompleteDict[Partkey]= task.task
                    

    Cores_not_in_Archive = Part.objects.filter(archive__exact = False).count()
    context = {"Parts": Parts,
               "Check_Tasks_Completed": CompleteDict,
               "Cores_not_in_Archive": Cores_not_in_Archive,
               }
    
    return render(request, "final_checks.html", context = context)

class CoreArchiveView(generic.ListView):
    model = Part
    context_object_name = "archive_part_list"
    template_name = "core_archive.html"
    paginate_by = 10
    
    
    
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
def indexer(indexable, i): 
        return indexable[i]   

@register.filter
def get_partNo(serial, key): 
    return key+"s"+serial

@register.filter
def get_item(key, dictionary): 
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
                 if task.status != 10:
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
                     Completedict[task.part] = "Not Complete"
                     
        #Stacking Tasks for each individual part
        partst = None
        StackingCompletedict = {}
        for task in StackingTaskInstance.objects.all():
             if task.part != partst:
                 partst = task.part
                 if task.status != 10:
                     StackingCompletedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
                     StackingCompletedict[task.part] = "Not Complete"
        #Forming Tasks for each individual part
        partfo = None
        FormingCompletedict = {}
        for task in FormingTaskInstance.objects.all():
             if task.part != partfo:
                 partfo = task.part
                 if task.status != 10:
                     FormingCompletedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
                     FormingCompletedict[task.part] = "Not Complete"
                     
        #Wire Cut Tasks for each individual part
        partwc = None
        WCCompletedict = {}
        for task in WireCutTaskInstance.objects.all():
             if task.part != partwc:
                 partwc = task.part
                 if task.status != 10:
                     WCCompletedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
                     WCCompletedict[task.part] = "Not Complete" 
                     
        #Pitching Tasks for each individual part
        partpt = None
        PitchCompletedict = {}
        for task in PitchingTaskInstance.objects.all():
             if task.part != partpt:
                 partpt = task.part
                 if task.status != 10:
                     PitchCompletedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
                     PitchCompletedict[task.part] = "Not Complete" 
                     
        #Hp Machining Tasks for each individual part
        parthp = None
        HPCompletedict = {}
        for task in HeaderPlateTaskInstance.objects.all():
             if task.part != parthp:
                 parthp = task.part
                 if task.status != 10:
                     HPCompletedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
                     HPCompletedict[task.part] = "Not Complete"
                     
        #Deburr Tasks for each individual part
        partdb = None
        DeburrCompletedict = {}
        for task in DeburrTaskInstance.objects.all():
             if task.part != partdb:
                 partdb = task.part
                 if task.status != 10:
                     DeburrCompletedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
                     DeburrCompletedict[task.part] = "Not Complete"
                     
        #Plating Tasks for each individual part
        partpl = None
        PlatingCompletedict = {}
        for task in PlatingTaskInstance.objects.all():
             if task.part != partpl:
                 partpl = task.part
                 if task.status != 10:
                     PlatingCompletedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
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
            try:
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
                Part_Saved.send(sender = part, title = part.title)
                return HttpResponseRedirect(reverse('part-dashboard'))
            except:
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
    
class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team
    fields = '__all__'
    success_url = reverse_lazy('part-create')
    

#Component Prep Classes
class CpTaskListView(generic.ListView):
    model = ComponentPrepTaskInstance
    context_object_name = "cptask_list"
    template_name = "cptask_list.html"
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        num_tasks_not_started = ComponentPrepTaskInstance.objects.filter(status__exact=2, part__archive__exact = False).count()
        tasks_remaining = ComponentPrepTaskInstance.objects.exclude(status__exact=10,part__archive__exact = False).count()
        tasks_complete_count = ComponentPrepTaskInstance.objects.filter(status__exact=10, part__archive__exact = False).count()
        tasks_complete = ComponentPrepTaskInstance.objects.filter(status__exact=10, part__archive__exact = False)
        tasks_on_hold = ComponentPrepTaskInstance.objects.filter(status__exact=3,part__archive__exact = False).count()
        not_archived_tasks = ComponentPrepTaskInstance.objects.exclude(part__archive__exact = True).count()
        tasks_in_progress = ComponentPrepTaskInstance.objects.filter(status__exact=1,part__archive__exact = False)
        tasks_in_progress_count = ComponentPrepTaskInstance.objects.filter(status__exact=1,part__archive__exact = False).count()
        
        tasks_avaliable = ComponentPrepTaskInstance.objects.filter(status__exact=2,part__archive__exact = False)
        tasks_avaliable_count = ComponentPrepTaskInstance.objects.filter(status__exact=2,part__archive__exact = False).count()
        
        tasks_on_hold = ComponentPrepTaskInstance.objects.filter(status__exact=3,part__archive__exact = False)
        tasks_on_hold_count = ComponentPrepTaskInstance.objects.filter(status__exact=3, part__archive__exact = False).count()
        
        context["tasks_on_hold_count"] = tasks_on_hold_count
        context["tasks_on_hold"] = tasks_on_hold      
        context["tasks_avaliable_count"] = tasks_avaliable_count
        context["tasks_avaliable"] = tasks_avaliable
        context["tasks_in_progress_count"] = tasks_in_progress_count
        context["tasks_in_progress"] = tasks_in_progress
        context["not_archived_tasks"] = not_archived_tasks
        context["num_tasks_not_started"] = num_tasks_not_started
        context["tasks_remaining"] = tasks_remaining
        context["tasks_complete"] = tasks_complete
        context["tasks_complete_count"] = tasks_complete_count
        return context
    
class CPTaskDetailView(generic.DetailView):
    model = ComponentPrepTaskInstance
    
class CPTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = ComponentPrepTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('part-dashboard')
    
class CPTaskDelete(LoginRequiredMixin,DeleteView):
    model = ComponentPrepTaskInstance 
    success_url = reverse_lazy('part-dashboard')
    
def StartCPTask(request, pk):
    Task = ComponentPrepTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.status = 1
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
    timetostartstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))

def FinishCPTask(request, pk):
    Task = ComponentPrepTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.finishtime = str_Time
    Task.status = 10
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))
  
#Stacking Classes  
class StackingTaskListView(generic.ListView):
    model = StackingTaskInstance
    context_object_name = "stackingtask_list"
    template_name = "stackingtask/stackingtaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         num_tasks_not_started = StackingTaskInstance.objects.filter(status__exact=2, part__archive__exact = False).count()
         tasks_remaining = StackingTaskInstance.objects.exclude(status__exact=10,part__archive__exact = False).count()
         tasks_complete_count = StackingTaskInstance.objects.filter(status__exact=10, part__archive__exact = False).count()
         tasks_complete = StackingTaskInstance.objects.filter(status__exact=10, part__archive__exact = False)
         tasks_on_hold = StackingTaskInstance.objects.filter(status__exact=3,part__archive__exact = False).count()
         not_archived_tasks = StackingTaskInstance.objects.exclude(part__archive__exact = True).count()
         tasks_in_progress = StackingTaskInstance.objects.filter(status__exact=1,part__archive__exact = False)
         tasks_in_progress_count = StackingTaskInstance.objects.filter(status__exact=1,part__archive__exact = False).count()
            
         tasks_avaliable = StackingTaskInstance.objects.filter(status__exact=2,part__archive__exact = False)
         tasks_avaliable_count = StackingTaskInstance.objects.filter(status__exact=2,part__archive__exact = False).count()
            
         tasks_on_hold = StackingTaskInstance.objects.filter(status__exact=3,part__archive__exact = False)
         tasks_on_hold_count = StackingTaskInstance.objects.filter(status__exact=3, part__archive__exact = False).count()
         part = None
         Completedict = {}
         for task in ComponentPrepTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != 10:
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
                     Completedict[task.part] = "Not Complete"
         
         context["tasks_on_hold_count"] = tasks_on_hold_count
         context["tasks_on_hold"] = tasks_on_hold      
         context["tasks_avaliable_count"] = tasks_avaliable_count
         context["tasks_avaliable"] = tasks_avaliable
         context["tasks_in_progress_count"] = tasks_in_progress_count
         context["tasks_in_progress"] = tasks_in_progress
         context["tasks_complete"] = tasks_complete
         context["tasks_complete_count"] = tasks_complete_count
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
                if task.status != 10:
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != 10:
                    Completedict[task.part] = "Not Complete"
        context["component_prep_tasks_not_completed"] = Completedict
        return context
    
class StackingTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = StackingTaskInstance
    fields = ['status'] 
    
class StackingTaskDelete(LoginRequiredMixin,DeleteView):
    model = StackingTaskInstance 
    success_url = reverse_lazy('part-dashboard')
    

def StartStackTask(request, pk):
    Task = StackingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.status = 1
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
    return HttpResponseRedirect(reverse('part-dashboard'))

def FinishStackTask(request, pk):
    Task = StackingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.finishtime = str_Time
    Task.status = 10
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))    
    

 
# Sheet Metal Forming Classes
class FormingTaskInstanceListView(generic.ListView):
    model = FormingTaskInstance
    context_object_name = "formingtask_list"
    template_name = "formingtask/formingtaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
         
        num_tasks_not_started = FormingTaskInstance.objects.filter(status__exact=2).count()
        tasks_remaining = FormingTaskInstance.objects.exclude(status__exact=10).count()
        tasks_complete_count = FormingTaskInstance.objects.filter(status__exact=10, part__archive__exact = False).count()
        tasks_complete = FormingTaskInstance.objects.filter(status__exact=10, part__archive__exact = False)
        tasks_on_hold = FormingTaskInstance.objects.filter(status__exact=3).count()
        not_archived_tasks = FormingTaskInstance.objects.exclude(part__archive__exact = True).count()
        tasks_in_progress = FormingTaskInstance.objects.filter(status__exact=1).exclude(part__archive__exact = True)
        tasks_in_progress_count = FormingTaskInstance.objects.filter(status__exact=1).exclude(part__archive__exact = True).count()
        
        tasks_avaliable = FormingTaskInstance.objects.filter(status__exact=2).exclude(part__archive__exact = True)
        tasks_avaliable_count = FormingTaskInstance.objects.filter(status__exact=2).exclude(part__archive__exact = True).count()
        
        tasks_on_hold = FormingTaskInstance.objects.filter(status__exact=3).exclude(part__archive__exact = True)
        tasks_on_hold_count = FormingTaskInstance.objects.filter(status__exact=3).exclude(part__archive__exact = True).count()
        
        context["tasks_on_hold_count"] = tasks_on_hold_count
        context["tasks_on_hold"] = tasks_on_hold      
        context["tasks_avaliable_count"] = tasks_avaliable_count
        context["tasks_avaliable"] = tasks_avaliable
        context["tasks_in_progress_count"] = tasks_in_progress_count
        context["tasks_in_progress"] = tasks_in_progress
        context["not_archived_tasks"] = not_archived_tasks
        context["num_tasks_not_started"] = num_tasks_not_started
        context["tasks_remaining"] = tasks_remaining
        context["tasks_complete"] = tasks_complete
        context["tasks_complete_count"] = tasks_complete_count
        return context 
     
class FormingTaskInstanceDetailView(generic.DetailView):
    model = FormingTaskInstance
    
class FormingTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = FormingTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('part-dashboard')
    
class FormingTaskDelete(LoginRequiredMixin,DeleteView):
    model = FormingTaskInstance 
    success_url = reverse_lazy('part-dashboard')
    
def StartFormingTask(request, pk):
    Task = FormingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.status = 1
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
    timetostartstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))

def FinishFormingTask(request, pk):
    Task = FormingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.finishtime = str_Time
    Task.status = 10
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))
    
#Header Plate Views
class HeaderPlateTaskInstanceListView(generic.ListView):
    model = HeaderPlateTaskInstance
    context_object_name = "headerplatetask_list"
    template_name = "headerplatetask/headerplatetaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         tasks_remaining = HeaderPlateTaskInstance.objects.exclude(status__exact=10).count()
         num_tasks_not_started = HeaderPlateTaskInstance.objects.filter(status__exact=2).count()
         part = None
         Completedict = {}
         for task in PitchingTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != 10:
                     Completedict[task.part] = "Not Complete"
             else:
                 if task.status != 10:
                    Completedict[task.part] = "Not Complete"
                    
         tasks_complete_count = HeaderPlateTaskInstance.objects.filter(status__exact=10, part__archive__exact = False).count()
         tasks_complete = HeaderPlateTaskInstance.objects.filter(status__exact=10, part__archive__exact = False)
         tasks_on_hold = HeaderPlateTaskInstance.objects.filter(status__exact=3,part__archive__exact = False).count()
         not_archived_tasks = HeaderPlateTaskInstance.objects.exclude(part__archive__exact = True).count()
         tasks_in_progress = HeaderPlateTaskInstance.objects.filter(status__exact=1,part__archive__exact = False)
         tasks_in_progress_count = HeaderPlateTaskInstance.objects.filter(status__exact=1,part__archive__exact = False).count()
         
         tasks_avaliable = HeaderPlateTaskInstance.objects.filter(status__exact=2,part__archive__exact = False)
         tasks_avaliable_count = HeaderPlateTaskInstance.objects.filter(status__exact=2,part__archive__exact = False).count()
         
         tasks_on_hold = HeaderPlateTaskInstance.objects.filter(status__exact=3,part__archive__exact = False)
         tasks_on_hold_count = HeaderPlateTaskInstance.objects.filter(status__exact=3, part__archive__exact = False).count()
         
         context["tasks_complete"] = tasks_complete
         context["tasks_complete_count"] = tasks_complete_count
         context["tasks_on_hold_count"] = tasks_on_hold_count
         context["tasks_on_hold"] = tasks_on_hold      
         context["tasks_avaliable_count"] = tasks_avaliable_count
         context["tasks_avaliable"] = tasks_avaliable
         context["tasks_in_progress_count"] = tasks_in_progress_count
         context["tasks_in_progress"] = tasks_in_progress
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
    success_url = reverse_lazy('part-dashboard')
    
class HeaderPlateTaskDelete(LoginRequiredMixin,DeleteView):
    model = HeaderPlateTaskInstance 
    success_url = reverse_lazy('part-dashboard')
    
def StartHeaderPlateTask(request, pk):
    Task = HeaderPlateTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.status = 1
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
    timetostartstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))

def FinishHeaderPlateTask(request, pk):
    Task = HeaderPlateTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.finishtime = str_Time
    Task.status = 10
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))

#Pitching Task Views
class PitchingTaskListView(generic.ListView):
    model = PitchingTaskInstance
    context_object_name = "pitchingtask_list"
    template_name = "pitchingtask/pitchingtaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         num_tasks_not_started = PitchingTaskInstance.objects.filter(status__exact=2).count()
         tasks_remaining = PitchingTaskInstance.objects.exclude(status__exact=1).count()
         part = None
         Completedict = {}
         for task in WireCutTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != 10:
                     Completedict[task.part] = "Not Complete"
             else:
                 if task.status != 10:
                    Completedict[task.part] = "Not Complete"
         tasks_complete_count = PitchingTaskInstance.objects.filter(status__exact=10, part__archive__exact = False).count()
         tasks_complete = PitchingTaskInstance.objects.filter(status__exact=10, part__archive__exact = False)
         tasks_on_hold = PitchingTaskInstance.objects.filter(status__exact=3,part__archive__exact = False).count()
         not_archived_tasks = PitchingTaskInstance.objects.exclude(part__archive__exact = True).count()
         tasks_in_progress = PitchingTaskInstance.objects.filter(status__exact=1,part__archive__exact = False)
         tasks_in_progress_count = PitchingTaskInstance.objects.filter(status__exact=1,part__archive__exact = False).count()
         
         tasks_avaliable = PitchingTaskInstance.objects.filter(status__exact=2,part__archive__exact = False)
         tasks_avaliable_count = PitchingTaskInstance.objects.filter(status__exact=2,part__archive__exact = False).count()
         
         tasks_on_hold = PitchingTaskInstance.objects.filter(status__exact=3,part__archive__exact = False)
         tasks_on_hold_count = PitchingTaskInstance.objects.filter(status__exact=3, part__archive__exact = False).count()
         
         context["tasks_complete"] = tasks_complete
         context["tasks_complete_count"] = tasks_complete_count
         context["tasks_on_hold_count"] = tasks_on_hold_count
         context["tasks_on_hold"] = tasks_on_hold      
         context["tasks_avaliable_count"] = tasks_avaliable_count
         context["tasks_avaliable"] = tasks_avaliable
         context["tasks_in_progress_count"] = tasks_in_progress_count
         context["tasks_in_progress"] = tasks_in_progress
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
                if task.status != 10:
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != 10:
                    Completedict[task.part] = "Not Complete"
        context["wire_cut_tasks_not_completed"] = Completedict
        return context
    
class PitchingTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = PitchingTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('part-dashboard')
    
class PitchingTaskDelete(LoginRequiredMixin,DeleteView):
    model = PitchingTaskInstance 
    success_url = reverse_lazy('part-dashboard')
    
def StartPitchingTask(request, pk):
    Task = PitchingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.status = 1
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
    timetostartstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))

def FinishPitchingTask(request, pk):
    Task = PitchingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.finishtime = str_Time
    Task.status = 10
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))


#Wire Cut Task Views
class WireCutTaskListView(generic.ListView):
    model = WireCutTaskInstance
    context_object_name = "wirecuttask_list"
    template_name = "wirecuttask/wirecuttaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         num_tasks_not_started = WireCutTaskInstance.objects.filter(status__exact=2, part__archive__exact = False).count()
         tasks_remaining = WireCutTaskInstance.objects.exclude(status__exact=10, part__archive__exact = False).count()
         part = None
         Completedict = {}
         for task in StackingTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != 10:
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
                     Completedict[task.part] = "Not Complete"
                     
                     
         tasks_complete_count = WireCutTaskInstance.objects.filter(status__exact=10, part__archive__exact = False).count()
         tasks_complete = WireCutTaskInstance.objects.filter(status__exact=10, part__archive__exact = False)
         tasks_on_hold = WireCutTaskInstance.objects.filter(status__exact=3,part__archive__exact = False).count()
         not_archived_tasks = WireCutTaskInstance.objects.exclude(part__archive__exact = True).count()
         tasks_in_progress = WireCutTaskInstance.objects.filter(status__exact=1,part__archive__exact = False)
         tasks_in_progress_count = WireCutTaskInstance.objects.filter(status__exact=1,part__archive__exact = False).count()
         
         tasks_avaliable = WireCutTaskInstance.objects.filter(status__exact=2,part__archive__exact = False)
         tasks_avaliable_count = WireCutTaskInstance.objects.filter(status__exact=2,part__archive__exact = False).count()
         
         tasks_on_hold = WireCutTaskInstance.objects.filter(status__exact=3,part__archive__exact = False)
         tasks_on_hold_count = WireCutTaskInstance.objects.filter(status__exact=3, part__archive__exact = False).count()
         
         context["tasks_complete"] = tasks_complete
         context["tasks_complete_count"] = tasks_complete_count
         context["tasks_on_hold_count"] = tasks_on_hold_count
         context["tasks_on_hold"] = tasks_on_hold      
         context["tasks_avaliable_count"] = tasks_avaliable_count
         context["tasks_avaliable"] = tasks_avaliable
         context["tasks_in_progress_count"] = tasks_in_progress_count
         context["tasks_in_progress"] = tasks_in_progress
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
                if task.status != 10:
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != 10:
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
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.status = 1
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
    timetostartstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))

def FinishWireCutTask(request, pk):
    Task = WireCutTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.finishtime = str_Time
    Task.status = 10
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))


#Deburr Task Views
class DeburrTaskListView(generic.ListView):
    model = DeburrTaskInstance
    context_object_name = "deburrtask_list"
    template_name = "deburrtask/deburrtaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         num_tasks_not_started = DeburrTaskInstance.objects.filter(status__exact=2, part__archive__exact = False).count()
         tasks_remaining = DeburrTaskInstance.objects.exclude(status__exact=10, part__archive__exact = False).count()
         part = None
         Completedict = {}
         for task in HeaderPlateTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != 10:
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
                     Completedict[task.part] = "Not Complete"
                     
                     
         not_archived_tasks = DeburrTaskInstance.objects.exclude(part__archive__exact = True).count()
         tasks_complete_count = DeburrTaskInstance.objects.filter(status__exact=10, part__archive__exact = False).count()
         tasks_complete = DeburrTaskInstance.objects.filter(status__exact=10, part__archive__exact = False)
         tasks_on_hold = DeburrTaskInstance.objects.filter(status__exact=3,part__archive__exact = False).count()
         tasks_in_progress = DeburrTaskInstance.objects.filter(status__exact=1,part__archive__exact = False)
         tasks_in_progress_count = DeburrTaskInstance.objects.filter(status__exact=1,part__archive__exact = False).count()
         
         tasks_avaliable = DeburrTaskInstance.objects.filter(status__exact=2,part__archive__exact = False)
         tasks_avaliable_count = DeburrTaskInstance.objects.filter(status__exact=2,part__archive__exact = False).count()
         
         tasks_on_hold = DeburrTaskInstance.objects.filter(status__exact=3,part__archive__exact = False)
         tasks_on_hold_count = DeburrTaskInstance.objects.filter(status__exact=3, part__archive__exact = False).count()
         
         context["tasks_complete"] = tasks_complete
         context["tasks_complete_count"] = tasks_complete_count
         context["tasks_on_hold_count"] = tasks_on_hold_count
         context["tasks_on_hold"] = tasks_on_hold      
         context["tasks_avaliable_count"] = tasks_avaliable_count
         context["tasks_avaliable"] = tasks_avaliable
         context["tasks_in_progress_count"] = tasks_in_progress_count
         context["tasks_in_progress"] = tasks_in_progress
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
                if task.status != 10:
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != 10:
                    Completedict[task.part] = "Not Complete"
        context["header_plate_tasks_not_completed"] = Completedict
        return context
    
class DeburrTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = DeburrTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('part-dashboard')
    
class DeburrTaskDelete(LoginRequiredMixin,DeleteView):
    model = DeburrTaskInstance
    success_url = reverse_lazy('part-dashboard')
    
def StartDeburrTask(request, pk):
    Task = DeburrTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.status = 1
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
    timetostartstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))

def FinishDeburrTask(request, pk):
    Task = DeburrTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.finishtime = str_Time
    Task.status = 10
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))

#Plating Task Views
class PlatingTaskListView(generic.ListView):
    model = PlatingTaskInstance
    context_object_name = "platingtask_list"
    template_name = "platingtask/platingtaskinstance_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         num_tasks_not_started = PlatingTaskInstance.objects.filter(status__exact=2, part__archive__exact = False).count()
         tasks_remaining = PlatingTaskInstance.objects.exclude(status__exact=10, part__archive__exact = False).count()
         part = None
         Completedict = {}
         for task in DeburrTaskInstance.objects.all():
             if task.part != part:
                 part = task.part
                 if task.status != 10:
                     Completedict[task.part] = "Not Complete"
             else:
                if task.status != 10:
                     Completedict[task.part] = "Not Complete"
                     
         not_archived_tasks = PlatingTaskInstance.objects.exclude(part__archive__exact = True).count()
         tasks_complete_count = PlatingTaskInstance.objects.filter(status__exact=10, part__archive__exact = False).count()
         tasks_complete = PlatingTaskInstance.objects.filter(status__exact=10, part__archive__exact = False)
         tasks_on_hold = PlatingTaskInstance.objects.filter(status__exact=3,part__archive__exact = False).count()
         tasks_in_progress = PlatingTaskInstance.objects.filter(status__exact=1,part__archive__exact = False)
         tasks_in_progress_count = PlatingTaskInstance.objects.filter(status__exact=1,part__archive__exact = False).count()
         
         tasks_avaliable = PlatingTaskInstance.objects.filter(status__exact=2,part__archive__exact = False)
         tasks_avaliable_count = PlatingTaskInstance.objects.filter(status__exact=2,part__archive__exact = False).count()
         
         tasks_on_hold = PlatingTaskInstance.objects.filter(status__exact=3,part__archive__exact = False)
         tasks_on_hold_count = PlatingTaskInstance.objects.filter(status__exact=3, part__archive__exact = False).count()
         
         context["tasks_complete"] = tasks_complete
         context["tasks_complete_count"] = tasks_complete_count
         context["tasks_on_hold_count"] = tasks_on_hold_count
         context["tasks_on_hold"] = tasks_on_hold      
         context["tasks_avaliable_count"] = tasks_avaliable_count
         context["tasks_avaliable"] = tasks_avaliable
         context["tasks_in_progress_count"] = tasks_in_progress_count
         context["tasks_in_progress"] = tasks_in_progress
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
                if task.status != 10:
                    Completedict[task.part] = "Not Complete"
            else:
                if task.status != 10:
                    Completedict[task.part] = "Not Complete"
        context["deburr_tasks_not_completed"] = Completedict
        return context
    
class PlatingTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = PlatingTaskInstance
    fields = ['status'] 
    success_url = reverse_lazy('part-dashboard')
    
class PlatingTaskDelete(LoginRequiredMixin,DeleteView):
    model = PlatingTaskInstance
    success_url = reverse_lazy('part-dashboard')
    
def StartPlatingTask(request, pk):
    Task = PlatingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.status = 1
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
    timetostartstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetostart = str(timetostartstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))

def FinishPlatingTask(request, pk):
    Task = PlatingTaskInstance.objects.get(pk = pk)
    str_Time = datetime.datetime.now()
    str_Time = str_Time.strftime("%X")+" on the "+str_Time.strftime("%d/%m/%Y")
    Task.finishtime = str_Time
    Task.status = 10
    Task.finishtimenum = time.time()
    start = float(Task.starttimenum)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    if hours > 24:
        days, extra = divmod(hours,24)
    else:
        days = 0
    mins, seconds = divmod(rem, 60)
    timetakenstr = "{:0>2} days- {:0>2} hours, {:0>2} minutes, {:05.2f} seconds".format(int(days),int(hours),int(mins),seconds)
    Task.timetaken = str(timetakenstr)
    Task.save()
    return HttpResponseRedirect(reverse('part-dashboard'))

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
    
