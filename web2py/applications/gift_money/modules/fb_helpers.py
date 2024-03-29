import base64
import hashlib
import hmac
try:
    # For Google AppEngine
    from django.utils import simplejson
except ImportError:
    # for web2py
    from gluon.contrib import simplejson

def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor 
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(signed_request, secret):

    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = base64_url_decode(encoded_sig)
    data = simplejson.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        #print('Unknown algorithm')
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        #print('valid signed request received..')
        return data

def signed_request_getTokenWithID(signed_request, secret):
    data = parse_signed_request(signed_request, secret)
    return data['oauth_token'], data['user_id']
