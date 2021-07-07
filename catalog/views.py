from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.forms import RenewBookForm

def index(request):
    """View for the home page of the website"""
    
    #Generate counts for soe of the main objetcs
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    #Avivable books (status = "a")
    num_instances_avaliable = BookInstance.objects.filter(status__exact="a").count()
    
    #all() is implied by default
    num_authors = Author.objects.count()
    
    #Number of site visits by the current user
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    
    
    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_avaliable,
        "num_authors": num_authors,        
        "num_visits": num_visits,
        }
    
    #Render the HTML template index.html with the data in the context vairable
    return render(request, "index.html", context = context)

def BookRenewSuccess(request):
    """View confirming the book renewal has been completed"""
    
    #book_instance = get_object_or_404(BookInstance)
    #context = {
        #'book_instance': book_instance,
    #}
    return render(request, "catalog/book_renew_success.html", context = None)


class BookListView(generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    context_object_name = "book_list"
    #queryset = Book.objects.filter(title__icontains="Enginee"[:3])
    template_name = "books/book_list.html"
    paginate_by = 10
 

class BookDetailView(generic.DetailView):
    model = Book
    
class AuthorListView(generic.ListView):
    model = Author
    context_object_name = "author_list"
    template_name = "authors/author_list.html"
    paginate_by = 10
    
class AuthorDetailView(generic.DetailView):
    model = Author
    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact="o").order_by("due_back")
    
import datetime

from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('bookrenewsuccess'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(LoginRequiredMixin,CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(LoginRequiredMixin,UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(LoginRequiredMixin,DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    
class BookCreate(LoginRequiredMixin,CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookUpdate(LoginRequiredMixin,UpdateView):
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)