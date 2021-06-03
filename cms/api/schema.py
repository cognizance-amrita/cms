import graphene
import panel.api.schema

class Query(panel.api.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)