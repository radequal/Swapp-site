# -*- coding: utf-8 -*-
import webapp2
from webapp2_extras import jinja2
from google.appengine.ext import ndb

import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import re
import json
from webob import Request

from google.appengine.ext import db
from models import *

#upload functionality
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

#password functionality
from hashlib import sha256
from random import random

#generate unique ID
import random
import string

#byte-by-byte comparison
import filecmp

#file download
import urllib2
from google.appengine.api import images
from StringIO import StringIO


def getContentType( filename ): # lists and converts supported file extensions to MIME type
    ext = filename.split('.')[-1].lower()
    if ext == 'jpg' or ext == 'jpeg': return 'image/jpeg'
    if ext == 'png': return 'image/png'
    if ext == 'gif': return 'image/gif'
    if ext == 'svg': return 'image/svg+xml'
    if ext == 'xml': return 'text/xml'
    return None

def genPassword( plain_password ):
    #random_key = random()
    #hashed_password = sha256('%s%s%s'%('-vdgqumje*6_@&81_&9o)nlsup_a5r2f6^(g(ta@b+_^ej+7fn',random_key,plain_password))
    hashed_password = sha256(plain_password).hexdigest()
    return hashed_password;

def genPermalink( permalink ):
    permalink = permalink.replace(" ", "-")
    permalink = re.sub("[ +?$@]", "-", permalink)
    permalink = re.sub("[&]", "and", permalink)
    permalink = permalink.lower()
    return permalink

def genId(size=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + "_"):    
    dupe_unique_id_count = 1
    while (dupe_unique_id_count != 0):
        unique_id = ''.join(random.choice(chars) for x in range(size))
        dupe_unique_id_count = BlobFiles.query(BlobFiles.unique_id == unique_id).count()
    return unique_id

def getCategories(input_cat):
    categories = [
        ['hot-topics', 'Hot topics'],
        ['current-affairs', 'Current affairs'],
        ['world-news', 'World news'],
        ['business-and-finance', 'Business &amp; Finance'],
        ['industries', 'Industries'],
        ['technology', 'Technology'],
        ['science', 'Science'],
        ['sport', 'Sport'],
        ['lifestyle', 'Lifestyle'],
        ['entertainment', 'Entertainment &amp; Arts'],
        ['local', 'Local'],
    ]
    categoryParameters = {}
    categoryParameters['category_array'] = list()
    for permalink, name in categories:
        cat_array = [permalink, name]
        categoryParameters['category_array'].append(cat_array)
        if permalink == input_cat:
            categoryParameters['permalink'] = permalink
            categoryParameters['name'] = name
    return categoryParameters

def getLanguage(language):
    languages = [
        ['en', 'English', 'English'],
        ['it', 'Italian', 'Italiano'],
        ['es', 'Spanish', 'Espa&ntilde;ol'],
    ]
    languageParameters = {}
    languageParameters['language_array'] = list()
    for iso, english_name, native_name in languages:
        lang_array = [iso, english_name, native_name]
        languageParameters['language_array'].append(lang_array)
        if iso == language:
            languageParameters['iso'] = iso
            languageParameters['english_name'] = english_name
            languageParameters['native_name'] = native_name
    return languageParameters

def getCity(city):
    cities = [
        ['london', 'London, UK'],
        ['dublin', 'Dublin, IE'],
        ['new-york', 'New York, US'],
    ]
    cityParameters = {}
    cityParameters['city_array'] = list()
    for permalink, name in cities:
        city_array = [permalink, name]
        cityParameters['city_array'].append(city_array)
        if permalink == city:
            cityParameters['permalink'] = permalink
            cityParameters['name'] = name
    return cityParameters

def listOfSections():
    sections = [
        ['live', '/', 'Home', 'user', ''],
        ['live', '/news', 'News', 'user',
                        [
                            ['live', '/news/viral', 'Viral', 'user'],
                            ['live', '/news/world', 'World', 'user'],
                            ['live', '/news/africa', 'Africa', 'user'],
                            ['live', '/news/asia', 'Asia', 'user'],
                            ['live', '/news/europe', 'Europe', 'user'],
                            ['live', '/news/latin-america', 'Latin America', 'user'],
                            ['live', '/news/middle-east', 'Middle East', 'user'],
                            ['live', '/news/us-and-canada', 'US & Canada', 'user'],
                        ]
        ],
        ['draft', '/sport', 'Sport', 'user',
                        [
                            ['draft', '/sport/football', 'Football', 'user'],
                            ['draft', '/sport/tennis', 'Tennis', 'user'],
                            ['draft', '/sport/formula-1', 'Formula 1', 'user'],
                        ]

        ],
        ['draft', '/local', 'Local', 'user', ''],
        ['draft', '/travel', 'Travel', 'user', ''],
        ['draft', '/weather', 'Weather', 'user', ''],
        ['draft', '/autos', 'Autos', 'user', ''],
        ['draft', '/food', 'Food', 'user', ''],
        ['draft', '/health', 'Health', 'user', ''],
        ['draft', '/education', 'Education', 'user', ''],
        ['draft', '/gossip', 'Gossip', 'user', ''],
        ['admin', '/admin', 'Admin', 'suparadmin',
                        [
                            ['live', '/admin/scrape', 'Scrape', 'superadmin'],
                            ['live', '/admin/rss', 'RSS Feeds', 'superadmin'],
                            ['live', '/admin/robots', 'Robots', 'superadmin'],
                        ]
        ],
    ]
    return sections

def navbarItems(navPath):
    sections = listOfSections()
    navbar = {}
    navbar['parents'] = list()
    navbar['submenu'] = list()
    for status, path, title, permission, submenu in sections:
        menu_item = [status, path, title, permission]
        navbar['parents'].append(menu_item)
        if navPath == path and submenu:
            for status, path, title, permission in submenu:
                sub_menu_item = [status, path, title, permission]
                navbar['submenu'].append(sub_menu_item)

    return navbar

def getPageDetails( sectionPath, subsectionPath ):
    sections = listOfSections()
    page_titles = list()
    page = {}
    for status, path, title, permission, submenu in sections:
        if path == sectionPath:
            page['section_status'] = status
            page['section_path'] = path
            page['section_title'] = title
            page['section_permission'] = permission
        if submenu and path == sectionPath:
            for status, path, title, permission in submenu:
                if path == subsectionPath:
                    page['subsection_status'] = status
                    page['subsection_path'] = path
                    page['subsection_title'] = title
                    page['subsection_permission'] = permission
            break
    return page

class Jinja2Handler(webapp2.RequestHandler):
    """
        BaseHandler for all requests all other handlers will
        extend this handler

    """
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, template_name, template_values={}):
        self.response.write(self.jinja2.render_template(
            template_name, **template_values))

    def render_string(self, template_string, template_values={}):
        self.response.write(self.jinja2.environment.from_string(
            template_string).render(**template_values))

    def json_response(self, json):
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(json)