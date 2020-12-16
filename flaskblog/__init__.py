from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main


def regist_blueprints(app):
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)