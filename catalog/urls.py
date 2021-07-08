from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("CPTasks/", views.CpTaskListView.as_view(), name="cptasks"),
    path("CPTask/<int:pk>", views.CPTaskDetailView.as_view(), name = "cptask-detail"),
    ]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('book/renew/success/', views.BookRenewSuccess, name='bookrenewsuccess'),
]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
]

urlpatterns += [
    path("parts/", views.PartListView.as_view(), name = "parts"),
    path("part/<int:pk>", views.PartDetailView.as_view(), name = "part-detail"),
    path('part/create/', views.PartCreate.as_view(), name='part-create'),
    path('part/<int:pk>/update/', views.PartUpdate.as_view(), name='part-update'),
]