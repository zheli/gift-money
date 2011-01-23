# -*- coding: utf-8 -*-
from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = '\xe5\x8e\x8b\xe5\xb2\x81\xe9\x92\xb1'
settings.subtitle = 'powered by web2py'
settings.author = 'Zhe'
settings.author_email = 'linuxcity.jn@gmail.com'
settings.keywords = '\xe5\x8e\x8b\xe5\xb2\x81\xe9\x92\xb1'
settings.description = ''
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '25b9044a-fb75-48a1-8629-61ce7f2b6ceb'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''

import sys, os
path = os.path.join(request.folder, 'modules')
if not path in sys.path:
    sys.path.append(path)

from fbappauth import *
