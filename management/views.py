from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Trees, Section, Lot, Geolocation
from .serializers import TreesSerializer, LotSerializer, SectionSerializer, GeolocationSerializer
from django.utils import timezone


def homepage(request):
    return render(request, 'base.html', {

    })


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
            'Endpoint': '/location/id/',
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
            'Endpoint': '/add/location/tree/',
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
            'Endpoint': '/delete/geolocation/id/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes a geolocation object'
        },
    ]
    return Response(routes)


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
        section=data['section'],
    )
    serializer = LotSerializer(lot, many=False)
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


# Update/Edit object
@api_view(['PUT'])
def update_tree(request, id):
    tree = Trees.objects.get(id=id)
    # edited_tree = tree.name = data['name']
    serializer = TreesSerializer(tree, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


# delete objects view function
@api_view(['DELETE'])
def delete_tree(request, id):
    tree = Trees.objects.get(id=id)
    tree.delete()
    return Response('Tree deleted')
