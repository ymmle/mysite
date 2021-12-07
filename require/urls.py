from .views import require_detail, requires_with_type, require_list, requires_with_date
from django.urls import path

urlpatterns = [
    #http://localhosr:8000/require
    path('',require_list, name = 'require_list'),
    path('<int:require_pk>',require_detail, name='require_detail'),
    path('type/<int:require_type_pk>',requires_with_type, name='requires_with_type'),
    path('date/<int:year>/<int:month>',requires_with_date, name='requires_with_date'),

]