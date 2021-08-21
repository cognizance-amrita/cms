import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from panel.models import *
import graphql_jwt

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class MemberType(DjangoObjectType):
    class Meta:
        model = Member

class TaskType(DjangoObjectType):
    class Meta:
        model = Task

class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department

class RoleType(DjangoObjectType):
    class Meta:
        model = Role

class PositionType(DjangoObjectType):
    class Meta:
        model = Position

class DomainType(DjangoObjectType):
    class Meta:
        model = Domain

class DomainMemberType(DjangoObjectType):
    class Meta:
        model = DomainMember

class ApplicationType(DjangoObjectType):
    class Meta:
        model = Application

class AchievementType(DjangoObjectType):
    class Meta:
        model = Achievement

class SubmissionType(DjangoObjectType):
    class Meta:
        model = Submission

class Query(graphene.ObjectType):
    members = graphene.List(MemberType)
    tasks = graphene.List(TaskType)
    department = graphene.List(DepartmentType)
    role = graphene.List(RoleType)
    position = graphene.List(PositionType)
    domain = graphene.List(DomainType)
    domainmember = graphene.List(DomainMemberType)
    application = graphene.List(ApplicationType)
    achievement = graphene.List(AchievementType)
    submission = graphene.List(SubmissionType)

    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
            return
        return user

    def resolve_members(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
            return
        return Member.objects.all()
    
    def resolve_tasks(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
            return
        return Task.objects.all()
    
    def resolve_departments(self,info,**kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
            return
        return Department.objects.all()

    def resolve_role(self,info,**kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
            return
        return Role.objects.all()

    def resolve_position(self,info,**kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
            return
        return Position.objects.all()

    def resolve_domain(self,info,**kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
            return
        return Domain.objects.all()

    def resolve_domainmember(self,info,**kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
            return
        return DomainMember.objects.all()

    def resolve_application(self,info,**kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
            return
        return Application.objects.all()

    def resolve_submission(self,info,**kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
            return
        return Submission.objects.all()

class Sub(graphene.ObjectType):
   task_id = graphene.Int()
   candidate_gitname = graphene.String()
   submission_link = graphene.String()
   submission_text = graphene.String()
   feedback = graphene.String() 

class SubmissionData(graphene.InputObjectType):
   task_id = graphene.Int()
   candidate_gitname = graphene.String()
   submission_link = graphene.String()
   submission_text = graphene.String()
   feedback = graphene.String() 

class AddSubmission(graphene.Mutation):

   class Arguments:
       data = SubmissionData(required=True)
   submission = graphene.Field(Sub)
   def mutate(root, info, data=None):
       candidate = Member.objects.get(github_username=data.candidate_gitname)
       submission = Submission(
           task_id=data.task_id,
           candidate=candidate,
           submission_link=data.submission_link,
           submission_text=data.submission_text,
           feedback=data.feedback    
       )
       submission.save()
       return AddSubmission(submission = submission)

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    add_submission = AddSubmission.Field()
