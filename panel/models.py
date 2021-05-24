from cms.settings.base import DISCORD_CHANNEL, DISCORD_GUILD, DISCORD_TOKEN
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from panel.utils.discord import Discord

class Department(models.Model):
    name = models.CharField(max_length=100, primary_key=True, default='')
    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100, primary_key=True, default='')
    from_date = models.DateTimeField(auto_now_add=True)
    discord_role_id = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=100, primary_key=True, default='')
    from_date = models.DateTimeField(auto_now_add=True)
    discord_role_id = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.name

class Member(models.Model):
    years = (
        ('I year', 'I year'),
        ('II year', 'II year'),
        ('III year', 'III year'),
        ('IV year', 'IV year'),
    )
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    academic_year = models.CharField(choices=years, max_length=100, null=True)
    discord_id = models.CharField(max_length=50, null=True)
    github_username = models.CharField(max_length=200, primary_key=True, default='')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    positions = models.ManyToManyField(Position)
    phone = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.first_name + self.last_name

class Domain(models.Model):
    name = models.CharField(max_length=50, primary_key=True, default='')
    coordinators = models.ManyToManyField(Member, related_name='coordinators')
    mentors = models.ManyToManyField(Member, related_name='mentors')

    def __str__(self):
        return self.name

class DomainMember(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True, default='')
    domain = models.ManyToManyField(Domain)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member.first_name + self.member.last_name
    

class Application(models.Model):

    years = (
        ('I year', 'I year'),
        ('II year','II year'),
        ('III year','III year'),
        ('IV year','IV year')
    )
    
    statuses = (
        ('Under review','Under review'),
        ('Accepted','Accepted'),
        ('Rejected','Rejected')
    )
    
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, primary_key=True, default='')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    domain = models.ManyToManyField(Domain)
    ques1 = models.TextField(max_length=400, null=True)
    writeup = models.TextField(max_length=1000, null=True)
    ac_year = models.CharField(max_length=20, null=True, choices=years)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, null=True, choices=statuses)
    experience = models.TextField(max_length=500, null=True)
    reviewer = models.ForeignKey(Member, on_delete=models.CASCADE)
    tasksrepo = models.URLField(max_length=200, null=True)
    discord_id = models.CharField(max_length=50, null=True)
    github_username = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.first_name + self.last_name

class Achievement(models.Model):

    title = models.CharField(max_length=200, null=True)
    content = models.CharField(max_length=1000, null=True)
    achievers = models.ManyToManyField(Member)
    image = models.ImageField(null=True, upload_to='Achievements')
    date = models.DateField(primary_key=True, default='')
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True)
    goal = models.CharField(max_length=500, null=True)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, null=True)
    deadline = models.DateTimeField(null=True)
    starting_time = models.DateTimeField(null=True)
    max_score = models.FloatField(null=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    resource_file = models.FileField(null=True)

    def __str__(self):
        return self.title

class Submission(models.Model):
     
    task_id = models.IntegerField(null=True)
    username = models.CharField(max_length=200, primary_key=True, default='')
    score = models.FloatField(max_length=50, null=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
    submission_file = models.FileField(null=True)
    submission_text = models.CharField(max_length=500, null=True)
    evaluator = models.ForeignKey(Member, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=500, null=True)
    
    def __str__(self):
        return self.username

# DJANGO SIGNALS 

@receiver(post_save, sender=Member)
def createUser(sender, instance, **kwargs):
    if User.objects.get(email=instance.email) == None:
        user = User.objects.create(
        email=instance.email,
        date_joined=instance.join_date,
        password='admin123',
        first_name=instance.first_name,
        last_name=instance.last_name,
        username=(instance.first_name + '_' + instance.last_name).lower()
        )
        # Discord client
        obj = []
        obj.append(DISCORD_TOKEN) #Token
        obj.append(DISCORD_GUILD) #Guild
        obj.append(DISCORD_CHANNEL) #Channel
        msg = '<@!'+ instance.discord_id +'>'+ ' is now an official member of the club :star:'
        client = Discord(obj=obj, message=msg)
        client.sendMessage()

@receiver(pre_delete, sender=Member)
def kickUser(sender, instance, **kwargs):
    username=(instance.first_name + '_' + instance.last_name).lower()
    user = User.objects.get(username=username)
    user.delete()
    # Discord client
    obj = []
    obj.append(DISCORD_TOKEN) #Token
    obj.append(DISCORD_GUILD) #Guild
    obj.append(DISCORD_CHANNEL) #Channel
    discord_id = str(instance.discord_id) #Get ID of the user
    msg = instance.first_name + ' ' + instance.last_name + ' is kicked out from the club ⚠️'
    client = Discord(obj=obj, message=msg, userID=discord_id)
    client.kickMember()
    client.sendMessage()