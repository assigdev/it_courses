from django.urls import path
from .views import StudentSelectionCPView


app_name = 'control_center'
urlpatterns = [
    path('selection/<slug:slug>', StudentSelectionCPView.as_view(), name='selection'),
]
