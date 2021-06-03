import graphene
from graphene_django import DjangoObjectType
from panel.models import Member, Task

class MemberType(DjangoObjectType):
    class Meta:
        model = Member

class TaskType(DjangoObjectType):
    class Meta:
        model = Task

class Query(graphene.ObjectType):
    members = graphene.List(MemberType)
    tasks = graphene.List(TaskType)

    def resolve_members(self, info, **kwargs):
        return Member.objects.all()
    
    def resolve_tasks(self, info, **kwargs):
        return Task.objects.all()