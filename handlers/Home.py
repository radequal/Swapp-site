# -*- coding: utf-8 -*-
from handlers.Jinja2Handler import *

class Handler(Jinja2Handler):

    def root(self):
        session = self.request.session if self.request.session else None
        user = self.request.user if self.request.user else None
        profiles = None
        is_admin = False
        if user:
            profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
            profiles = ndb.get_multi(profile_keys)
            if user.user_type == "admin":
                is_admin = True

        self.render_template('home.html', {
            'user': user,
            'session': session,
            'profiles': profiles,
            'nav_tab_location': "home",
            'is_admin': is_admin,
        })
