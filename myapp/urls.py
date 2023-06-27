from django.urls import path
from myapp import views

urlpatterns = [
    path("",views.image_to_text,name="image_to_text"),
]