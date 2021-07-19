from django.db import models
from django.urls import reverse # generate urls' by reversing url patterns
import uuid #Required for unique book instances
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Case, When, Value

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
    TASK_STATUS = (("a","Not Started"),("h", "On Hold"),("z", "Complete"),
                   ("b", "In Progress"))
    status = models.CharField(max_length = 1, choices = TASK_STATUS, 
                              blank = False, default = "a",
                              help_text = "Set task completion status")
    
    class Meta:
        ordering = ['status']

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
    TASK_STATUS = (("a","Not Started"),("h", "On Hold"),("z", "Complete"),
                   ("b", "In Progress"))
    status = models.CharField(max_length = 1, choices = TASK_STATUS, 
                              blank = False, default = "a",
                              help_text = "Set task completion status")
    
    class Meta:
        ordering = ['status']

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
    TASK_STATUS = (("a","Not Started"),("h", "On Hold"),("z", "Complete"),
                   ("b", "In Progress"))
    status = models.CharField(max_length = 1, choices = TASK_STATUS, 
                              blank = False, default = "a",
                              help_text = "Set task completion status")
    
    class Meta:
        ordering = ['status']

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
    TASK_STATUS = (("a","Not Started"),("h", "On Hold"),("z", "Complete"),
                   ("b", "In Progress"))
    status = models.CharField(max_length = 1, choices = TASK_STATUS, 
                              blank = False, default = "a",
                              help_text = "Set task completion status")
    
    class Meta:
        ordering = ['status']

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
    TASK_STATUS = (("a","Not Started"),("h", "On Hold"),("z", "Complete"),
                   ("b", "In Progress"))
    status = models.CharField(max_length = 1, choices = TASK_STATUS, 
                              blank = False, default = "a",
                              help_text = "Set task completion status")
    
    class Meta:
        ordering = ['status']

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
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
    
class StackingTaskInstance(models.Model):
    """ Instance of a specific component prep task"""
    task = models.CharField(max_length= 100, null = True)
    part = models.ForeignKey("Part",on_delete=models.CASCADE, null=True)
    TASK_STATUS = (("a","Not Started"),("h", "On Hold"),("z", "Complete"),
                   ("b", "In Progress"))
    
    status = models.CharField(max_length = 1, choices= TASK_STATUS, 
                              blank = False, default = "a", help_text = "Set \
                                  task completion status")
    class Meta:
        ordering = ['status']
        
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
    
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
class ComponentPrepTaskInstance(models.Model):
    """ Instance of a specific component prep task"""
    task = models.CharField(max_length= 100, null = True)
    part = models.ForeignKey("Part",on_delete=models.CASCADE, null=True)
    TASK_STATUS = (("a","Not Started"),("h", "On Hold"),("z", "Complete"),
                   ("b", "In Progress"))
    
    status = models.CharField(max_length = 1, choices= TASK_STATUS, 
                              blank = False, default = "a", help_text = "Set \
                                  task completion status")
    class Meta:
        ordering = ['status']
        
        
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
    serial = models.IntegerField(null = True)
    team = models.ForeignKey(Team, on_delete = models.RESTRICT, null = True)
    Component_Prep_tasks = models.ManyToManyField(Component_Prep_Task, help_text = "Select \
                                     the component prep tasks \
                                         to be completed.") 
    Stacking_tasks = models.ManyToManyField(Stacking_Task, help_text = "Select\
                                         the required stacking tasks.")
    Forming_tasks = models.ManyToManyField(Forming_Task, help_text = "Select\
                                           the required forming tasks.")
    Header_Plate_tasks = models.ManyToManyField("Header_Plate_Task", help_text = "\
                                                Select The nessessary header \
                                                    plate tasks")
    Pitching_tasks = models.ManyToManyField(Pitching_Task, help_text = "\
                                            Select the nessessary pitching \
                                                tasks")
    Wire_Cut_tasks = models.ManyToManyField(Wire_Cut_Task, help_text = "\
                                            Select the nessessary wire cut\
                                                tasks")
    Deburr_tasks = models.ManyToManyField(Deburr_Task, help_text = "\
                                            Select the nessessary deburr\
                                                tasks")
    Plating_tasks = models.ManyToManyField(Plating_Task, help_text = "\
                                            Select the nessessary plating\
                                                tasks")
    pub_date = models.DateTimeField("time published", default = timezone.now)
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a sepecfic author instance."""
        return reverse("part-detail", args=[str(self.id)])
    
    class Meta:
        ordering = ['title','serial']
    
class Header_Plate_Task(models.Model):
    """Model representing the required Header Plate Tasks"""
    title = models.CharField(max_length = 100, help_text = "Enter the Name\
                     of a header plate machining task")
                     
    def __str__(self):
        """string for representing the Model object."""
        return self.title
                     
class HeaderPlateTaskInstance(models.Model):
    """Model representing the multiple instances of a header plate task"""
    task = models.CharField(max_length = 100, null = True)
    part = models.ForeignKey("Part", on_delete = models.CASCADE,null = True)
    TASK_STATUS = (("a","Not Started"),("h", "On Hold"),("z", "Complete"),
                   ("b", "In Progress"))
    
    status = models.CharField(max_length = 1, choices= TASK_STATUS, 
                              blank = False, default = "a", help_text = "Set \
                                  task completion status")
    class Meta:
        ordering = ['status']
        
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
    for task in Formingtask_list:
       try:
           FormingTaskInstance.objects.get(task= task, part=obj)
       except:
           FormingTaskInstance.objects.create(task= task, part=obj, status="a")
           
# Create Component Prep Tasks  
@receiver(m2m_changed, sender = Part.Component_Prep_tasks.through)
def CreateNewCPTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    CPtask_list = obj.Component_Prep_tasks.all()
    for task in CPtask_list:
       try:
           ComponentPrepTaskInstance.objects.get(task= task, part=obj)
       except:
           ComponentPrepTaskInstance.objects.create(task= task, part=obj, status="a")

# Create Stacking Tasks
@receiver(m2m_changed, sender = Part.Stacking_tasks.through)
def CreateNewStackingTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    Stacktask_list = obj.Stacking_tasks.all()
    for task in Stacktask_list:
        try:
            StackingTaskInstance.objects.get(task = task, part = obj)
        except:
            StackingTaskInstance.objects.create(task = task, part = obj, status = "a")
            
# Create Header Plate Machining Tasks
@receiver(m2m_changed, sender = Part.Header_Plate_tasks.through)
def CreateNewHeaderPlateTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    HPtask_list = obj.Header_Plate_tasks.all()
    for task in HPtask_list:
        try:
            HeaderPlateTaskInstance.objects.get(task = task, part = obj)
        except:
            HeaderPlateTaskInstance.objects.create(task = task, part = obj, status = "a")
            
# Create Pitching Tasks
@receiver(m2m_changed, sender = Part.Pitching_tasks.through)
def CreateNewPitchingTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    Pitchingtask_list = obj.Pitching_tasks.all()
    for task in Pitchingtask_list:
        try:
            PitchingTaskInstance.objects.get(task = task, part = obj)
        except:
            PitchingTaskInstance.objects.create(task = task, part = obj, status = "a")
            
# Create WireCut Tasks
@receiver(m2m_changed, sender = Part.Wire_Cut_tasks.through)
def CreateNewWireCutTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    WireCuttask_list = obj.Wire_Cut_tasks.all()
    for task in WireCuttask_list:
        try:
            WireCutTaskInstance.objects.get(task = task, part = obj)
        except:
            WireCutTaskInstance.objects.create(task = task, part = obj, status = "a")
            
# Create Deburr Tasks
@receiver(m2m_changed, sender = Part.Deburr_tasks.through)
def CreateNewDeburrTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    Deburrtask_list = obj.Deburr_tasks.all()
    for task in Deburrtask_list:
        try:
            DeburrTaskInstance.objects.get(task = task, part = obj)
        except:
            DeburrTaskInstance.objects.create(task = task, part = obj, status = "a")
            
# Create Plating Tasks
@receiver(m2m_changed, sender = Part.Plating_tasks.through)
def CreateNewPlatingTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    Platingtask_list = obj.Plating_tasks.all()
    for task in Platingtask_list:
        try:
            PlatingTaskInstance.objects.get(task = task, part = obj)
        except:
            PlatingTaskInstance.objects.create(task = task, part = obj, status = "a")