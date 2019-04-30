from google.appengine.ext import ndb


class Blog(ndb.Model):
    user = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    added = ndb.DateProperty(auto_now_add=True)
    text = ndb.StringProperty(required=True)