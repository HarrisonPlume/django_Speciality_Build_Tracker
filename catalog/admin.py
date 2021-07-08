from django.contrib import admin
from .models import Author, Book, BookInstance, Component_PrepTask, ComponentPrepTaskInstance, Part, Team
# Register your models here.

#admin.site.register(Book)
#admin.site.register(Author)
#admin.site.register(Genre)
#admin.site.register(BookInstance)
#admin.site.register(Language)

class AuthorInstanceInline(admin.TabularInline):
    model = Book
    extra = 0

#Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]
    inlines = [AuthorInstanceInline]

#Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

class ComponentPrepTaskAdmin(admin.ModelAdmin):
    list_display = ("task","part","status")

admin.site.register(ComponentPrepTaskInstance, ComponentPrepTaskAdmin)
admin.site.register(Component_PrepTask)
#admin.site.register(ComponentPrepTaskInstance)
admin.site.register(Part)
admin.site.register(Team)