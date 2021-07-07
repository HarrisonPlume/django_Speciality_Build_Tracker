from django.contrib import admin
from .models import Author, Book, BookInstance, Component_PrepTask, ComponentPrepTaskInstance, Part
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

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    inlines = [BookInstanceInline]
    
    
    
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ("status", "due_back")
    
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', "borrower")
        }),
    )
    list_display = ("book","status","borrower", "due_back", "id")
    
#@admin.register(Component_Prep)
#class TaskInstanceAdmin(admin.ModelAdmin):
    #list_filter = ["status"]
    
    #fieldsets = (
        #(None, {
            #'fields': ('speciality_build_area', 'status')
        #}),
    #)
    #list_display = ("book","status","borrower", "due_back", "id")

admin.site.register(Component_PrepTask)
admin.site.register(ComponentPrepTaskInstance)
admin.site.register(Part)