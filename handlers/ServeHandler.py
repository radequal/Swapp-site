# -*- coding: utf-8 -*-
from handlers.Jinja2Handler import *

class Handler(Jinja2Handler):

    def get(self,key):
      session = self.request.session if self.request.session else None
      user = self.request.user if self.request.user else None
      profiles = None
      if user:
          profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
          profiles = ndb.get_multi(profile_keys)

          current_user_key = user.key.urlsafe()
      else:
          current_user_key = None
      BlobFile = None
      try:
        # BlobFile = BlobFiles.get( key )
        BlobFile = ndb.Key(urlsafe=key).get()

        if not BlobFile: raise "Not found"
        if BlobFile.privacy == "private":
          self.response.headers['X-Robots-Tag:'] = "none, noindex, nofollow, noarchive, nosnippet, noodp, notranslate, noimageindex"
          if not current_user_key:
            raise "You don't have permission to view this image"
          if current_user_key != BlobFile.created_by.urlsafe():
            raise "You don't have permission to view this image"
      except:
        self.error(404)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write( "Could not find image: '%s'" % id )
        return

      dl = self.request.get('dl') # optionally download as attachment
      if dl=='1' or dl=='true':
        self.response.headers['Content-Disposition'] = 'attachment; filename="%s"' % str(BlobFile.name)

      self.response.headers['Content-Type'] = str(BlobFile.mimetype)
      self.response.out.write( BlobFile.data )