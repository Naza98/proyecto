from django.urls import path, include

from .views import (DomicilioCreateView)
                    

urlpatterns = [
    path('new/<int:id>',DomicilioCreateView.as_view(), name="domicilio_new"),
]