import os
import sys
root = os.path.dirname(__file__)
sys.path.insert(0,os.path.join(root,'site-packages'))

import sae


from manage import app, db
db.create_all()


application = sae.create_wsgi_app(app)