from django.urls import path
from . import views
from django.conf.urls.static import static
from agvinture import settings

urlpatterns = [
    # Pages
    path('', views.homepage, name='homepage'),
    path('endpoints/', views.endpoints, name='endpoints'),
    path('trees/', views.get_trees, name='trees'),
    path('lots/', views.get_lots, name='lots'),
    path('sections/', views.get_sections, name='sections'),
    path('statuses/', views.get_statuses, name='statuses'),
    path('geolocations/', views.get_geolocations, name='geolocations'),
    # specific views
    path('tree/<int:id>/', views.specific_tree, name='tree'),
    path('section/<int:id>/', views.specific_section, name='section'),
    path('lot/<int:id>/', views.specific_lot, name='lot'),
    path('status/<int:id>/', views.specific_status, name='status'),
    path('geolocation/<int:id>/', views.specific_geolocation, name='geolocation'),
    # create objects
    path('add/tree/', views.create_tree_object, name='add-tree'),
    path('add/section/', views.create_section_object, name='add-section'),
    path('add/lot/', views.create_lot_object, name='add-lot'),
    path('add/status/', views.create_status_object, name='add-status'),
    path('add/geolocation/', views.create_geolocation_object, name='add-geolocation'),
    path('create/coordinate/', views.create_coordinates, name='create-coordinate-object'),
    # edit objects
    path('edit/tree/<int:id>/', views.update_tree, name='edit-tree'),
    path('edit/section/<int:id>/', views.update_section, name='edit-section'),
    path('edit/lot/<int:id>/', views.update_lot, name='edit-lot'),
    path('edit/status/<int:id>/', views.update_status, name='edit-status'),
    path('edit/geolocation/<int:id>/', views.update_geolocation, name='edit-geolocation'),
    # delete objects url
    path('delete/tree/<int:id>/', views.delete_tree, name='delete-tree'),
    path('delete/section/<int:id>/', views.delete_section, name='delete-section'),
    path('delete/lot/<int:id>/', views.delete_lot, name='delete-lot'),
    path('delete/status/<int:id>/', views.delete_status, name='delete-status'),
    path('delete/geolcoation/<int:id>/', views.delete_geolocation, name='delete-geolocation'),
    # other views URL
    path('lots/section/<int:id>/', views.lots_section, name='lots-section'),
    path('lot/<int:lot_id>/section/<int:section_id>/', views.lot_section_view, name='section-lot'),
    path('lot/<int:lot_id>/section/<int:section_id>/tree/<int:tree_id>/status/<int:status_id>/',
        views.create_geolocation_view_ease,
        name='create-geolcoation'
    ),
    path('lot/<int:lot_id>/section/<int:section_id>/tree/<int:tree_id>/status/<int:status_id>/offline/',
        views.create_geolocation_view_ease_offline,
        name='create-geolcoation-offline'
    ),
    path('page/trees/', views.trees, name='trees-page'),
    path('page/sections/', views.sections, name='sections-page'),
    path('page/lots/', views.lots, name='lots-page'),
    path('page/geolocations/', views.geolocations, name='geolocations-page'),
    path('page/geolocation/<int:id>/', views.geolocation, name='geolocation-page'),
    path('login/', views.authentication, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # view functions
    path('edit/<str:tree>/', views.change_edit_tree_name, name='edit-tree'),
    path('load-coordinates/', views.load_json, name='load-coordinates'),
    path('download/excel/geolocation/dates/', views.download_geolocation_dates_excel, name='geolocation-date-excel'),
    path('download/excel/geolocation/section/', views.download_geolocation_section_excel,
         name='geolocation-section-excel'),
    path('download/excel/geolocation/lot/', views.download_geolocation_lot_excel, name='geolocation-lot-excel'),
    # APIS
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
