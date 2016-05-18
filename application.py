import sys
from flask import current_app
sys.path.insert(0, "/")

from flask_app.app import create_app


application = create_app('default')




if __name__ == "__main__":
    application.run()


