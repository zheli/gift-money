# -*- coding: utf-8 -*-
### required - do no delete
import facebook
import fb_helpers
import logging
#logging.getLogger().setLevel(logging.DEBUG)

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

def show_credit():
    print request.vars['signed_requst']
    update_session_token()
    if is_first_time_login(session.user_id):
        first_time = True
        record_me = db.fb_users[add_user(session.user_id)]
    else:
        first_time = False
        record_me = db(db.fb_user.uid == session.user_id).select().first()
    print record_me
    return dict(me = record_me, first_time=first_time)

def update_session_token():
    try:
        token = facebook.get_user_from_cookie(request.cookies, fb_oae['id'], fb_oae['secret'])
        session.user_id     = token['uid']
        session.oauth_token = token['access_token']
    except:
        session.oauth_token, session_user_id = \
                fb_helpers.signed_request_getTokenWithID(request.vars['signed_request'],
                                                        fb_oae['secret'])

def is_first_time_login(uid = session.user_id):
    return (len(db(db.fb_user.uid == uid).select(db.fb_user.ALL)) == 0)

def add_user(uid = session.user_id):
    return db.fb_user.insert(uid=uid)

def send_request():
    return dict()
