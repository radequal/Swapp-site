# -*- coding: utf-8 -*-
from handlers.Jinja2Handler import *

class Handler(Jinja2Handler):

    def root(self, page_name):
        session = self.request.session if self.request.session else None
        user = self.request.user if self.request.user else None
        profiles = None
        is_admin = False
        if user:
            profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
            profiles = ndb.get_multi(profile_keys)
            if user.user_type == "admin":
                is_admin = True

        page = {}
        nav_tab_location = None
        if page_name == "about":
            page['title'] = "About"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://swapp-site.appspot.com">Swapp</a></p>
            """
            nav_tab_location = "about"
        elif page_name == "help":
            page['title'] = "Help"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://swapp-site.appspot.com">Swapp</a></p>
            """
            nav_tab_location = "help"
        elif page_name == "contact":
            page['title'] = "Contact"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://swapp-site.appspot.com">Swapp</a></p>
            """
            nav_tab_location = "contact"
        elif page_name == "advertisers":
            page['title'] = "Advertisers"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://swapp-site.appspot.com">Swapp</a></p>
            """
            nav_tab_location = "advertisers"
        elif page_name == "privacy":
            page['title'] = "Privacy Policy"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://swapp-site.appspot.com">Swapp</a></p>
            """
            nav_tab_location = "privacy"
        elif page_name == "terms":
            page['title'] = "Terms of Service"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://swapp-site.appspot.com">Swapp</a></p>
            """
            nav_tab_location = "terms"
        elif page_name == "faqs":
            page['title'] = "FAQs"
            page['meta'] = """<meta name="robots" contant="index, follow">"""
            page['body'] = """
                            <p>hi</p>
            """
            nav_tab_location = "faqs"
        elif page_name == "download":
            page['title'] = "You can download the app from your app store"
            page['meta'] = """<meta name="robots" contant="index, follow">"""
            page['body'] = """
                            <p>hi</p>
            """
            nav_tab_location = "download"
        else:
            self.error(404)
            self.redirect('/404')

        self.render_template('static-page.html', {
            'user': user,
            'session': session,
            'profiles': profiles,
            'is_admin': is_admin,
            'nav_tab_location': nav_tab_location,
            'page': page,
        })
