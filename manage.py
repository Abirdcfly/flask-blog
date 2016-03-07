#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Permission, Post, Follow, Comment
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask import g


# reload(os.sys)
# sys.setdefaultencoding('utf-8')


if os.environ.get('APP_NAME') == None:
    check = 'development'
else:
    check = 'production'

# app = create_app(os.getenv('WOTER_CONFIG') or 'production')
app = create_app(os.getenv('WOTER_CONFIG') or 'development')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission, Post=Post, Follow=Follow, Comment=Comment)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
# @app.before_first_request
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()

    # create self-follows for all users
    User.add_self_follows()


@manager.command
def fake(count):
    from app.models import Post, User
    User.generate_fake(count)
    Post.generate_fake(count)


# @app.before_first_request
# def create_database():
#     db.create_all()

# create_database()

if __name__ == '__main__':
    # create_database()
    # db.create_all()
    # manager.run({'deploy': deploy()})
    # manager.run({'fake': fake(100)})
    manager.run()


# @app.before_first_request
# def database_init():
#     """Run deployment tasks."""
#
#     db.create_all()

# def before_request():
#     g.session = create_session()
#
#
# @app.teardown_request
# def teardown_request(exception):
#     g.session.close()
#


@app.before_request
def deploy():
    """Run deployment tasks."""
    # from flask.ext.migrate import upgrade, init
    from app.models import Role, User

    # migrate database to latest revision
    # if os.path.exists('./migrations'):
    #     upgrade()
    # else:
    #     init()

    # create user roles
    Role.insert_roles()

    # create self-follows for all users
    User.add_self_follows()