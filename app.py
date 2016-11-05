from m import Application
from m.security import AuthenticationFilter
from blog.models import db
from blog.handlers.user import router as user
from blog.authentication import JWTAuthenticationProvider

app = Application()
app.register_extension(db)
app.add_filter(AuthenticationFilter(JWTAuthenticationProvider))
app.add_router(user)


if __name__ == '__main__':
    db.metadata.create_all()
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8080, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
