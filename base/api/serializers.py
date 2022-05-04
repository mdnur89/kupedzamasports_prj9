from rest_framework.serializers import ModelSerializer
from base.models import Team, User


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"
        

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name','email', 'points')
