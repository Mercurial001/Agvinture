from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest, \
    HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Trees, Section, Lot, Geolocation, PlantedStatus, Coordinates
from .serializers import TreesSerializer, LotSerializer, SectionSerializer, GeolocationSerializer, PlantedStatusSerializer, CoordinatesSerializer
from django.utils import timezone
import folium
from django.db import models
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
# from pytz import timezone
import json
from datetime import datetime
from django.core.serializers import serialize, deserialize
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .decorators import authenticated_user
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def homepage(request):
    current_site = get_current_site(request)
    protocol = "https" if request.is_secure() else "http"
    media_url = f"{protocol}://{current_site.domain}{settings.MEDIA_URL}"

    geolocations = Geolocation.objects.filter(lat__isnull=False, long__isnull=False)
    coordinates = Coordinates.objects.filter(lat__isnull=False, long__isnull=False, section='Section 5')

    coordinates_lat_mean = coordinates.aggregate(models.Avg('lat'))['lat__avg']
    coordinates_long_mean = coordinates.aggregate(models.Avg('long'))['long__avg']

    coordinates_map = folium.Map(
        location=[coordinates_lat_mean, coordinates_long_mean],
        # location=[124.52333, 11.0244],
        zoom_start=15,
        no_wrap=False,
        max_bounds=True
    )

    # Add the GeoJSON layer to the map and style the border

    section_1_coordinates_list = []

    section_1_coordinates = Coordinates.objects.filter(section='Section 1 Coordinates')
    for coordinates in section_1_coordinates:
        section_1_coordinates_list.append([coordinates.long, coordinates.lat])

    geojson_section_1 = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                section_1_coordinates_list
            ]
        }
    }

    folium.GeoJson(
        geojson_section_1,
        style_function=lambda feature: {
            'color': 'orange',  # Border color
            'weight': 2,  # Border weight
            'opacity': 0.5  # Border opacity
        },

    ).add_to(coordinates_map)

    section_2_coordinates_list = []
    section_2_coordinates = Coordinates.objects.filter(section='Section 2 Coordinates')
    for coordinates in section_2_coordinates:
        section_2_coordinates_list.append([coordinates.long, coordinates.lat])

    geojson_section_2 = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                section_2_coordinates_list
            ]
        }
    }

    folium.GeoJson(
        geojson_section_2,
        style_function=lambda feature: {
            'color': 'blue',  # Border color
            'weight': 2,  # Border weight
            'opacity': 0.5  # Border opacity
        },

    ).add_to(coordinates_map)

    section_3_coordinates_list = []
    section_3_coordinates = Coordinates.objects.filter(section='Section 3 Coordinates')
    for coordinates in section_3_coordinates:
        section_3_coordinates_list.append([coordinates.long, coordinates.lat])

    geojson_section_3 = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                section_3_coordinates_list
            ]
        }
    }

    folium.GeoJson(
        geojson_section_3,
        style_function=lambda feature: {
            'color': 'red',  # Border color
            'weight': 2,  # Border weight
            'opacity': 0.5  # Border opacity
        },

    ).add_to(coordinates_map)

    section_6_coordinates_list = []
    section_6_coordinates = Coordinates.objects.filter(section='Section 6 Coordinates')
    for coordinates in section_6_coordinates:
        section_6_coordinates_list.append([coordinates.long, coordinates.lat])

    geojson_section_6 = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                section_6_coordinates_list
            ]
        }
    }

    folium.GeoJson(
        geojson_section_6,
        style_function=lambda feature: {
            'color': 'violet',  # Border color
            'weight': 2,  # Border weight
            'opacity': 0.5  # Border opacity
        },

    ).add_to(coordinates_map)

    section_5_coordinates_list = []
    if Coordinates.objects.filter(section='Section 5 Coordinates').exists():
        section_5_coordinates = Coordinates.objects.filter(section='Section 5 Coordinates')
        for coordinate in section_5_coordinates:
            section_5_coordinates_list.append([coordinate.long, coordinate.lat])

    geojson_section_5 = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                section_5_coordinates_list
            ]
        }
    }

    folium.GeoJson(
        geojson_section_5,
        style_function=lambda feature: {
            'color': 'rgb(40, 90, 90)',  # Border color
            'weight': 2,  # Border weight
            'opacity': 0.5  # Border opacity
        },

    ).add_to(coordinates_map)

    section_4_coordinates_list = []
    section_4_coordinates = Coordinates.objects.filter(section='Section 4 Coordinates')
    for coordinate in section_4_coordinates:
        section_4_coordinates_list.append([coordinate.long, coordinate.lat])

    geojson_section_4 = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                section_4_coordinates_list
            ]
        }
    }

    folium.GeoJson(
        geojson_section_4,
        style_function=lambda feature: {
            'color': 'rgb(15, 170, 90)',  # Border color
            'weight': 2,  # Border weight
            'opacity': 0.5  # Border opacity
        },

    ).add_to(coordinates_map)

    # Filters

    object_dates = {}
    for obj in geolocations:
        date = obj.date
        if date not in object_dates:
            object_dates[date] = [obj]
        else:
            object_dates[date].append(obj)

    unique_dates = []
    for date, obj in object_dates.items():
        unique_dates.append(date)

    section_objects = Section.objects.all()
    lot_objects = Lot.objects.all()

    selected_specific_date = request.GET.get('geolocation-dates')
    selected_specific_section = request.GET.get('geolocation-section')
    selected_specific_lot = request.GET.get('geolocation-lot')

    selected_composite_date = request.GET.get('geolocation-dates-composite')
    selected_composite_section = request.GET.get('geolocation-section-composite')
    selected_composite_lot = request.GET.get('geolocation-lot-composite')

    filter_applied = ''

    if selected_specific_date:
        date_obj = datetime.strptime(selected_specific_date, "%B %d, %Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        filter_applied = selected_specific_date
        filtered_geolocation = Geolocation.objects.filter(
            lat__isnull=False,
            long__isnull=False,
            date=formatted_date
        )
        for barangay in filtered_geolocation:
            folium.CircleMarker(
                location=[barangay.lat, barangay.long],
                popup=f"Tree: <strong>{barangay.tree.name}</strong><br><br>Longitude:{barangay.lat}, <br>Latitude:{barangay.long}"
                      f"<br>"
                      f"Status: {barangay.status}"
                      f"<br><br>"
                      f"Date: {barangay.date}"
                      f"<img src='{media_url}{barangay.image}' width='200' height='200'>",
                radius=0.1,  # Adjust the radius as needed
                color='green',  # Adjust the color as needed
                fill=True,
                fill_color='red',
                fill_opacity=0.6,
            ).add_to(coordinates_map)
    elif selected_specific_section:
        selected_section = Section.objects.get(id=selected_specific_section)
        filter_applied = selected_section.name
        filtered_geolocation = Geolocation.objects.filter(
            lat__isnull=False,
            long__isnull=False,
            section=selected_section
        )
        for barangay in filtered_geolocation:
            folium.CircleMarker(
                location=[barangay.lat, barangay.long],
                popup=f"Tree: <strong>{barangay.tree.name}</strong><br><br>Longitude:{barangay.lat}, <br>Latitude:{barangay.long}"
                      f"<br>"
                      f"Status: {barangay.status}"
                      f"<br><br>"
                      f"Date: {barangay.date}"
                      f"<img src='{media_url}{barangay.image}' width='200' height='200'>",
                radius=0.1,  # Adjust the radius as needed
                color='green',  # Adjust the color as needed
                fill=True,
                fill_color='red',
                fill_opacity=0.6,
            ).add_to(coordinates_map)
    elif selected_specific_lot:
        selected_lot = Lot.objects.get(id=selected_specific_lot)
        filter_applied = selected_lot.name
        filtered_geolocation = Geolocation.objects.filter(
            lat__isnull=False,
            long__isnull=False,
            lot=selected_lot
        )
        for barangay in filtered_geolocation:
            folium.CircleMarker(
                location=[barangay.lat, barangay.long],
                popup=f"Tree: <strong>{barangay.tree.name}</strong><br><br>Longitude:{barangay.lat}, <br>Latitude:{barangay.long}"
                      f"<br>"
                      f"Status: {barangay.status}"
                      f"<br><br>"
                      f"Date: {barangay.date}"
                      f"<img src='{media_url}{barangay.image}' width='200' height='200'>",
                radius=0.1,  # Adjust the radius as needed
                color='green',  # Adjust the color as needed
                fill=True,
                fill_color='red',
                fill_opacity=0.6,
            ).add_to(coordinates_map)
    elif selected_composite_date and selected_composite_section and selected_composite_lot:

        date_obj = datetime.strptime(selected_composite_date, "%B %d, %Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        selected_section = Section.objects.get(id=selected_composite_section)
        selected_lot = Lot.objects.get(id=selected_composite_lot)
        filtered_geolocation = Geolocation.objects.filter(
            lat__isnull=False,
            long__isnull=False,
            section=selected_section,
            lot=selected_lot,
            date=formatted_date,
        )
        for barangay in filtered_geolocation:
            folium.CircleMarker(
                location=[barangay.lat, barangay.long],
                popup=f"Tree: <strong>{barangay.tree.name}</strong><br><br>Longitude:{barangay.lat}, <br>Latitude:{barangay.long}"
                      f"<br>"
                      f"Status: {barangay.status}"
                      f"<br><br>"
                      f"Date: {barangay.date}"
                      f"<img src='{media_url}{barangay.image}' width='200' height='200'>",
                radius=0.1,  # Adjust the radius as needed
                color='green',  # Adjust the color as needed
                fill=True,
                fill_color='red',
                fill_opacity=0.6,
            ).add_to(coordinates_map)
    else:
        for barangay in geolocations:
            folium.CircleMarker(
                location=[barangay.lat, barangay.long],
                popup=f"Tree: <strong>{barangay.tree.name}</strong><br><br>Longitude:{barangay.lat}, <br>Latitude:{barangay.long}"
                      f"<br>"
                      f"Status: {barangay.status}"
                      f"<br><br>"
                      f"Date: {barangay.date}"
                      f"<img src='{media_url}{barangay.image}' width='200' height='200'>",
                radius=0.1,  # Adjust the radius as needed
                color='green',  # Adjust the color as needed
                fill=True,
                fill_color='red',
                fill_opacity=0.6,
            ).add_to(coordinates_map)

    # coordinates_map.add_child(folium.LatLngPopup())

    coordinates_map.save('highlighted_border_map.html')

    coordinates_html_map = coordinates_map._repr_html_()

    return render(request, 'base.html', {
        'coordinates_html_map': coordinates_html_map,
        'section_1_coordinates_list': section_1_coordinates_list,
        'section_2_coordinates_list': section_2_coordinates_list,
        'section_3_coordinates_list': section_3_coordinates_list,
        'section_4_coordinates_list': section_4_coordinates_list,
        'section_5_coordinates_list': section_5_coordinates_list,
        'section_6_coordinates_list': section_6_coordinates_list,
        'unique_dates': unique_dates,
        'section_objects': section_objects,
        'lot_objects': lot_objects,
        'selected_specific_date': selected_specific_date,
        'selected_specific_section': selected_specific_section,
        'selected_specific_lot': selected_specific_lot,
        'selected_composite_date': selected_composite_date,
        'selected_composite_section': selected_composite_section,
        'selected_composite_lot': selected_composite_lot,
        'filter_applied': filter_applied,
    })


@login_required(login_url='login')
def trees(request):
    trees = Trees.objects.all()
    return render(request, 'trees.html', {
        'trees': trees
    })


@login_required(login_url='login')
def sections(request):
    lots = Lot.objects.all()
    lots_section_list = {}
    for lot in lots:
        lot_section = lot.section
        if lot_section not in lots_section_list:
            lots_section_list[lot_section] = [lot]
        else:
            lots_section_list[lot_section].append(lot)

    return render(request, 'sections.html', {
        'lots_section': lots_section_list,
    })


@login_required(login_url='login')
def lots(request):
    lots = Lot.objects.all()
    lots_section = {}
    for lot in lots:
        lot_section = lot.section
        if lot_section not in lots_section:
            lots_section[lot_section] = [lot]
        else:
            lots_section[lot_section].append(lot)
    return render(request, 'lots.html', {
        'lots': lots,
        'lots_section': lots_section,
    })


@login_required(login_url='login')
def geolocations(request):
    geolocation_objects = Geolocation.objects.all()
    geolocation_dates = {}
    geolocation_filter = request.GET.get('filter')
    if_section = geolocation_filter == 'section'
    if_lot = geolocation_filter == 'lot'
    for geolocation in geolocation_objects:
        date = geolocation.date
        if date not in geolocation_dates:
            geolocation_dates[date] = [geolocation]
        else:
            geolocation_dates[date].append(geolocation)

    geolocation_sections = {}
    for geolocation in geolocation_objects:
        section = geolocation.section
        if section not in geolocation_sections:
            geolocation_sections[section] = [geolocation]
        else:
            geolocation_sections[section].append(geolocation)

    geolocation_lot = {}
    for geolocation in geolocation_objects:
        lot = geolocation.lot
        if lot not in geolocation_lot:
            geolocation_lot[lot] = [geolocation]
        else:
            geolocation_lot[lot].append(geolocation)

    return render(request, 'geolocations.html', {
        'geolocation_dates': geolocation_dates,
        'geolocation_sections': geolocation_sections,
        'geolocation_lot': geolocation_lot,
        'if_section': if_section,
        'if_lot': if_lot,
    })


@login_required(login_url='login')
def geolocation(request, id):
    geolocation_object = Geolocation.objects.get(id=id)
    return render(request, 'geolocation.html', {
        'geolocation': geolocation_object,
    })


@authenticated_user
def authentication(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid Form Data')

    return render(request, 'login.html', {

    })


def logout_user(request):
    logout(request)
    return redirect('login')


# def geolocation(request, section, lot):
#     section_object = Section.objects.get(name=section)
#     lot_object = Lot.objects.get(name=lot)
#     geolocation_objects = Geolocation.objects.filter(section=section_object.id, lot=lot_object.id)
#     return render(request, 'geolocations.html', {
#         'geolocation_objects': geolocation_objects,
#     })


def change_edit_tree_name(request, tree):
    tree_object = Trees.objects.get(name=tree)
    tree_name_value = request.POST.get('tree-edited-name')

    if request.method == 'POST':
        tree_object.name = tree_name_value
        tree_object.save()

    referring_url = request.META.get('HTTP_REFERER')

    if referring_url:
        # Redirect back to the referring page
        return HttpResponseRedirect(referring_url)
    else:
        # If there's no referring URL, redirect to a default page
        return redirect('homepage')


@api_view(['GET'])
def endpoints(request):
    routes = [
        # Displays
        {
            'Endpoint': '/trees/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of trees',
        },
        {
            'Endpoint': '/sections/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of section',
        },
        {
            'Endpoint': '/lots/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of lot'
        },
        {
            'Endpoint': '/statuses/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of statuses'
        },
        {
            'Endpoint': '/geolocations/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of locations'
        },
        # Specific Displays
        {
            'Endpoint': '/tree/id/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a specific tree view'
        },
        {
            'Endpoint': '/section/id/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a specific section',
        },
        {
            'Endpoint': '/lot/id/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a specific lot'
        },
        {
            'Endpoint': '/status/id/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a specific status'
        },
        {
            'Endpoint': '/geolocation/id/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a specific location of a tree'
        },
        # Object creation endpoints
        {
            'Endpoint': '/add/tree/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Created and adds a new tree',
        },
        {
            'Endpoint': '/add/lot/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates, or a adds a new lot',
        },
        {
            'Endpoint': '/add/section/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates or adds a new section',
        },
        {
            'Endpoint': '/add/status/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates a new status object'
        },
        {
            'Endpoint': '/add/geolocation/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates or adds a new tree location'
        },
        # Object Edition Endpoints
        {
            'Endpoint': '/edit/tree/id/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Edit a tree object',
        },
        {
            'Endpoint': '/edit/lot/id/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Edit a lot object',
        },
        {
            'Endpoint': '/edit/section/id/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Edit a section object',
        },
        {
            'Endpoint': '/edit/status/id/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Edit a status object'
        },
        {
            'Endpoint': '/edit/geolocation/id/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Edit a geolocation object'
        },
        # Delete Endpoints
        {
            'Endpoint': '/delete/tree/id/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes a tree object.'
        },
        {
            'Endpoint': '/delete/lot/id/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes a lot object',
        },
        {
            'Endpoint': '/delete/section/id/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes a section object',
        },
        {
            'Endpoint': '/delete/status/id/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes a status object'
        },
        {
            'Endpoint': '/delete/geolocation/id/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes a geolocation object'
        },
        # Specific Views
        {
            'Endpoint': '/lots/section/id/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of lots in a section'
        },
        {
            'Endpoint': '/lot/id/section/id/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a page of lot and section'
        },
        {
            'Endpoint': '/lot/id/section/id/tree/id/status/id/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Page for creating geolocation with ease'
        },
        # New model added endpoint creation
        {
            'Endpoint': '/retrieve-coordinates/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Retrieve Coordinates object from flutter app'
        }
    ]
    return Response(routes)


# All objects view functions
@api_view(['GET'])
def get_trees(request):
    trees = Trees.objects.all()
    serializer = TreesSerializer(trees, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_sections(request):
    sections = Section.objects.all()
    serializer = SectionSerializer(sections, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_lots(request):
    lots = Lot.objects.all()
    serializer = LotSerializer(lots, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_statuses(request):
    statuses = PlantedStatus.objects.all()
    serializer = PlantedStatusSerializer(statuses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_geolocations(request):
    geolocations = Geolocation.objects.all()
    serializer = GeolocationSerializer(geolocations, many=True)
    return Response(serializer.data)


# specific views
@api_view(['GET'])
def specific_tree(request, id):
    tree = Trees.objects.get(id=id)
    serializer = TreesSerializer(tree, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def specific_section(request, id):
    section = Section.objects.get(id=id)
    serializer = SectionSerializer(section, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def specific_lot(request, id):
    lot = Lot.objects.get(id=id)
    serializer = LotSerializer(lot, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def specific_status(request, id):
    status = PlantedStatus.objects.get(id=id)
    serializer = PlantedStatusSerializer(status, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def specific_geolocation(request, id):
    geolocation = Geolocation.objects.get(id=id)
    serializer = GeolocationSerializer(geolocation, many=False)
    return Response(serializer.data)


# create object function
@api_view(['POST'])
def create_tree_object(request):
    data = request.data

    tree = Trees.objects.create(
        name=data['name']
    )
    # tree.save()
    serializer = TreesSerializer(tree, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_section_object(request):
    data = request.data

    section = Section.objects.create(
        name=data['name']
    )
    serializer = SectionSerializer(section, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_lot_object(request):
    data = request.data

    lot = Lot.objects.create(
        name=data['name'],
        section=Section.objects.get(id=int(data['section'])),
    )
    serializer = LotSerializer(lot, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_status_object(request):
    data = request.data

    status = PlantedStatus.objects.create(
            name=data['name'],
        )
    serializer = PlantedStatusSerializer(status, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_geolocation_object(request):
    data = request.data

    geolocation = Geolocation.objects.create(
        lat=data['lat'],
        long=data['long'],
        image=data['image'],
        date=timezone.now(),
        date_time=timezone.now(),
        tree=data['tree'],
        section=data['section'],
        lot=data['lot'],
        status=data['status']
    )
    serializer = GeolocationSerializer(geolocation, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_coordinates(request):
    data = request.data

    coordinate = Coordinates.objects.create(
        section=data['section'],
        lat=data['lat'],
        long=data['long'],
        point=data['point']
    )

    serializer = CoordinatesSerializer(coordinate, many=False)
    return Response(serializer.data)


# Update/Edit object
@api_view(['PUT'])
def update_tree(request, id):
    tree = Trees.objects.get(id=id)
    # edited_tree = tree.name = data['name']
    serializer = TreesSerializer(tree, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PUT'])
def update_section(request, id):
    section_object = Section.objects.get(id=id)

    serializer = SectionSerializer(section_object, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PUT'])
def update_lot(request, id):
    lot = Lot.objects.get(id=id)

    serializer = LotSerializer(lot, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PUT'])
def update_status(request, id):
    status = PlantedStatus.objects.get(id=id)

    serializer = PlantedStatusSerializer(status, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PUT'])
def update_geolocation(request, id):
    geolocation = Geolocation.objects.get(id=id)

    serializer = GeolocationSerializer(geolocation, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


# delete objects view function
@api_view(['DELETE'])
def delete_tree(request, id):
    tree = Trees.objects.get(id=id)
    tree.delete()
    return Response('Tree deleted')


@api_view(['DELETE'])
def delete_section(request, id):
    section = Section.objects.get(id=id)
    section.delete()
    return Response('Section Deleted')


@api_view(['DELETE'])
def delete_lot(request, id):
    lot = Lot.objects.get(id=id)
    lot.delete()
    return Response('Lot Delete')


@api_view(['DELETE'])
def delete_status(request, id):
    status = PlantedStatus.objects.get(id=id)
    status.delete()
    return Response('Status Deleted')


@api_view(['DELETE'])
def delete_geolocation(request, id):
    geolocation = Geolocation.objects.get(id=id)
    geolocation.delete()
    return Response('Geolocation Deleted')


# Specific Views
@api_view(['GET'])
def lots_section(request, id):
    section = Section.objects.get(id=id)
    lots = Lot.objects.filter(section=section)

    serializer = LotSerializer(lots, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def lot_section_view(request, lot_id, section_id):
    lot = Lot.objects.get(id=lot_id)
    section = Section.objects.get(id=section_id)

    lot_serializer = LotSerializer(lot, many=False)
    section_serializer = SectionSerializer(section, many=False)

    response_data = {
        'lot': lot_serializer.data,
        'section': section_serializer.data
    }

    return Response(response_data)


@api_view(['POST'])
def create_geolocation_view_ease(request, lot_id, section_id, tree_id, status_id):
    data = request.data
    lot = Lot.objects.get(id=lot_id)
    section = Section.objects.get(id=section_id)
    tree = Trees.objects.get(id=tree_id)
    status = PlantedStatus.objects.get(id=status_id)

    current_date = timezone.now().date()

    geolocation = Geolocation.objects.create(
        lat=data['lat'],
        long=data['long'],
        date=current_date,
        date_time=timezone.now(),
        tree=tree,
        section=section,
        lot=lot,
        status=status,
        image=request.FILES.get('image'),  # Get the uploaded image
    )
    serializer = GeolocationSerializer(geolocation, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_geolocation_view_ease_offline(request, lot_id, section_id, tree_id, status_id):
    data = request.data
    lot = Lot.objects.get(id=lot_id)
    section = Section.objects.get(id=section_id)
    tree = Trees.objects.get(id=tree_id)
    status = PlantedStatus.objects.get(id=status_id)

    geolocation, created = Geolocation.objects.get_or_create(
        date_time=data['date_time'],
        defaults={
            'lat': data['lat'],
            'long': data['long'],
            'tree': tree,
            'date': data['date'],
            'section': section,
            'lot': lot,
            'status': status,
            'image': request.FILES.get('image')  # Get the uploaded image
        }
    )

    # Update fields if geolocation already exists
    if not created:
        geolocation.lat=data['lat']
        geolocation.long=data['long']
        geolocation.save()

    serializer = GeolocationSerializer(geolocation, many=False)
    return Response(serializer.data)


def jsonize_coordinates(request):
    coordinates = Coordinates.objects.all()
    serialized_coordinates = CoordinatesSerializer(coordinates, many=True)

    jsoned_coordinates = json.dumps(serialized_coordinates.data, indent=4)

    with open('coordinates.json', 'w') as json_file:
        json_file.write(jsoned_coordinates)

    referring_url = request.META.get('HTTP_REFERER')

    if referring_url:
        # Redirect back to the referring page
        return HttpResponseRedirect(referring_url)
    else:
        # If there's no referring URL, redirect to a default page
        return redirect('homepage')


def load_json(request):
    with open('coordinates.json', 'r') as f:
        data = json.load(f)

        # Assuming your JSON structure
        coordinates = data

        # Iterate over the coordinates and save each one
        for coord in coordinates:
            Coordinates.objects.create(
                section=coord['section'],
                lat=coord['lat'],
                long=coord['long'],
                point=coord['point']
            )

    referring_url = request.META.get('HTTP_REFERER')

    if referring_url:
        # Redirect back to the referring page
        return HttpResponseRedirect(referring_url)
    else:
        # If there's no referring URL, redirect to a default page
        return redirect('homepage')
