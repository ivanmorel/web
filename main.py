import os
import webapp2
from jinja2 import Environment, FileSystemLoader
import re

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinjaEnv = Environment(loader=FileSystemLoader(template_dir), autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9]{3,15}$")
PASS_RE = re.compile(r"^.{3,15}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


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


def valid_user(username):
    return username and USER_RE.match(username)


def valid_pass(password):
    return password and PASS_RE.match(password)


def valid_email(email):
    return email and EMAIL_RE.match(email)


app = webapp2.WSGIApplication([
    ('/memes', Memes),
    ('/fizzbuzz', FizzBuzz),
    ('/shop', Shop),
    ('/rot13', Rot13),
    ('/signup', SignUp),
], debug=True)
