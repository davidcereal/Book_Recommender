#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Book, Read, Keyword, Book_keyword
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
import flask.ext.whooshalchemy
#from flask_alembic.cli.script import manager as alembic_manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default') 
manager = Manager(app)
migrate = Migrate(app, db)
application = create_app(os.getenv('FLASK_CONFIG') or 'default') 

flask.ext.whooshalchemy.whoosh_index(app, Book)

def make_shell_context():
	return dict(app=app, db=db, User=User, Book=Book, Read=Read, 
				Keyword=Keyword, Book_Keyword=Book_keyword)
	
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
#manager.add_command('db', alembic_manager)


if __name__ == '__main__':
	manager.run()
