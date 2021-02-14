import graphene
from graphene_django import DjangoObjectType
from typing import Type, Optional
from .models import Track
from users.models import User


class TrackType(DjangoObjectType):
    class Meta:
        model = Track


class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)
    track = graphene.Field(TrackType, id=graphene.UUID(required=True))

    def resolve_tracks(self, info):
        return Track.objects.all()

    def resolve_track(self, info, id):
        return Track.objects.get(id=id)


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title: str, description: str, url: str):
        user: Type[User] = info.context.user

        if(user.is_anonymous):
            raise Exception('Please login to create a track.')

        track = Track(title=title, description=description,
                      url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()
        track_id = graphene.UUID(required=True)

    def mutate(
        self,
        info,
        track_id: str,
        title: Optional[str] = None,
        url: Optional[str] = None,
        description: Optional[str] = None
    ):
        user: Type[User] = info.context.user
        track: Type[Track] = Track.objects.get(id=track_id)

        if(user.is_anonymous):
            raise Exception('Please log in to update track.')
        # https://realpython.com/python-is-identity-vs-equality/
        if(track.posted_by != user):
            raise Exception('You are not the owner of this track.')

        if(title):
            track.title = title
        if(description):
            track.description = description
        if(url):
            track.url = url

        track.save()

        return UpdateTrack(track=track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.UUID()

    class Arguments:
        track_id = graphene.UUID(required=True)

    def mutate(self, info, track_id):
        user: Type[User] = info.context.user
        track: Type[Track] = Track.objects.get(id=track_id)

        if(track.posted_by != user):
            raise Exception('You are not the owner of this track.')

        track.delete()

        return DeleteTrack(track_id=track_id)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
