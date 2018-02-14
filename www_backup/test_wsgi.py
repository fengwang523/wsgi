import sys, os, bottle
#sys.path = ['/usr/local/www/apache22/data/ops/'] + sys.path
sys.path.append('/usr/local/www/apache22/data/ops/')
sys.path.append('/data/ops/python/wsgi/')
os.chdir(os.path.dirname(__file__))

import mx_re_subscribers_wsgi
import huawei_5800_olt_wsgi
import mx_re_wsgi

application = bottle.default_app()
