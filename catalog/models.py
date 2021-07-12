from django.db import models
from django.urls import reverse # generate urls' by reversing url patterns
import uuid #Required for unique book instances
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone

class Stacking_Task(models.Model):
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
    
class StackingTaskInstance(models.Model):
    """ Instance of a specific component prep task"""
    task = models.CharField(max_length= 100, null = True)
    part = models.ForeignKey("Part",on_delete=models.CASCADE, null=True)
    TASK_STATUS = (("a","Not Started"),("h", "On Hold"),("c", "Complete"),
                   ("p", "In Progress"), ("f", "Failed"))
    
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
    TASK_STATUS = (("a","Not Started"),("h", "On Hold"),("c", "Complete"),
                   ("p", "In Progress"), ("f", "Failed"))
    
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
    team = models.ForeignKey(Team, on_delete = models.RESTRICT, null = True)
    Component_Prep_tasks = models.ManyToManyField(Component_Prep_Task, help_text = "Select \
                                     the component prep tasks \
                                         to be completed.") 
    Stacking_tasks = models.ManyToManyField(Stacking_Task, help_text = "Select\
                                         the required stacking tasks.")
    pub_date = models.DateTimeField("time published", default = timezone.now)
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a sepecfic author instance."""
        return reverse("part-detail", args=[str(self.id)])
    
@receiver(m2m_changed, sender = Part.Component_Prep_tasks.through)
def CreateNewCPTaskInstance(sender, **kwargs):
    #part_name = "title"
    obj = Part.objects.latest("pub_date")
    #part = getattr(obj, part_name)
    CPtask_list = obj.Component_Prep_tasks.all()
    Current_Tasks = ComponentPrepTaskInstance.objects.all()
    Current_Task_list = []
    for task in Current_Tasks:
        Current_Task_list.append(task.task)
    Create_list = []  
    if len(CPtask_list) == 0:
        pass
    else:
        for task in CPtask_list:
            if task.title in Current_Task_list:
                pass
            else:
                Create_list.append(task)
        for task in Create_list:
            ComponentPrepTaskInstance.objects.create(task= task, part=obj, status="a")
    


@receiver(m2m_changed, sender = Part.Stacking_tasks.through)
def CreateNewStackingTaskInstance(sender, **kwargs):
    obj = Part.objects.latest("pub_date")
    Stacktask_list = obj.Stacking_tasks.all()
    Current_Tasks = StackingTaskInstance.objects.all()
    Current_Task_list = []
    for task in Current_Tasks:
        Current_Task_list.append(task.task)
    Create_list = []
    if len(Stacktask_list) == 0:
        pass
    else:
        for task in Stacktask_list:
            if task.title in Current_Task_list:
                pass
            else:
                Create_list.append(task)
        for task in Create_list:
            StackingTaskInstance.objects.create(task= task, part=obj, status="a")
            