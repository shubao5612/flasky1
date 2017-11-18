import os

from app import create_app,db
from app.models import User,Role,Post,Follow

from flask_script import Shell,Manager
from flask_migrate import Migrate,MigrateCommand

app=create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager=Manager(app)

migrate=Migrate(app,db)
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Post=Post,Follow=Follow)
manager.add_command('shell',Shell(make_context=make_shell_context))

manager.add_command('db',MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

#运行时 用 python manage.py hello
@manager.command
def hello():
    return 'hello'

@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import User,Role
    upgrade()
    Role.insert_roles()
    User.add_self_follows()


if __name__=='__main__':
    manager.run()