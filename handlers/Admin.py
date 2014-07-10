# -*- coding: utf-8 -*-
from handlers.Jinja2Handler import *

class Handler(Jinja2Handler):

    def root(self):
        session = self.request.session if self.request.session else None
        user = self.request.user if self.request.user else None
        profiles = None
        if user:
            profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
            profiles = ndb.get_multi(profile_keys)
        if user.user_type == "admin":
            self.redirect('/admin/swapps')
        else:
            self.error(404)
            self.redirect('/404')


    def page(self, page_name):
        session = self.request.session if self.request.session else None
        user = self.request.user if self.request.user else None
        profiles = None
        is_admin = False
        if user:
            profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
            profiles = ndb.get_multi(profile_keys)
        if user.user_type == "admin":
            is_admin = True
        else:
            self.error(404)
            self.redirect('/404')

        self.render_template('admin.html', {
            'user': user,
            'session': session,
            'profiles': profiles,
            'nav_tab_location': 'admin',
            'page_name': page_name,
            'is_admin': is_admin,
        })


    def robots(self):
        self.response.write("""\n
User-agent: *\n
"""
        )
