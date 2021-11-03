from django.urls import path
from . import views
#Index
urlpatterns = [
    path("", views.index, name = "index"),
    ]
#Componet Prep urls
urlpatterns += [
    path("CPTasks/", views.CpTaskListView.as_view(), name="cptasks"),
    path("CPTask/<int:pk>/", views.CPTaskDetailView.as_view(), 
         name = "cptask-detail"),
    path("CPTask/<int:pk>/updatestatus/", views.CPTaskStatusUpdate.as_view(), 
         name = "cptask-update-status"),
    path("CPTask/<int:pk>/delete/", views.CPTaskDelete.as_view(), 
         name = "cptask-delete"),
    path("CPTask/<int:pk>/StartTask", views.StartCPTask, 
         name="startcptask"),
    path("CPTask/<int:pk>/FinishTask", views.FinishCPTask, 
       name="finishcptask"),
    path('mask_feed', views.mask_feed, name='mask_feed'),
    path("WorkOrderScan/", views.WorkOrderScan, name="Scan"),
    path('ScanComplete/', views.ScanResult, name='Scan_Complete'),
    ]
#Check off core urls
urlpatterns += [
    path("FinalChecks/", views.FinalChecks, name = "finalchecks"),
    path("CoreArchive/", views.CoreArchiveView.as_view(), name = "corearchive"),
    path('part/<int:pk>/complete/', views.PartComplete, 
         name='part-complete'),
    path('parts/dashboard/', views.PartDashboardView.as_view(), 
         name='part-dashboard'),
    ]
# part url's
urlpatterns += [
    path("parts/", views.PartListView.as_view(), name = "parts"),
    path("part/<int:pk>/", views.PartDetailView.as_view(), 
         name = "part-detail"),
    path('part/create/', views.PartCreate, name='part-create'),
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
  path("StackingTask/<int:pk>/StartTask", views.StartStackTask, 
         name="startstackingtask"),
  path("StackingTask/<int:pk>/FinishTask", views.FinishStackTask, 
         name="finishstackingtask"),
    ]

#Forming Task Url's
urlpatterns += [
  path("FormingTasks/", views.FormingTaskInstanceListView.as_view(), 
       name="formingtasks"),
  path("FormingTask/<int:pk>/", views.FormingTaskInstanceDetailView.as_view(), 
       name="formingtask-detail"),
  path("FormingTask/<int:pk>/updatestatus/", views.FormingTaskStatusUpdate.as_view(), 
       name="formingtask-update-status"),
  path("FormingTask/<int:pk>/delete/", views.FormingTaskDelete.as_view(), 
       name="formingtask-delete"),
  path("FormingTask/<int:pk>/StartTask", views.StartFormingTask, 
         name="startformingtask"),
  path("FormingTask/<int:pk>/FinishTask", views.FinishFormingTask, 
         name="finishformingtask"),
    ]



#Header Plate Task Url's
urlpatterns += [
  path("HPTasks/", views.HeaderPlateTaskInstanceListView.as_view(), 
       name="headerplatetasks"),
  path("HPTask/<int:pk>/", views.HeaderPlateTaskInstanceDetailView.as_view(), 
       name="hptask-detail"),
  path("HPTask/<int:pk>/updatestatus/", views.HeaderPlateTaskStatusUpdate.as_view(), 
       name="hptask-update-status"),
  path("HPTask/<int:pk>/delete/", views.HeaderPlateTaskDelete.as_view(), 
       name="hptask-delete"),
  path("HPTask/<int:pk>/StartTask", views.StartHeaderPlateTask, 
         name="starthptask"),
  path("HPTask/<int:pk>/FinishTask", views.FinishHeaderPlateTask, 
         name="finishhptask"),
    ]

#Pitching Task Url's
urlpatterns += [
  path("PitchingTasks/", views.PitchingTaskListView.as_view(), 
       name="pitchingtasks"),
  path("PitchingTask/<int:pk>/", views.PitchingTaskDetailView.as_view(), 
       name="pitchingtask-detail"),
  path("PitchingTask/<int:pk>/updatestatus/", views.PitchingTaskStatusUpdate.as_view(), 
       name="pitchingtask-update-status"),
  path("PitchingTask/<int:pk>/delete/", views.PitchingTaskDelete.as_view(), 
       name="pitchingtask-delete"),
  path("PitchingTask/<int:pk>/StartTask", views.StartPitchingTask, 
       name="startpitchingtask"),
  path("PitchingTask/<int:pk>/FinishTask", views.FinishPitchingTask, 
       name="finishpitchingtask"),
    ]

#Wire Cut Task Url's
urlpatterns += [
  path("WireCutTasks/", views.WireCutTaskListView.as_view(), 
       name="wirecuttasks"),
  path("WireCutTask/<int:pk>/", views.WireCutTaskDetailView.as_view(), 
       name="wirecuttask-detail"),
  path("WireCutTask/<int:pk>/updatestatus/", views.WireCutTaskStatusUpdate.as_view(), 
       name="wirecuttask-update-status"),
  path("WireCutTask/<int:pk>/delete/", views.WireCutTaskDelete.as_view(), 
       name="wirecuttask-delete"),
  path("WireCutTask/<int:pk>/StartTask", views.StartWireCutTask, 
       name="startwirecuttask"),
  path("WireCutTask/<int:pk>/FinishTask", views.FinishWireCutTask, 
       name="finishwirecuttask"),
    ]

#deburr Task Url's
urlpatterns += [
  path("DeburrTasks/", views.DeburrTaskListView.as_view(), 
       name="deburrtasks"),
  path("DeburrTask/<int:pk>/", views.DeburrTaskDetailView.as_view(), 
       name="deburrtask-detail"),
  path("DeburrTask/<int:pk>/updatestatus/", views.DeburrTaskStatusUpdate.as_view(), 
       name="deburrtask-update-status"),
  path("DeburrTask/<int:pk>/delete/", views.DeburrTaskDelete.as_view(), 
       name="deburrtask-delete"),
  path("DeburrTask/<int:pk>/StartTask", views.StartDeburrTask, 
       name="startdeburrtask"),
  path("DeburrTask/<int:pk>/FinishTask", views.FinishDeburrTask, 
       name="finishdeburrtask"),
    ]

#Plating Task Url's
urlpatterns += [
  path("PlatingTasks/", views.PlatingTaskListView.as_view(), 
       name="platingtasks"),
  path("PlatingTask/<int:pk>/", views.PlatingTaskDetailView.as_view(), 
       name="platingtask-detail"),
  path("PlatingTask/<int:pk>/updatestatus/", views.PlatingTaskStatusUpdate.as_view(), 
       name="platingtask-update-status"),
  path("platingTask/<int:pk>/delete/", views.PlatingTaskDelete.as_view(), 
       name="platingtask-delete"),
  path("PlatingTask/<int:pk>/StartTask/", views.StartPlatingTask, 
       name="startplatingtask"),
  path("PlatingTask/<int:pk>/FinishTask/", views.FinishPlatingTask, 
       name="finishplatingtask"),
    ]

#Create Team Url
urlpatterns += [
    path("team/create", views.TeamCreate.as_view(), name = "teamcreate")
]
