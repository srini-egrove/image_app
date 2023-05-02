# from django.urls import path

# from myapp import views

# urlpatterns = [
#     path("imageupload/",views.upload_file,name="upload_file"),
# ]
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.image_upload, name='image_upload'),
    path('scan_image', views.image_scan, name='image_scan'),
    # path('image/', views.image_capture, name='image_capture'),
]
