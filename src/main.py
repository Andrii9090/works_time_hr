from app.server import app
from app.db import db
from command import cmd
from workers.routers import worker_module
from users.routers import user_module

app.register_blueprint(worker_module, url_prefix='/workers')
app.register_blueprint(user_module, url_prefix='/users')
app.register_blueprint(cmd)


db.init_app(app=app)
