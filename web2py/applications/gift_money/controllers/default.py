# -*- coding: utf-8 -*-
### required - do no delete
import facebook
import fb_helpers
import logging
logging.getLogger().setLevel(logging.ERROR)

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call():
    session.forget()
    return service()
### end requires
def index():
    from urllib import urlencode, unquote_plus
    return dict(request_string = XML(urlencode(request.vars)))

def main():
    #print request.vars['signed_request']
    update_session_token()
    session.app_id = fb_oae['id']
    record_id = update_user_info_in_db()
    if record_id:
        record_me = db.fb_user(record_id)
    else:
        record_me = db(db.fb_user.uid == session.uid).select().first()
    session.me = record_me
    return dict(name = record_me['name'], login_url = XML(get_login_url()), log_records = get_log())

def update_user_info_in_db():
    if is_first_time_login(session.uid):
        return add_user(session.uid)
    else:
        return None

def error():
    return dict()

def get_login_url():
    from urllib import urlencode, unquote_plus
    query = dict(client_id = fb_oae['id'], scope = fb_oae['scope'], redirect_uri = app_url)
    return unquote_plus(fb_auth_url + urlencode(query))

def show_credit():
    record_me = db(db.fb_user.uid == session.uid).select().first()
    logging.info(record_me)
    return dict(record = record_me)

def update_session_token():
    try:
        token = facebook.get_user_from_cookie(request.cookies, fb_oae['id'], fb_oae['secret'])
        session.uid     = token['uid']
        session.oauth_token = token['access_token']
    except:
        session.oauth_token, session.uid = \
                fb_helpers.signed_request_getTokenWithID(\
                request.vars['signed_request'], fb_oae['secret'])

def is_first_time_login(uid = session.uid):
    return (len(db(db.fb_user.uid == uid).select(db.fb_user.ALL)) == 0)

def add_user(uid = session.uid):
    graph = facebook.GraphAPI(session.oauth_token)
    user = graph.get_object(uid)
    return db.fb_user.insert(uid=uid, first_name=user['first_name'], name=user['name'])

def get_log():
    result = []
    try:
        user_id = session.me.id
        records = db(db.log.receiver == user_id).select(orderby=db.log.time)
        if len(records)>0:
            logging.debug(records)
            return records
    except:
        pass

    return result

def ranking():
    friends = get_app_friends()
    dict_data = {}
    if len(friends)>0:
        for friend_uid in friends:
            record = db(db.fb_user.uid==friend_uid).select().first()
            dict_data[record.credit] = {'name': record.name,
                                    'uid': record.uid}
        ranking = sorted(dict_data, reverse=True)
    else:
        ranking = None
    return dict(ranking = ranking, dict_data = dict_data)

def get_app_friends():
    friends = []
    try:
        graph = facebook.GraphAPI(session.oauth_token)
        friends = [str(i) for i in graph.get_app_connections()]
    except facebook.GraphAPIError:
        logging.error('GraphAPIError! user_id: [%s] token: [%s]' % (session.me['uid'], session.oauth_token))
    return friends

def send_request():
    return dict()

def push_messages():
    id_list = request.vars['id[]']
    graph = facebook.GraphAPI(session.oauth_token)
    if type(id_list) == type(list()):
        for id in id_list:
            try:
                db_id= update_credit(id)
                add_log(db_id)
                post_on_wall(graph, id)
            except GraphAPIError:
                logging.error("uid:[%s] post failed!" % id)
                pass

    elif type(id_list) == type(str()):
        try:
            id = id_list
            db_id = update_credit(id)
            add_log(db_id)
            post_on_wall(graph, id)
        except GraphAPIError:
            logging.error("uid:[%s] post failed!" % id)
            pass
    else:
        pass
    return dict()

def post_on_wall(graph = None, id = None):
    if id and graph:
        graph.put_object(id, 'feed',
                message=u'過年可不要忘了壓歲錢哦！'.encode('utf-8'),
                picture = u'http://lucky-money.appspot.com/gift_money/static/images/logo.jpg',
                name=u'%s剛剛給你了一個紅包'.encode('utf-8') % session.me['name'],
                link=u'http://apps.facebook.com/lucky_money/',
                description=u'新年行大運！我剛剛給你包了一個紅包，今年要乖乖的喲！'.encode('utf-8'),
                )

def update_credit(id = None):
    if id:
        if is_first_time_login(id):
            record_id = add_user(id)
            return record_id
        else:
            record = db(db.fb_user.uid == id).select().first()
            record.update_record(credit = record.credit + 1)
            return record.id

def add_log(id = None):
    if id and session.me['uid']:
        db.log.insert(sender = session.me.id, receiver = id)
