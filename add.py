from google.appengine.api import users
from google.appengine.ext import ndb

from blog import Blog

import webapp2
import jinja2
import os
import time

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)

class AddHandler(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            template_values = {
                "user_name": user_name,
                "access_link": access_link,
            }

            template = JINJA_ENVIRONMENT.get_template("add.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")


    def post(self):

        user = users.get_current_user()

        if user:

            blog = Blog()
            blog.title = self.request.get("title").strip()
            blog.text = self.request.get("text").strip()
            blog.user = user.user_id()

            # Chk
            if len(blog.title) < 1:
                self.redirect("/error?msg=" + "add aborted: title's name is mandatory")
                return

            if blog.text < 0:
                self.redirect("/error?msg=" + "add aborted: text's name is mandatory")
                return

            # Save
            blog.put()
            time.sleep(1)
            self.redirect("/main")
        else:
            self.redirect("/")
