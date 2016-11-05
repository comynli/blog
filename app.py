from m import Application
from blog.models import db


app = Application()
app.register_extension(db)


if __name__ == '__main__':
    db.metadata.create_all()