# encoding: utf-8


import os
import sys
from m import Application
from m.security import AuthenticationFilter
from logging.config import fileConfig
from blog.models import db
from blog.handlers.user import router as user
from blog.authentication import JWTAuthenticationProvider
from blog.handlers.post import router as post
from blog.handlers.comment import router as comment
from blog.handlers.catalog import router as catalog

app = Application()
app.register_extension(db)
app.add_filter(AuthenticationFilter(JWTAuthenticationProvider))
app.add_router(user)
app.add_router(post)
app.add_router(comment)
app.add_router(catalog)


if __name__ == '__main__':
    home = os.path.dirname(sys.argv[0])
    if os.path.exists(os.path.join(home, 'logging.ini')):
        fileConfig(os.path.join(home, 'logging.ini'))
    db.metadata.create_all()
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8080, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
