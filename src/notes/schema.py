from graphene_django import DjangoiObjectType
import graphene
from .models import PersonalNote as PersonalNoteModel


class PersonalNote(DjangoiObjectType):

    class Meta:
        model = PersonalNoteModel
        # describe data as a node.
        interface = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    notes = graphene.List(PersonalNote)

    def resolve_notes(self, info):
        # decide which notes to return
        user = info.context.user

        if user.is_anonymous:
            return PersonalNoteModel.objects.none()
        else:
            return PersonalNoteModel.objects.filter(user=user)


schema = graphene.Schema(query=Query)