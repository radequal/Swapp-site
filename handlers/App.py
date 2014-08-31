# -*- coding: utf-8 -*-
from handlers.Jinja2Handler import *
import logging

class Handler(Jinja2Handler):

    def app_request(self, request_name):
        # Enalbe CORS
        # http://enable-cors.org/server_appengine.html
        # http://stackoverflow.com/questions/18907216/origin-null-is-not-allowed-by-access-control-allow-origin-with-google-app-engine
        self.response.headers['Access-Control-Allow-Origin'] = "*"
        self.response.headers['Access-Control-Allow-Methods'] = "GET, PUT, POST, DELETE, OPTIONS"
        self.response.headers['Access-Control-Max-Age'] = "1000"
        self.response.headers['Access-Control-Allow-Headers'] = "Content-Type, Authorization, X-Requested-With"

        # session = self.request.session if self.request.session else None
        # user = self.request.user if self.request.user else None
        # profiles = None
        # is_admin = False
        # if user:
        #     profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
        #     profiles = ndb.get_multi(profile_keys)
        #     if user.user_type == "admin":
        #         is_admin = True

        geo = self.request.get('geo')
        userId = self.request.get('userId')

        items = list()

        x = 0
        while x != 10:
            x = x + 1
            item = {}
            item['title'] = "Item " + str(x)
            item['img'] = "http://google.com/image-" + str(x) + ".jpg"
            item['distance'] = str(x) + "miles"
            item['description'] = "The description of product " + str(x)
            items.append(item)


        output = {}
        output['items'] = items
        # output = items
        output = json.dumps(output)
        self.response.write(output)

    def app_save_data(self, request_name):
        # Enalbe CORS
        # http://enable-cors.org/server_appengine.html
        # http://stackoverflow.com/questions/18907216/origin-null-is-not-allowed-by-access-control-allow-origin-with-google-app-engine
        self.response.headers['Access-Control-Allow-Origin'] = "*"
        self.response.headers['Access-Control-Allow-Methods'] = "GET, PUT, POST, DELETE, OPTIONS"
        self.response.headers['Access-Control-Max-Age'] = "1000"
        self.response.headers['Access-Control-Allow-Headers'] = "Content-Type, Authorization, X-Requested-With"

        # session = self.request.session if self.request.session else None
        # user = self.request.user if self.request.user else None
        # profiles = None
        # is_admin = False
        # if user:
        #     profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
        #     profiles = ndb.get_multi(profile_keys)
        #     if user.user_type == "admin":
        #         is_admin = True

        if request_name == "main":
            log = Log()
            log.category = request_name
            log.fb_user_id = self.request.get('userId')
            log.fb_user_object = self.request.get('fb_user')
            log.fb_pp_url = self.request.get('fb_pp_url')
            log.fb_cover_url = self.request.get('fb_cover_url')
            log.geo_object = self.request.get('geo_object')
            log.put()

        output = True
        # output = items
        output = json.dumps(output)
        self.response.write(output)
