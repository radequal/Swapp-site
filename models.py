from engineauth import models
from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.api import users

class CustomUser(models.User):
    user_type = ndb.StringProperty(default="user")

    delete_request = ndb.BooleanProperty(default=False)

    # User data
    # email = ndb.StringProperty()
    # first_name = ndb.StringProperty()
    # last_name = ndb.StringProperty()
    # full_name = ndb.StringProperty()
    # locale = ndb.StringProperty()
    @classmethod
    def _get_kind(cls):
        return 'EAUser'

class Images(ndb.Model):
    uid = ndb.StringProperty()
    size = ndb.StringProperty()
    data = ndb.BlobProperty()
    mimetype = ndb.StringProperty()
    extension = ndb.StringProperty()

    created_by = ndb.KeyProperty()
    created_geo = ndb.GeoPtProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    created_ip = ndb.StringProperty()


class Items(ndb.Model):
    uid = ndb.StringProperty()

    # User input
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    category = ndb.KeyProperty(repeated=True)
    tags = ndb.StringProperty(repeated=True)
    images = ndb.StructuredProperty(Images, repeated=True)

    # Meta info
    created_by = ndb.KeyProperty()
    created_geo = ndb.GeoPtProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    created_ip = ndb.StringProperty()

    approved = ndb.BooleanProperty(default=False)
    approved_by = ndb.KeyProperty()


class Categories(ndb.Model):
    uid = ndb.StringProperty()
    name = ndb.StringProperty()

    created_by = ndb.KeyProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    created_ip = ndb.StringProperty()

class Log(ndb.Model):
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    category = ndb.StringProperty()
    fb_user_id = ndb.StringProperty(required=True)
    fb_user_object = ndb.JsonProperty()
    fb_pp_url = ndb.StringProperty()
    fb_cover_url = ndb.StringProperty()
    geo_object = ndb.JsonProperty()


