from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Team, User, Incident


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio', 'points']
        
        
class IncidentForm(ModelForm):
    class Meta:
        model = Incident
        fields = ['incident_type', 'name', 'description', 'ball_dropper', 'reporting_medium']
