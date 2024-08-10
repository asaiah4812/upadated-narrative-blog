from django.urls import path
from .import views

app_name='inspiration'

urlpatterns = [
    path('inspiration/', views.inspiration, name='inspiration'),
    # path('inspiration-detail/', views.inspiration_detail, name='inspiration_detail')
]
