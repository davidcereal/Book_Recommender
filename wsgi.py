#import sys
#sys.path.insert(0, "/flask_app/")

from flask_app.app import create_app


application = create_app('default') 

if __name__ == "__main__":
    application.run()


