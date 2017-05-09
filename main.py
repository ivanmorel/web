import os
import webapp2
from jinja2 import Environment, FileSystemLoader
import re
import hashlib
import hmac

from google.appengine.ext.ndb import model
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinjaEnv = Environment(loader=FileSystemLoader(template_dir), autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9]{3,15}$")
PASS_RE = re.compile(r"^.{3,15}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
SECRET = "wtfmanin"

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        return jinjaEnv.get_template(template).render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Rot13(Handler):
    def get(self):
        self.render('rot13_form.html')

    def post(self):
        params = {}
        text = self.request.get("text")
        text13 = text.encode("rot13")
        params['text'] = text13
        self.render('rot13_form.html', **params)


class SignUp(Handler):
    def get(self):
        self.render('signup.html')

    def post(self):
        error = False
        params = dict()
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if not valid_user(username):
            error = True
            params['error_user'] = "Incorrect username"
        if not valid_pass(password):
            error = True
            params['error_pass'] = "Incorrect password"
        if password != verify:
            error = True
            params['error_ver'] = "Passwords not identical"
        if not valid_email(email):
            error = True
            params['error_email'] = "Incorrect email"

        if error:
            self.render('signup.html', **params)
        else:
            self.response.write("<h1>Thank you</h1>")


class Shop(Handler):
    shop = []

    def get(self):
        self.render('shop.html', shop=Shop.shop)

    def post(self):
        Shop.shop.append(self.request.get('food'))
        self.render('shop.html', shop=Shop.shop)


class FizzBuzz(Handler):
    def get(self):
        num = []
        for i in range(1, 100):
            if i % 3 == 0:
                num.append('Fizz')
            elif i % 5 == 0:
                num.append('Buzz')
            else:
                num.append(i)
        self.render('FizzBuzz.html', num=num)


class Memes(Handler):
    def get(self):
        self.render('memes.html')


class Art(model.Model):
    art = model.TextProperty()
    date = model.DateTimeProperty(auto_now_add=True)


class Blog(model.Model):
    title = model.StringProperty()
    body = model.TextProperty()
    date = model.DateTimeProperty(auto_now_add=True)


class Ascii(Handler):
    def get(self):
        self.render('ASCIIart.html', arts=Art.query().order(-Art.date))

    def post(self):
        art = self.request.get('art')
        Art(art=art, parent=ndb.Key(Art, 'Arts')).put()
        self.render('ASCIIart.html', arts=Art.query(ancestor=ndb.Key(Art, 'Arts')).order(-Art.date), art=art)


class BlogForm(Handler):
    def get(self):
        self.render('blogform.html')

    def post(self):
        title = self.request.get('title')
        body = self.request.get('body')
        Blog(title=title, body=body, parent=ndb.Key(Blog, 'Blogs')).put()
        self.redirect("/blog")


class BlogView(Handler):
    def get(self):
        self.render('blog.html',  blog=Blog.query(ancestor=ndb.Key(Blog, 'Blogs')).order(-Blog.date))


class Cookie(Handler):
    def get(self):
        if not self.request.cookies.get('pass'):
            self.response.headers.add_header('Set-Cookie', 'pass=%s' % hmac.new(SECRET, 'sancocho94').hexdigest())
        self.render('cookie.html')

    def post(self):
        hash_cookie = self.request.cookies.get('pass')
        pwd_hash = hmac.new(SECRET, self.request.get('pass')).hexdigest()
        msg = "Correct Password" if pwd_hash == hash_cookie else 'Incorrect Password'
        self.render('cookie.html', msg=msg)


def valid_user(username):
    return username and USER_RE.match(username)


def valid_pass(password):
    return password and PASS_RE.match(password)


def valid_email(email):
    return email and EMAIL_RE.match(email)


def delete(cls):
    for i in cls.query():
        i.put().delete()


app = webapp2.WSGIApplication([
    ('/', Cookie),
    ('/cookie', Cookie),
    ('/blog', BlogView),
    ('/blogform', BlogForm),
    ('/ascii', Ascii),
    ('/memes', Memes),
    ('/fizzbuzz', FizzBuzz),
    ('/shop', Shop),
    ('/rot13', Rot13),
    ('/signup', SignUp),
], debug=True)
