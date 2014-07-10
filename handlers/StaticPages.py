# -*- coding: utf-8 -*-
from handlers.Jinja2Handler import *

class Handler(Jinja2Handler):

    def root(self, page_name):
        session = self.request.session if self.request.session else None
        user = self.request.user if self.request.user else None
        profiles = None
        if user:
            profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
            profiles = ndb.get_multi(profile_keys)

        page = {}
        if page_name == "about":
            page['title'] = "About"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://imagineurl.appspot.com">Imagine URL</a></p>
            """
        elif page_name == "help":
            page['title'] = "Help"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://imagineurl.appspot.com">Imagine URL</a></p>
            """
        elif page_name == "contact":
            page['title'] = "Contact"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://imagineurl.appspot.com">Imagine URL</a></p>
            """
        elif page_name == "advertisers":
            page['title'] = "Advertisers"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://imagineurl.appspot.com">Imagine URL</a></p>
            """
        elif page_name == "privacy":
            page['title'] = "Privacy Policy"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://imagineurl.appspot.com">Imagine URL</a></p>
            """
        elif page_name == "terms":
            page['title'] = "Terms of Service"
            page['body'] = """
                            <p>Stay tuned to find out more about <a href="http://imagineurl.appspot.com">Imagine URL</a></p>
            """
        elif page_name == "mime-types":
            page['title'] = "Mime Types"
            page['body'] = """
                            <p>We are increasing support for different file types. At the moment you can upload images only. See below what we support:</p>
                            <ul>
                                <li>JPG, JPEG</li>
                                <li>PNG</li>
                                <li>GIF</li>
                                <li>SVG</li>
                            </ul>
            """
        elif page_name == "file-too-big":
            page['title'] = "Sorry, this file is too big!!"
            page['meta'] = """<meta name="robots" contant="noindex, nofollow">"""
            page['body'] = """
                            <div class="row-fluid">
                                <div class="span8">
                                    <p>We limit file uploads to 1 MB.</p>
                                    <p class="lead">Try again:</p>
                                    <div class="masthead">
                                        <form class="form-inline" action="/actions/upload-file" method="post" enctype="multipart/form-data">
                                          <input type="file" class="input input-xlarge" name="file">
                                          <input type="submit" class="btn btn-primary" value="Upload">
                                        </form>
                                    </div>
                                </div>
                                <div class="span4">
                                    <img src="/static/img/too-heavy.png">
                                </div>
                            </div>
            """
        elif page_name == "unsupported-mime-type":
            page['title'] = "Sorry, this file not yet supported"
            page['meta'] = """<meta name="robots" contant="noindex, nofollow">"""
            page['body'] = """
                            <div class="row-fluid">
                                <div class="span8">
                                    <p>Currently we only allow certain image files on to the site. Read more about which file types we support <a href="/t/mime-types">here</a>.</p>
                                    <p class="lead">Try again:</p>
                                    <div class="masthead">
                                        <form class="form-inline" action="/actions/upload-file" method="post" enctype="multipart/form-data">
                                          <input type="file" class="input input-xlarge" name="file">
                                          <input type="submit" class="btn btn-primary" value="Upload">
                                        </form>
                                    </div>
                                </div>
                                <div class="span4">
                                    <img src="/static/img/wrong-file.png">
                                </div>
                            </div>
            """
        else:
            self.error(404)
            self.redirect('/404')

        self.render_template('static-page.html', {
            'user': user,
            'session': session,
            'profiles': profiles,
            'nav_tab_location': 'static-page',
            'page': page,
        })


    def filePage(self, file_id):
        session = self.request.session if self.request.session else None
        user = self.request.user if self.request.user else None
        profiles = None
        if user:
            profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
            profiles = ndb.get_multi(profile_keys)
            current_user_key = user.key.urlsafe()
        else:
            current_user_key = None

        page = {}
        print file_id
        getFile = BlobFiles.query(BlobFiles.unique_id == file_id).get()

        if getFile.privacy == "private":
          page['meta'] = '<meta name="robots" contant="noindex, nofollow, noarchive, nosnippet, noodp, notranslate, noimageindex">'
          self.response.headers['X-Robots-Tag:'] = "none, noindex, nofollow, noarchive, nosnippet, noodp, notranslate, noimageindex"
          if not current_user_key:
            self.error('400')
            self.redirect('/')
          if current_user_key != getFile.created_by.urlsafe():
            self.error('400')
            self.redirect('/')

        self.render_template('file-page.html', {
            'user': user,
            'session': session,
            'profiles': profiles,
            'nav_tab_location': 'file-page',
            'getFile': getFile,
            'page': page,
        })


    def myfiles(self):
        session = self.request.session if self.request.session else None
        user = self.request.user if self.request.user else None
        profiles = None
        if user:
            profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
            profiles = ndb.get_multi(profile_keys)

        myFiles = BlobFiles.query(BlobFiles.created_by == user.key).fetch()

        self.render_template('myfiles.html', {
            'user': user,
            'session': session,
            'profiles': profiles,
            'nav_tab_location': 'myfiles',
            'myFiles': myFiles,
        })