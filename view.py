from google.appengine.api import users
from google.appengine.ext import ndb


import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class ViewHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=blog was not found")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                blog = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return

            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "blog": blog,
            }

            template = JINJA_ENVIRONMENT.get_template("view.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")