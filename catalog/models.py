from django.db import models
from django.urls import reverse # generate urls' by reversing url patterns
import uuid #Required for unique book instances
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Case, When, Value
import time
import datetime

class Deburr_Task(models.Model):
    """
    Model for the required sheet metal forming tasks on the press:
    """
    title = models.CharField(max_length = 100, null = True)
    
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
class DeburrTaskInstance(models.Model):
    """
    Model for representing multiple sheet metal forming tasks required to be
    completed
    """
    task = models.CharField(max_length = 100, null = True)
    part = models.ForeignKey("Part", on_delete=models.CASCADE, null = True)
    TASK_STATUS = ((2,"Not Started"),(3, "On Hold"),(10, "Complete"),
                   (1, "In Progress"))
    status = models.IntegerField(choices = TASK_STATUS, 
                              blank = False, default = 2,
                              help_text = "Set task completion status")
    #Create Time String and decimal fields
    createtime = models.CharField(max_length = 50, null = True, blank = True)
    createtimenum = models.DecimalField(decimal_places=2, max_digits=14, null=True, blank = True)
    #Start Time String and decimal fields
    starttime = models.CharField(max_length = 50, null = True, blank = True)
    starttimenum = models.DecimalField(decimal_places=2,max_digits=14,null=True, blank = True)
    #Time to start string feild
    timetostart = models.CharField(max_length = 50,null=True, blank = True)
    #Finish Time String field
    finishtime = models.CharField(max_length = 50, null = True, blank = True)
    #Time taken str field
    timetaken = models.CharField(max_length = 50,null=True, blank = True)
    class Meta:
        ordering = ['part','status']

    def __str__(self):
        """String for Representing the model object (on admin site)"""
        return self.task
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this task."""
        return reverse('deburrtask-detail', args = [str(self.id)])
    
class Plating_Task(models.Model):
    """
    Model for the required sheet metal forming tasks on the press:
    """
    title = models.CharField(max_length = 100, null = True)
    
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
class PlatingTaskInstance(models.Model):
    """
    Model for representing multiple sheet metal forming tasks required to be
    completed
    """
    task = models.CharField(max_length = 100, null = True)
    part = models.ForeignKey("Part", on_delete=models.CASCADE, null = True)
    TASK_STATUS = ((2,"Not Started"),(3, "On Hold"),(10, "Complete"),
                   (1, "In Progress"))
    status = models.IntegerField(choices = TASK_STATUS, 
                              blank = False, default = 2,
                              help_text = "Set task completion status")
    #Create Time String and decimal fields
    createtime = models.CharField(max_length = 50, null = True, blank = True)
    createtimenum = models.DecimalField(decimal_places=2, max_digits=14, null=True, blank = True)
    #Start Time String and decimal fields
    starttime = models.CharField(max_length = 50, null = True, blank = True)
    starttimenum = models.DecimalField(decimal_places=2,max_digits=14,null=True, blank = True)
    #Time to start string feild
    timetostart = models.CharField(max_length = 50,null=True, blank = True)
    #Finish Time String field
    finishtime = models.CharField(max_length = 50, null = True, blank = True)
    #Time taken str field
    timetaken = models.CharField(max_length = 50,null=True, blank = True)    
    class Meta:
        ordering = ['part','status']

    def __str__(self):
        """String for Representing the model object (on admin site)"""
        return self.task
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this task."""
        return reverse('platingtask-detail', args = [str(self.id)])

class Wire_Cut_Task(models.Model):
    """
    Model for the required sheet metal forming tasks on the press:
    """
    title = models.CharField(max_length = 100, null = True)
    
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
class WireCutTaskInstance(models.Model):
    """
    Model for representing multiple sheet metal forming tasks required to be
    completed
    """
    task = models.CharField(max_length = 100, null = True)
    part = models.ForeignKey("Part", on_delete=models.CASCADE, null = True)
    TASK_STATUS = ((2,"Not Started"),(3, "On Hold"),(10, "Complete"),
                   (1, "In Progress"))
    status = models.IntegerField(choices = TASK_STATUS, 
                              blank = False, default = 2,
                              help_text = "Set task completion status")
    createtime = models.CharField(max_length = 50, null = True, blank = True)
    createtimenum = models.DecimalField(decimal_places=2, max_digits=14, null=True, blank = True)
    #Start Time String and decimal fields
    starttime = models.CharField(max_length = 50, null = True, blank = True)
    starttimenum = models.DecimalField(decimal_places=2,max_digits=14,null=True, blank = True)
    #Time to start string feild
    timetostart = models.CharField(max_length = 50,null=True, blank = True)
    #Finish Time String field
    finishtime = models.CharField(max_length = 50, null = True, blank = True)
    #Time taken str field
    timetaken = models.CharField(max_length = 50,null=True, blank = True)
    class Meta:
        ordering = ['part','status']

    def __str__(self):
        """String for Representing the model object (on admin site)"""
        return self.task
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this task."""
        return reverse('wirecuttask-detail', args = [str(self.id)])


class Pitching_Task(models.Model):
    """
    Model for the required sheet metal forming tasks on the press:
    """
    title = models.CharField(max_length = 100, null = True)
    
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
class PitchingTaskInstance(models.Model):
    """
    Model for representing multiple sheet metal forming tasks required to be
    completed
    """
    task = models.CharField(max_length = 100, null = True)
    part = models.ForeignKey("Part", on_delete=models.CASCADE, null = True)
    TASK_STATUS = ((2,"Not Started"),(3, "On Hold"),(10, "Complete"),
                   (1, "In Progress"))
    status = models.IntegerField(choices = TASK_STATUS, 
                              blank = False, default = 2,
                              help_text = "Set task completion status")
    createtime = models.CharField(max_length = 50, null = True, blank = True)
    createtimenum = models.DecimalField(decimal_places=2, max_digits=14, null=True, blank = True)
    #Start Time String and decimal fields
    starttime = models.CharField(max_length = 50, null = True, blank = True)
    starttimenum = models.DecimalField(decimal_places=2,max_digits=14,null=True, blank = True)
    #Time to start string feild
    timetostart = models.CharField(max_length = 50,null=True, blank = True)
    #Finish Time String field
    finishtime = models.CharField(max_length = 50, null = True, blank = True)
    #Time taken str field
    timetaken = models.CharField(max_length = 50,null=True, blank = True)    
    class Meta:
        ordering = ['part','status']

    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.task
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this task."""
        return reverse('pitchingtask-detail', args = [str(self.id)])



class Forming_Task(models.Model):
    """
    Model for the required sheet metal forming tasks on the press:
    """
    title = models.CharField(max_length = 100, null = True)
    
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
class FormingTaskInstance(models.Model):
    """
    Model for representing multiple sheet metal forming tasks required to be
    completed
    """
    task = models.CharField(max_length = 100, null = True)
    part = models.ForeignKey("Part", on_delete=models.CASCADE, null = True)
    TASK_STATUS = ((2,"Not Started"),(3, "On Hold"),(10, "Complete"),
                   (1, "In Progress"))
    status = models.IntegerField(choices = TASK_STATUS, 
                              blank = False, default = 2,
                              help_text = "Set task completion status")
    #Create Time String and decimal fields
    createtime = models.CharField(max_length = 50, null = True, blank = True)
    createtimenum = models.DecimalField(decimal_places=2, max_digits=14, null=True, blank = True)
    #Start Time String and decimal fields
    starttime = models.CharField(max_length = 50, null = True, blank = True)
    starttimenum = models.DecimalField(decimal_places=2,max_digits=14,null=True, blank = True)
    #Time to start string feild
    timetostart = models.CharField(max_length = 50,null=True, blank = True)
    #Finish Time String field
    finishtime = models.CharField(max_length = 50, null = True, blank = True)
    #Time taken str field
    timetaken = models.CharField(max_length = 50,null=True, blank = True)
    
    class Meta:
        ordering = ['part','status']

    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.task
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this task."""
        return reverse('formingtask-detail', args = [str(self.id)])
    
class Stacking_Task(models.Model):
    """Model representing the multiple stacking tasks that must be 
    completed for a part to be finished"""
    title = models.CharField(max_length = 100, help_text = " Name of a\
                             component prep task")
    description = models.TextField(max_length = 1000, help_text = "Task\
                                   description to aid new employees", null=True,
                                   blank = True)
        
    order = models.IntegerField(null=True)
    
    class Meta:
        ordering = ['order']
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
    
class StackingTaskInstance(models.Model):
    """ Instance of a specific component prep task"""
    task = models.CharField(max_length= 100, null = True)
    part = models.ForeignKey("Part",on_delete=models.CASCADE, null=True)
    TASK_STATUS = ((2,"Not Started"),(3, "On Hold"),(10, "Complete"),
                   (1, "In Progress"))
    
    status = models.IntegerField(choices= TASK_STATUS, 
                              blank = False, default = 2, help_text = "Set \
                                  task completion status")
    createtime = models.CharField(max_length = 50, null = True, blank = True)
    createtimenum = models.DecimalField(decimal_places=2, max_digits=14, null=True, blank = True)
    #Start Time String and decimal fields
    starttime = models.CharField(max_length = 50, null = True, blank = True)
    starttimenum = models.DecimalField(decimal_places=2,max_digits=14,null=True, blank = True)
    #Time to start string feild
    timetostart = models.CharField(max_length = 50,null=True, blank = True)
    #Finish Time String field
    finishtime = models.CharField(max_length = 50, null = True, blank = True)
    #Time taken str field
    timetaken = models.CharField(max_length = 50,null=True, blank = True)
    class Meta:
        ordering = ['part','status']
        
    def __str__(self):
        """string for representing the Model object."""
        return self.task
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this task."""
        return reverse('stackingtask-detail', args = [str(self.id)])
    
class Component_Prep_Task(models.Model):
    """Model representing the multiple component prep tasks that must be 
    completed for a part to be finished"""
    title = models.CharField(max_length = 100, help_text = " Name of a\
                             component prep task")
    description = models.TextField(max_length = 1000, help_text = "Task\
                                   description to aid new employees", null=True,
                                   blank = True)
    order = models.IntegerField(null=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
class ComponentPrepTaskInstance(models.Model):
    """ Instance of a specific component prep task"""
    task = models.CharField(max_length= 100, null = True)
    part = models.ForeignKey("Part",on_delete=models.CASCADE, null=True)
    TASK_STATUS = ((2,"Not Started"),(3, "On Hold"),(10, "Complete"),
                   (1, "In Progress"))
    
    status = models.IntegerField(choices= TASK_STATUS, 
                              blank = False, default = 2, help_text = "Set \
                                  task completion status")
    #Create Time String and decimal fields
    createtime = models.CharField(max_length = 50, null = True, blank = True)
    createtimenum = models.DecimalField(decimal_places=2, max_digits=14, null=True, blank = True)
    #Start Time String and decimal fields
    starttime = models.CharField(max_length = 50, null = True, blank = True)
    starttimenum = models.DecimalField(decimal_places=2,max_digits=14,null=True, blank = True)
    #Time to start string feild
    timetostart = models.CharField(max_length = 50,null=True, blank = True)
    #Finish Time String field
    finishtime = models.CharField(max_length = 50, null = True, blank = True)
    #Time taken str field
    timetaken = models.CharField(max_length = 50,null=True, blank = True)
    class Meta:
        ordering = ['part','status']
        
        
    def __str__(self):
        """string for representing the Model object."""
        return self.task
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this task."""
        return reverse('cptask-detail', args = [str(self.id)])
    
class Team(models.Model):
    """ Model to Represent teams"""
    title = models.CharField(max_length = 100, null = True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
    
class Part(models.Model):
    """ Model represents a Part to be completed"""
    title = models.CharField(max_length = 100)
    serial = models.CharField(max_length = 20,null = True)
    CORE_TYPES = (("Radiator", "Radiator"), ("Intercooler", "Intercooler"),
                  ("Oilcooler", "Oilcooler"),("ERS cooler", "ERS cooler"))
    core_type = models.CharField(choices = CORE_TYPES, max_length = 40, blank = False,
                                 default = "Rad", help_text = "Set Core Type")
    Work_Order = models.CharField(max_length = 6, null = True, help_text= "Define Work Order No")
    team = models.ForeignKey(Team, on_delete = models.RESTRICT, null = True)
    Component_Prep_tasks = models.ManyToManyField(Component_Prep_Task, help_text = "Select \
                                     the component prep tasks \
                                         to be completed.",
                                         blank = True) 
    Stacking_tasks = models.ManyToManyField(Stacking_Task, help_text = "Select\
                                         the required stacking tasks.",
                                         blank = True)
    Forming_tasks = models.ManyToManyField(Forming_Task, help_text = "Select\
                                           the required forming tasks.",
                                         blank = True)
    Header_Plate_tasks = models.ManyToManyField("Header_Plate_Task", help_text = "\
                                                Select The nessessary header \
                                                    plate tasks",
                                         blank = True)
    Pitching_tasks = models.ManyToManyField(Pitching_Task, help_text = "\
                                            Select the nessessary pitching \
                                                tasks",
                                         blank = True)
    Wire_Cut_tasks = models.ManyToManyField(Wire_Cut_Task, help_text = "\
                                            Select the nessessary wire cut\
                                                tasks",
                                         blank = True)
    Deburr_tasks = models.ManyToManyField(Deburr_Task, help_text = "\
                                            Select the nessessary deburr\
                                                tasks",
                                         blank = True)
    Plating_tasks = models.ManyToManyField(Plating_Task, help_text = "\
                                            Select the nessessary plating\
                                                tasks",
                                         blank = True)
    pub_date = models.DateTimeField("time published", auto_now=True)
    priority = models.IntegerField(null=True, default = 30, help_text = "\
                                            Select the nessessary priority\
                                                ")
    
    archive = models.BooleanField(null = True, default=False)
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a sepecfic author instance."""
        return reverse("part-detail", args=[str(self.id)])
    
    
    
    class Meta:
        ordering = ['priority','title','serial']
    
class Header_Plate_Task(models.Model):
    """Model representing the required Header Plate Tasks"""
    title = models.CharField(max_length = 100, help_text = "Enter the Name\
                     of a header plate machining task")
    order = models.IntegerField(null=True)
    
    class Meta:
        ordering = ['order']
                     
    def __str__(self):
        """string for representing the Model object."""
        return self.title
                     
class HeaderPlateTaskInstance(models.Model):
    """Model representing the multiple instances of a header plate task"""
    task = models.CharField(max_length = 100, null = True)
    part = models.ForeignKey("Part", on_delete = models.CASCADE,null = True)
    TASK_STATUS = ((2,"Not Started"),(3, "On Hold"),(10, "Complete"),
                   (1, "In Progress"))
    
    status = models.IntegerField(choices= TASK_STATUS, 
                              blank = False, default = "a", help_text = "Set \
                                  task completion status")
    #Create Time String and decimal fields
    createtime = models.CharField(max_length = 50, null = True, blank = True)
    createtimenum = models.DecimalField(decimal_places=2, max_digits=14, null=True, blank = True)
    #Start Time String and decimal fields
    starttime = models.CharField(max_length = 50, null = True, blank = True)
    starttimenum = models.DecimalField(decimal_places=2,max_digits=14,null=True, blank = True)
    #Time to start string feild
    timetostart = models.CharField(max_length = 50,null=True, blank = True)
    #Finish Time String field
    finishtime = models.CharField(max_length = 50, null = True, blank = True)
    #Time taken str field
    timetaken = models.CharField(max_length = 50,null=True, blank = True)
    class Meta:
        ordering = ['part','status']
        
    def __str__(self):
        """string for representing the Model object."""
        return self.task
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this task."""
        return reverse('hptask-detail', args = [str(self.id)])                          
                        
    
# Create Sheet Metal Forming Tasks
@receiver(m2m_changed, sender = Part.Forming_tasks.through)
def CreateNewFormingTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    Formingtask_list = obj.Forming_tasks.all()
    Created_Time = datetime.datetime.now()
    Created_Time = Created_Time.strftime("%X")+" on the "+Created_Time.strftime("%d/%m/%Y")
    for task in Formingtask_list:
       try:
           FormingTaskInstance.objects.get(task= task, part=obj)
       except:
           FormingTaskInstance.objects.create(task= task, part=obj, status=2, createtime = Created_Time, createtimenum = time.time())
           
    #Delete excess tasks if requested on update
    RequestedTaskList = Formingtask_list
    CurrentTaskList = FormingTaskInstance.objects.filter(part=obj)
    list1 = []
    list2 = []
    for task in CurrentTaskList.values_list():
        list1.append(task[1])
    for task in RequestedTaskList.values_list():
        list2.append(task[1])
    for task in list1:
        if task in list2:
            pass
        else:
            FormingTaskInstance.objects.filter(task= task, part = obj).delete()
            
            
# Create Component Prep Tasks  
@receiver(m2m_changed, sender = Part.Component_Prep_tasks.through)
def CreateNewCPTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    CPtask_list = obj.Component_Prep_tasks.all()
    Created_Time = datetime.datetime.now()
    Created_Time = Created_Time.strftime("%X")+" on the "+Created_Time.strftime("%d/%m/%Y")
    for task in CPtask_list:
       try:
           ComponentPrepTaskInstance.objects.get(task= task, part=obj)
       except:
           ComponentPrepTaskInstance.objects.create(task= task, part=obj, status=2, createtime = Created_Time, createtimenum = time.time())
           
    #Delete excess tasks if requested on update
    RequestedTaskList = CPtask_list
    CurrentTaskList = ComponentPrepTaskInstance.objects.filter(part=obj)
    list1 = []
    list2 = []
    for task in CurrentTaskList.values_list():
        list1.append(task[1])
    for task in RequestedTaskList.values_list():
        list2.append(task[1])
    for task in list1:
        if task in list2:
            pass
        else:
            ComponentPrepTaskInstance.objects.filter(task= task, part = obj).delete()
            
        

# Create Stacking Tasks
@receiver(m2m_changed, sender = Part.Stacking_tasks.through)
def CreateNewStackingTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    Stacktask_list = obj.Stacking_tasks.all()
    Created_Time = datetime.datetime.now()
    Created_Time = Created_Time.strftime("%X")+" on the "+Created_Time.strftime("%d/%m/%Y")
    for task in Stacktask_list:
        try:
            StackingTaskInstance.objects.get(task = task, part = obj)
        except:
            StackingTaskInstance.objects.create(task = task, part = obj, status = 2, createtime = Created_Time, createtimenum = time.time())
            
    #Delete excess tasks if requested on update
    RequestedTaskList = Stacktask_list
    CurrentTaskList = StackingTaskInstance.objects.filter(part=obj)
    list1 = []
    list2 = []
    for task in CurrentTaskList.values_list():
        list1.append(task[1])
    for task in RequestedTaskList.values_list():
        list2.append(task[1])
    for task in list1:
        if task in list2:
            pass
        else:
            StackingTaskInstance.objects.filter(task= task, part = obj).delete()
            
# Create Header Plate Machining Tasks
@receiver(m2m_changed, sender = Part.Header_Plate_tasks.through)
def CreateNewHeaderPlateTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    HPtask_list = obj.Header_Plate_tasks.all()
    Created_Time = datetime.datetime.now()
    Created_Time = Created_Time.strftime("%X")+" on the "+Created_Time.strftime("%d/%m/%Y")
    for task in HPtask_list:
        try:
            HeaderPlateTaskInstance.objects.get(task = task, part = obj)
        except:
            HeaderPlateTaskInstance.objects.create(task = task, part = obj, status = 2, createtime = Created_Time, createtimenum = time.time())
    
    #Delete excess tasks if requested on update
    RequestedTaskList = HPtask_list
    CurrentTaskList = HeaderPlateTaskInstance.objects.filter(part=obj)
    list1 = []
    list2 = []
    for task in CurrentTaskList.values_list():
        list1.append(task[1])
    for task in RequestedTaskList.values_list():
        list2.append(task[1])
    for task in list1:
        if task in list2:
            pass
        else:
            HeaderPlateTaskInstance.objects.filter(task= task, part = obj).delete()
            
# Create Pitching Tasks
@receiver(m2m_changed, sender = Part.Pitching_tasks.through)
def CreateNewPitchingTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    Pitchingtask_list = obj.Pitching_tasks.all()
    Created_Time = datetime.datetime.now()
    Created_Time = Created_Time.strftime("%X")+" on the "+Created_Time.strftime("%d/%m/%Y")
    for task in Pitchingtask_list:
        try:
            PitchingTaskInstance.objects.get(task = task, part = obj)
        except:
            PitchingTaskInstance.objects.create(task = task, part = obj, status = 2, createtime = Created_Time, createtimenum = time.time())
    
    #Delete excess tasks if requested on update
    RequestedTaskList = Pitchingtask_list
    CurrentTaskList = PitchingTaskInstance.objects.filter(part=obj)
    list1 = []
    list2 = []
    for task in CurrentTaskList.values_list():
        list1.append(task[1])
    for task in RequestedTaskList.values_list():
        list2.append(task[1])
    for task in list1:
        if task in list2:
            pass
        else:
            PitchingTaskInstance.objects.filter(task= task, part = obj).delete()
            
# Create WireCut Tasks
@receiver(m2m_changed, sender = Part.Wire_Cut_tasks.through)
def CreateNewWireCutTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    WireCuttask_list = obj.Wire_Cut_tasks.all()
    Created_Time = datetime.datetime.now()
    Created_Time = Created_Time.strftime("%X")+" on the "+Created_Time.strftime("%d/%m/%Y")
    for task in WireCuttask_list:
        try:
            WireCutTaskInstance.objects.get(task = task, part = obj)
        except:
            WireCutTaskInstance.objects.create(task = task, part = obj, status = 2, createtime = Created_Time, createtimenum = time.time())
            
    #Delete excess tasks if requested on update
    RequestedTaskList = WireCuttask_list
    CurrentTaskList = WireCutTaskInstance.objects.filter(part=obj)
    list1 = []
    list2 = []
    for task in CurrentTaskList.values_list():
        list1.append(task[1])
    for task in RequestedTaskList.values_list():
        list2.append(task[1])
    for task in list1:
        if task in list2:
            pass
        else:
            WireCutTaskInstance.objects.filter(task= task, part = obj).delete()
            
# Create Deburr Tasks
@receiver(m2m_changed, sender = Part.Deburr_tasks.through)
def CreateNewDeburrTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    Deburrtask_list = obj.Deburr_tasks.all()
    Created_Time = datetime.datetime.now()
    Created_Time = Created_Time.strftime("%X")+" on the "+Created_Time.strftime("%d/%m/%Y")
    for task in Deburrtask_list:
        try:
            DeburrTaskInstance.objects.get(task = task, part = obj)
        except:
            DeburrTaskInstance.objects.create(task = task, part = obj, status = 2, createtime = Created_Time, createtimenum = time.time())
            
    #Delete excess tasks if requested on update
    RequestedTaskList = Deburrtask_list
    CurrentTaskList = DeburrTaskInstance.objects.filter(part=obj)
    list1 = []
    list2 = []
    for task in CurrentTaskList.values_list():
        list1.append(task[1])
    for task in RequestedTaskList.values_list():
        list2.append(task[1])
    for task in list1:
        if task in list2:
            pass
        else:
            DeburrTaskInstance.objects.filter(task= task, part = obj).delete()       
            
# Create Plating Tasks
@receiver(m2m_changed, sender = Part.Plating_tasks.through)
def CreateNewPlatingTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    Platingtask_list = obj.Plating_tasks.all()
    Created_Time = datetime.datetime.now()
    Created_Time = Created_Time.strftime("%X")+" on the "+Created_Time.strftime("%d/%m/%Y")
    for task in Platingtask_list:
        try:
            PlatingTaskInstance.objects.get(task = task, part = obj)
        except:
            PlatingTaskInstance.objects.create(task = task, part = obj, status = 2, createtime = Created_Time, createtimenum = time.time())
            
    #Delete excess tasks if requested on update
    RequestedTaskList = Platingtask_list
    CurrentTaskList = PlatingTaskInstance.objects.filter(part=obj)
    list1 = []
    list2 = []
    for task in CurrentTaskList.values_list():
        list1.append(task[1])
    for task in RequestedTaskList.values_list():
        list2.append(task[1])
    for task in list1:
        if task in list2:
            pass
        else:
            PlatingTaskInstance.objects.filter(task= task, part = obj).delete()  