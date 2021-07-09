from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("CPTasks/", views.CpTaskListView.as_view(), name="cptasks"),
    path("CPTask/<int:pk>/", views.CPTaskDetailView.as_view(), name = "cptask-detail"),
    path("CPTask/<int:pk>/updatestatus/", views.CPTaskStatusUpdate.as_view(), name = "cptask-update-status"),
    path("CPTask/<int:pk>/delete/", views.CPTaskDelete.as_view(), name = "cptask-delete"),
    ]

urlpatterns += [
    path("parts/", views.PartListView.as_view(), name = "parts"),
    path("part/<int:pk>/", views.PartDetailView.as_view(), name = "part-detail"),
    path('part/create/', views.PartCreate.as_view(), name='part-create'),
    path('part/<int:pk>/update/', views.PartUpdate.as_view(), name='part-update'),
    path('part/<int:pk>/delete/', views.PartDelete.as_view(), name='part-delete'),
]