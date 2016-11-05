from m import Application
from blog.models import db
from blog.handlers.user import router as user


app = Application()
app.register_extension(db)
app.add_router(user)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8080, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()