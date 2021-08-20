import graphene
import panel.api.schema

class Query(panel.api.schema.Query, graphene.ObjectType):
    submission = graphene.Field(panel.api.schema.Sub)
class Mutation(panel.api.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)