# -*- coding: utf-8 -*-
from handlers.Jinja2Handler import *
import sys

class Handler(Jinja2Handler):

    def add_file(self):
        session = self.request.session if self.request.session else None
        user = self.request.user if self.request.user else None
        profiles = None
        if user:
            profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
            profiles = ndb.get_multi(profile_keys)


        file_from_form = self.request.get('file')
        if file_from_form:
            uploaded_file = self.request.POST.get("file",None)
            if uploaded_file is None : return self.error(400)

            contentType = getContentType( uploaded_file.filename )
            if contentType is None:
                self.error(400)
                self.redirect('/t/unsupported-mime-type')
                self.response.headers['Content-Type'] = 'text/html'
                self.response.out.write( "Unsupported image type: " + uploaded_file.filename + "<br>" )
                self.response.out.write( "<a href='/'>Back to root</a>" )
                # self.redirect('/t/unsupported-file')
                return

            extension = uploaded_file.filename.split(".")[-1]

            ip_address = os.environ['REMOTE_ADDR']
            file_entry = BlobFiles(unique_id=genId(), name=uploaded_file.filename, data=uploaded_file.file.read(), mimetype=contentType, extension=extension, created_by=user.key, created_ip=ip_address )
            thefile = file_entry.data
            size = sys.getsizeof(thefile)
            print size
            if size > 1000000:
                self.redirect('/t/file-too-big')
            else:
                file_entry.put()
                self.redirect("/files/" + file_entry.unique_id)

    def replace_file(self):
        session = self.request.session if self.request.session else None
        user = self.request.user if self.request.user else None
        profiles = None
        if user:
            profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
            profiles = ndb.get_multi(profile_keys)


        fileEntryKey = self.request.get('key')
        fileToReplace = ndb.Key(urlsafe=fileEntryKey).get()

        file_from_form = self.request.get('file')
        if file_from_form:
            uploaded_file = self.request.POST.get("file",None)
            if uploaded_file is None : return self.error(400)

            contentType = getContentType( uploaded_file.filename )
            if contentType is None:
                self.error(400)
                self.redirect('/t/unsupported-mime-type')
                self.response.headers['Content-Type'] = 'text/html'
                self.response.out.write( "Unsupported image type: " + uploaded_file.filename + "<br>" )
                self.response.out.write( "<a href='/'>Back to root</a>" )
                # self.redirect('/t/unsupported-file')
                return

            extension = uploaded_file.filename.split(".")[-1]

            ip_address = os.environ['REMOTE_ADDR']
            
            fileToReplace.name = uploaded_file.filename
            fileToReplace.data = uploaded_file.file.read()
            fileToReplace.mimetype = contentType
            fileToReplace.extension = extension
            fileToReplace.created_by = user.key
            fileToReplace.created_ip = ip_address

            thefile = fileToReplace.data
            size = sys.getsizeof(thefile)
            print size
            if size > 1000000:
                self.redirect('/t/file-too-big')
            else:
                fileToReplace.put()
                self.redirect("/files/" + fileToReplace.unique_id)

    def change_privacy(self):
        session = self.request.session if self.request.session else None
        user = self.request.user if self.request.user else None
        profiles = None
        if user:
            profile_keys = [ndb.Key('UserProfile', p) for p in user.auth_ids]
            profiles = ndb.get_multi(profile_keys)

        unique_id = self.request.get('file_id')
        getfile = BlobFiles.query(BlobFiles.unique_id == unique_id).get()

        if getfile.created_by.urlsafe() == user.key.urlsafe():
            getfile.privacy = self.request.get('privacy')
            getfile.put()

            destination = self.request.get('destination')
            self.redirect(destination)
        else:
            self.error('500')
            self.redirect('/')