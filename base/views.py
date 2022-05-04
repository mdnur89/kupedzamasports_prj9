from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Team, Project, Message, User, Incident
from .forms import TeamForm, UserForm, MyUserCreationForm, IncidentForm

# Create your views here.

# teams = [
#     {"id":1, "name":"Team 1"},
#     {"id":2, "name":"Team 2"},
#     {"id":3, "name":"Team 3"},
#     {"id":4, "name":"Team 4"},
#     {"id":5, "name":"Team 5"},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    teams = Team.objects.filter(
        Q(project__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    projects = Project.objects.all()[0:5]
    team_count = teams.count()
    team_messages = Message.objects.filter(
        Q(team__project__name__icontains=q))[0:3]

    context = {'teams': teams, 'projects': projects,
               'team_count': team_count, 'team_messages': team_messages}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def team(request, pk):
    team = Team.objects.get(id=pk)
    team_messages = team.message_set.all()
    participants = team.participants.all()
    #team_points = team.team_points.all()
    team_climate = team.team_climate._meta.get_fields()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            team=team,
            body=request.POST.get('body')
        )
        team.participants.add(request.user)
        return redirect('team', pk=team.id)

    context = {'team': team, 'team_messages': team_messages,
               'participants': participants, 'team_climate': team_climate}
    return render(request, 'base/team.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    teams = user.team_set.all()
    team_messages = user.message_set.all()
    projects = Project.objects.all()
    points = User.objects.all()
    context = {'user': user, 'points': points, 'teams': teams,
               'team_messages': team_messages, 'projects': projects}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createTeam(request):
    form = TeamForm()
    projects = Project.objects.all()
    if request.method == 'POST':
        project_name = request.POST.get('project')
        project, created = Project.objects.get_or_create(name=project_name)

        Team.objects.create(
            host=request.user,
            project=project,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'projects': projects}
    return render(request, 'base/team_form.html', context)


@login_required(login_url='login')
def updateTeam(request, pk):
    team = Team.objects.get(id=pk)
    form = TeamForm(instance=team)
    projects = Project.objects.all()
    if request.user != team.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        project_name = request.POST.get('project')
        project, created = Project.objects.get_or_create(name=project_name)
        team.name = request.POST.get('name')
        team.project = project
        team.description = request.POST.get('description')
        team.team_climate = request.POST.get('team_climate')
        team.save()
        return redirect('home')

    context = {'form': form, 'projects': projects, 'team': team}
    return render(request, 'base/team_form.html', context)


@login_required(login_url='login')
def deleteTeam(request, pk):
    team = Team.objects.get(id=pk)

    if request.user != team.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        team.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': team})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

@login_required(login_url='login')
def projectsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    projects = Project.objects.filter(name__icontains=q)
    
    return render(request, 'base/projects.html', {'projects': projects})


def activityPage(request):
    team_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'team_messages': team_messages})

@login_required(login_url='login')
def incidentsPage(request, pk):
    incident = Incident.objects.get(id=pk)
    incident_type = incident.message_set.all()
    description = incident.description.all()
    platform_used = incident.reporting_medium.all()
    foul_on = incident.ball_dropper.all()

    if request.method == 'POST':
        incident = Incident.objects.create(
            incident_type=request.incident_type,
            reporting_medium=request.reporting_medium,
            description=description,
            ball_dropper=request.user
        )
        name.incident_type.add(request.user)
        return redirect('home')

    context = {'incident_type': incident_type, 'ball_dropper': ball_dropper}
    return render(request, 'base/incident.html', context)