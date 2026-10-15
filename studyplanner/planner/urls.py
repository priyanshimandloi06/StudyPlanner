from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('plan/', views.plan_view, name='plan'),
    path('plan/new-week/', views.new_week, name='new_week'),
    path('slot/<int:slot_id>/delete/', views.delete_slot, name='delete_slot'),
    path('slot/<int:slot_id>/log/', views.log_minutes, name='log_minutes'),
    path('report/', views.report, name='report'),
]
