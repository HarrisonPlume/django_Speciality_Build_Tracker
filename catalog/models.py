from django.db import models
from django.urls import reverse # generate urls' by reversing url patterns
import uuid #Required for unique book instances
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone
    
class Component_PrepTask(models.Model):
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
    #part = models.CharField(max_length= 100, null = True)
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
        """Returns the url to access a detail record for this book."""
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
    CPtasks = models.ManyToManyField(Component_PrepTask, help_text = "Select \
                                     the component prep tasks \
                                         to be completed.")    
    pub_date = models.DateTimeField("time published", default = timezone.now)
    def __str__(self):
        """String for Representing the model objetc (on admin site)"""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a sepecfic author instance."""
        return reverse("part-detail", args=[str(self.id)])
    
@receiver(m2m_changed, sender = Part.CPtasks.through)
def CreateNewTaskInstance(sender, **kwargs):
    part_name = "title"
    obj = Part.objects.latest("pub_date")
    part = getattr(obj, part_name)
    task_list = obj.CPtasks.all()
    if len(task_list) == 0:
        pass
    else:
        for task in task_list:
            ComponentPrepTaskInstance.objects.create(task= task, part=obj, status="a")
    
class Book(models.Model):
    """ Model Representing a book"""
    title = models.CharField(max_length=200)
    
    #Foreign Key relationship as a book has multiple one many relationships
    #Books can only have a single author but an author can have multiple 
    #books.
    author = models.ForeignKey("Author", on_delete = models.SET_NULL,
                               null = True)
    
    summary = models.TextField(max_length = 1000, help_text = "Enter a breif\
                               description of the book in question.")
    isbn = models.CharField("ISBN", max_length = 13, unique = True,
                            help_text ='13 Character <a href = \
   "https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
   
    #ManyToManyField used becasue genre can contain many books. Books can cover
    #many genres. 
    #Utalsies the Genre class which is defined above
    
    class Meta:
        ordering = ["title", "author"]
   
    def __str__(self):
        """String for representing the Model object."""
        return self.title
  
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args = [str(self.id)])
    
    def display_genre(self):
        """Create a string for the Genre. This is required to show each genre \
            on the admin website"""
        return ", ".join(genre.name for genre in self.genre.all()[:3])    
    display_genre.short_description = 'Genre'
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
               

class BookInstance(models.Model):
    """Model representing a specific copy of a book \
        (i.e. that can be borrowed physically)."""
    id = models.UUIDField(primary_key=True, default = uuid.uuid4,
                          help_text = "Unique Book Id for each instance")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    
    LOAN_STATUS = (("m","Maintenance"),("o", "On loan"),("a", "Available"),
                   ("r", "Reserved"), ("x", "Missing"))
    
    status = models.CharField(max_length = 1, choices= LOAN_STATUS, 
                              blank = True, default = "m", help_text = "Book \
                                  availability")
                                  
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
                                
    class Meta:
        ordering = ['status', 'due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)
    
    def __str__(self):
        """string for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    date_of_birth = models.DateField(null=True, blank = True)
    date_of_death = models.DateField("died", null=True, blank=True)
    
    class Meta:
        ordering = ["last_name","first_name"]
        
    def get_absolute_url(self):
        """Returns the url to access a sepecfic author instance."""
        return reverse("author-detail", args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'