"""This module contains a marshmallow schema used to serialize and
deserialize Community models.
"""


from app.extensions import ma
from marshmallow import validate, EXCLUDE, pre_load
from app.models.community import CommunityTopic
from app.schemas.image import ImageSchema
from app.schemas.location import LocationSchema
from app.schemas.enum_field import EnumField


class CommunitySchema(ma.Schema):
    """Class to serialize and deserialize Community models."""

    COLLECTION_NAME = "communities"
    RESOURCE_NAME = "community"

    class Meta:
        unknown = EXCLUDE

    _id = ma.UUID(data_key="id", dump_only=True)
    name = ma.Str(required=True, validate=validate.Length(min=1, max=64))
    description = ma.Str(required=True, validate=validate.Length(min=1, max=280))
    topic = EnumField(CommunityTopic)
    avatar = ma.Nested(ImageSchema, dump_only=True)
    cover_photo = ma.Nested(ImageSchema, dump_only=True)
    location = ma.Nested(LocationSchema, required=True)
    _founder_id = ma.UUID(dump_only=True, data_key="founder_id")
    _created_at = ma.DateTime(
        data_key="founded_on", dump_only=True
    )  # defaults to ISO 8601
    resource_type = ma.Str(default="Community", dump_only=True)

    # Links
    self_url = ma.URLFor("api.get_community", community_id="<_id>")
    founder_url = ma.URLFor("api.get_user", user_id="<_founder_id>")
    members_url = ma.URLFor("api.get_community_members", community_id="<_id>")
    group_chats_url = ma.URLFor("api.get_community_group_chats", community_id="<_id>")

    @pre_load
    def strip_unwanted_fields(self, data, many, **kwargs):
        """Remove unwanted fields from the input data before deserialization."""
        unwanted_fields = ["resource_type"]
        for field in unwanted_fields:
            if field in data:
                data.pop(field)
        return data

