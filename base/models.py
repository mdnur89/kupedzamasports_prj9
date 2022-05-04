from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=50, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    points = models.PositiveIntegerField(default=100, validators=[MinValueValidator(1), MaxValueValidator(200)])
    
    def get_special_combination_value(self):
        return '{}{}{}'.format(self.name, self.email, self.points)

    # def __str__(self):
    #     return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    warcry = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    #team_wins = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], null=True)
    team_points = models.PositiveIntegerField(default=150, validators=[MinValueValidator(1), MaxValueValidator(1000)], null=True)
    #teamclimate = models.CharField(max_length=10, choices=CLIMATES, default="level 2")
    team_fouls = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], null=True)
    CLIMATES = [("level 1", "Cold"), ("level 2", "Normal"), ("level 3", "On Fire"), ("level 4", "Most Wanted"), ("level 5", "Most Valuable Players")]

    team_climate = models.CharField(
        max_length=10, choices=CLIMATES, default="level 2"
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Incident(models.Model):
    incident_type = models.SmallAutoField(db_column='incident_type', primary_key=True) # Field name made lowercase.
    description = models.TextField(null=False, blank=False)

    name = models.CharField(max_length=300, blank=True, null=True)
    
    ball_dropper = models.ForeignKey(User, on_delete=models.CASCADE)
    PLATFORM = [("whatsapp", "WhatsApp"), ("sasai", "Sasai"), ("phone call", "Phone Call"), ("sms", "SMS"), ("social media or email", "Social Media or Email")]

    reporting_medium = models.CharField(
        max_length=21, choices=PLATFORM, default="whatsapp"
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
        db_table = 'incident_type'        
        
    def create(self):
        self.save()
    
    @property
    def get_special_combination_value(self):
        return '{}{}{}{}'.format(self.name, self.incident_type, self.reporting_medium, self.description)

    def __str__(self):
        return self.incident_type
    
    