# from rest_framework.routers import DefaultRouter
# from .views import TALTutorViewSet
#
# TALTutor_router = DefaultRouter()
# TALTutor_router.register('TALTutor',TALTutorViewSet)

from django.urls import path
from .views import save_or_update_app_instance, load_app_instance

urlpatterns = [
    path('save/', save_or_update_app_instance, name='save_or_update_app_instance'),
    path('load/<str:session_key>/', load_app_instance, name='load_app_instance'),
]
