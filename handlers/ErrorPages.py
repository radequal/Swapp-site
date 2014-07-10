# -*- coding: utf-8 -*-
from handlers.Jinja2Handler import *

class Handler(Jinja2Handler):

    def root(self, error_id):
        session = self.request.session if self.request.session else None
        user = self.request.user if self.request.user else None
        profiles = None
        if user:
            profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
            profiles = ndb.get_multi(profile_keys)
        navbar = navbarItems('')

        page = {}
        if error_id == "404":
            page['title'] = ""
            page['body'] = """
                        <div class="row-fluid">
                            <div class="span6">
                                <div class="vertical100"></div>
                                <p class="lead">202 + 202</p>
                                <h1>404 Error</h1>
                                <p>The page you're looking for doesn't exist.</p>
                            </div>
                            <div class="span6">
                                <img src="/static/img/404.gif" >
                            </div>
                        </div>
            """
            self.error(404)

        self.render_template('static-page.html', {
            'user': user,
            'session': session,
            'profiles': profiles,
            'navbar': navbar,
            'page': page,
        })

    def redirect(self, url):
        self.error(404)
        self.redirect('/404')
