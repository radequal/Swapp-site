# -*- coding: utf-8 -*-
import sys
import os
import re
import webapp2
from webapp2 import Route
from webapp2_extras import routes
import os
from jinja2.filters import do_pprint

if 'lib' not in sys.path:
    sys.path[0:0] = ['lib']

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

routes = [
    #Home
    Route('/', 'handlers.Home.Handler:root'),

    #Static pages
    Route('/p/<page_name>', 'handlers.StaticPages.Handler:root'),

    #Error pages
    Route('/<error_id:\d{3}>', 'handlers.ErrorPages.Handler:root'),
    Route(r'/logout', handler='handlers.GlobalHandlers.Handler:logout'),    

    # App requests
    Route(r'/app/request/<request_name>', handler='handlers.App.Handler:app_request'),    
    Route(r'/app/save/<request_name>', handler='handlers.App.Handler:app_save_data'),    

    #FileServe
    Route(r'/serve/<key>.<extension>', handler='handlers.ServeHandlerWithExtension.Handler'),
    Route(r'/serve/<key>', handler='handlers.ServeHandler.Handler'),
    Route(r'/data/<id>/<filename>', handler='handlers.ServeHandler.ServeHandler'),

    #Admin
    Route('/admin', 'handlers.Admin.Handler:root'),
    Route('/admin/<page_name>', 'handlers.Admin.Handler:page'),

    #ACTIONS
    # Route('/actions/upload-file', 'handlers.Upload.Handler:add_file'),
    # Route('/actions/replace-file', 'handlers.Upload.Handler:replace_file'),
    # Route('/actions/change-privacy', 'handlers.Upload.Handler:change_privacy'),

    #Sections
    #Route('/<section>', 'handlers.SectionHomePages.Handler:root'),
    #Route('/<section>/<subsection>', 'handlers.Subsection.Handler:root'),

    #Story pages
    #Route('/<section>/<subsection>/<permalink>-<story_id:\w+>', 'handlers.News.Story.Handler:root'),




    #All other URLs
    Route('/<url:*>', 'handlers.ErrorPages.Handler:redirect'),

]

# routes = [
#     #HOME
#     Route(r'/home', handler='handlers.HomeHandler.Handler:root', strict_slash=True),

#     #FileServe
#     Route(r'/serve/<key>', handler='handlers.ServeHandler.Handler'),
#     Route(r'/data/<id>/<filename>', handler='handlers.ServeHandler.Handler'),

#     Route(r'/logout', handler='handlers.MiscHandlers.GlobalHandler:logout'),
#     ]

config = {
    'webapp2_extras.sessions': {
        'secret_key': 'snfglksnalgknslkdnglkasnflgknlsanfgal'
        #'secret_key': 'wIDjEesObzp5nonpRHDzSp40aba7STuqC6ZRY'
    },
    'webapp2_extras.auth': {
        'user_model': 'models.User',
        'user_attributes': ['displayName', 'email'],
        },
    'webapp2_extras.jinja2': {
        'filters': {
            'do_pprint': do_pprint,
            },
        },
    }


application = webapp2.WSGIApplication(routes, debug=DEBUG, config=config)