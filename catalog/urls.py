from django.urls import path
from . import views
#component prep url's
urlpatterns = [
    path("", views.index, name = "index"),
    path("CPTasks/", views.CpTaskListView.as_view(), name="cptasks"),
    path("CPTask/<int:pk>/", views.CPTaskDetailView.as_view(), 
         name = "cptask-detail"),
    path("CPTask/<int:pk>/updatestatus/", views.CPTaskStatusUpdate.as_view(), 
         name = "cptask-update-status"),
    path("CPTask/<int:pk>/delete/", views.CPTaskDelete.as_view(), 
         name = "cptask-delete"),
    ]
# part url's
urlpatterns += [
    path("parts/", views.PartListView.as_view(), name = "parts"),
    path("part/<int:pk>/", views.PartDetailView.as_view(), 
         name = "part-detail"),
    path('part/create/', views.PartCreate.as_view(), name='part-create'),
    path('part/<int:pk>/update/', views.PartUpdate.as_view(), 
         name='part-update'),
    path('part/<int:pk>/delete/', views.PartDelete.as_view(), 
         name='part-delete'),
]

# stacking task urls
urlpatterns += [
  path("StackingTasks/", views.StackingTaskListView.as_view(), 
       name="stackingtasks"),
  path("StackingTask/<int:pk>/", views.StackingTaskDetailView.as_view(), 
       name="stackingtask-detail"),
  path("StackingTask/<int:pk>/updatestatus/", 
       views.StackingTaskStatusUpdate.as_view(), 
       name = "stackingtask-update-status"),
  path("StackingTask/<int:pk>/delete/", views.StackingTaskDelete.as_view(), 
         name = "stackingtask-delete"),
    ]

#Forming Task Url's
urlpatterns += [
  path("FormingTasks/", views.FormingTaskInstanceListView.as_view(), 
       name="formingtasks"),
  path("FormingTask/<int:pk>/", views.FormingTaskInstanceDetailView.as_view(), 
       name="formingtask-detail"),
  path("FormingTask/<int:pk>/updatestatus/", views.FormingTaskStatusUpdate.as_view(), 
       name="formingtask-update-status"),
    ]

#Update Component prep task status
urlpatterns += [
    path("CPTask/<int:pk>/StartTask", views.StartCPTask, 
         name="startcptask"),
    path("CPTask/<int:pk>/FinishTask", views.FinishCPTask, 
       name="finishcptask"),
  ]

#Update stacking task status
urlpatterns += [
    path("StackingTask/<int:pk>/StartTask", views.StartStackTask, 
         name="startstackingtask"),
    path("StackingTask/<int:pk>/FinishTask", views.FinishStackTask, 
         name="finishstackingtask"),
  ]

#Update forming task status
urlpatterns += [
    path("FormingTask/<int:pk>/StartTask", views.StartFormingTask, 
         name="startformingtask"),
    path("FormingTask/<int:pk>/FinishTask", views.FinishFormingTask, 
         name="finishformingtask"),
  ]