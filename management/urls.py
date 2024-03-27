from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('endpoints/', views.endpoints, name='endpoints'),
    path('trees/', views.get_trees, name='trees'),
    path('lots/', views.get_lots, name='lots'),
    path('sections/', views.get_sections, name='sections'),
    path('geolocations/', views.get_geolocations, name='geolocations'),
    # specific views
    path('tree/<int:id>/', views.specific_tree, name='tree'),
    path('section/<int:id>/', views.specific_section, name='section'),
    path('lot/<int:id>/', views.specific_lot, name='lot'),
    path('geolocation/<int:id>/', views.specific_geolocation, name='geolocation'),
    # create objects
    path('add/tree/', views.create_tree_object, name='add-tree'),
    path('add/section/', views.create_section_object, name='add-section'),
    path('add/lot/', views.create_lot_object, name='add-lot'),
    # edit objects
    path('edit/tree/<int:id>/', views.update_tree, name='edit-tree'),
    # delete objects url
    path('delete/tree/<int:id>/', views.delete_tree, name='delete-tree'),
]
