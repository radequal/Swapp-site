from engineauth import models
from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.api import users

class CustomUser(models.User):
    user_type = ndb.StringProperty(default="user")
    @classmethod
    def _get_kind(cls):
        return 'EAUser'

class BlobFiles(ndb.Model):
    unique_id = ndb.StringProperty()
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    data = ndb.BlobProperty()
    mimetype = ndb.StringProperty()
    extension = ndb.StringProperty()
    created_by = ndb.KeyProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    created_ip = ndb.StringProperty()
    privacy = ndb.StringProperty(default="link") #link, public, private

class Swapps(ndb.Model):
    uid = ndb.StringProperty()
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    img = ndb.StructuredProperty(BlobFiles, repeated=True)

    created_by = ndb.KeyProperty()
    created_geo = ndb.GeoPtProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    created_ip = ndb.StringProperty()

    approved = ndb.BooleanProperty(default=False)
    approved_by = ndb.KeyProperty()