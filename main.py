#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
from jinja2 import Environment, FileSystemLoader
import re

jinjaEnv = Environment(loader=FileSystemLoader(template_dir))

USER_RE = re.compile(r"^[a-zA-Z0-9]{3,15}$")
PASS_RE = re.compile(r"^.{3,15}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    @staticmethod
    def render_str(template, **params):
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
            self.response.write("Thank you")


def valid_user(username):
    return username and USER_RE.match(username)


def valid_pass(password):
    return password and PASS_RE.match(password)


def valid_email(email):
    return email and EMAIL_RE.match(email)


app = webapp2.WSGIApplication([
    ('/', SignUp),
    ('/rot13', Rot13),
], debug=True)
