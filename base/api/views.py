from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Team, User
from .serializers import TeamSerializer
from base.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/teams',
        'GET /api/teams/:id'
        'GET /api/users',
        'GET /api/users/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getTeams(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTeam(request, pk):
    team = Team.objects.get(id=pk)
    serializer = TeamSerializer(team, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getUsers(request):
    teams = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
