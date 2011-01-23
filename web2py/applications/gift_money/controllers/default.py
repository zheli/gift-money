# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call():
    session.forget()
    return service()
### end requires
def index():
    session.app_id = fb_oae['id']
    return dict(login_url = XML(get_login_url()))

def error():
    return dict()

def get_login_url():
    from urllib import urlencode, unquote_plus
    query = dict(client_id = fb_oae['id'], scope = fb_oae['scope'], redirect_uri = app_url)
    return unquote_plus(fb_auth_url + urlencode(query))

def send_request():
    return dict()
