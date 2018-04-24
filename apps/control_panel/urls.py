from django.urls import path
from .views import StudentSelectionCPView, StudentVisitCPView, StudentHomeworkCPView


app_name = 'control_center'
urlpatterns = [
    path('selection/<slug:slug>', StudentSelectionCPView.as_view(), name='selection'),
    path('visit/<slug:slug>/', StudentVisitCPView.as_view(), name='visit_current'),
    path('visit/<slug:slug>/<slug:lesson_slug>', StudentVisitCPView.as_view(), name='visit'),
    path('homework/<slug:slug>/', StudentHomeworkCPView.as_view(), name='homework_current'),
    path('homework/<slug:slug>/<slug:lesson_slug>', StudentHomeworkCPView.as_view(), name='homework'),
]
