from google.appengine.api import users
from google.appengine.ext import ndb

from blog import Blog

import time
import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class ModifyHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=blog was not found")
            return

        user = users.get_current_user()

        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                blog = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return

            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "blog": blog,
            }

            template = JINJA_ENVIRONMENT.get_template("modify.html")
            self.response.write(template.render(template_values))
        else:
            self.redirect("/")

    def post(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=missing id for modification")
            return

        user = users.get_current_user()

        if user != None:
            # Get blog by key
            try:
                blog = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return

            blog.title = self.request.get("title").strip()
            blog.text = self.request.get("text").strip()

            # Chk
            if len(blog.title) < 1:
                self.redirect("/error?msg=" + "Modification aborted: blog's title is mandatory")
                return

            if len(blog.text) < 1:
                self.redirect("/error?msg=" + "Modification aborted: blog's text is mandatory")
                return

            # Save
            blog.put()
            time.sleep(1)
            self.redirect("/main")
        else:
            self.redirect("/")