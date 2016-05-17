from app import create_app 

application = create_app('default') 

if __name__ == "__main__":
    application.run()


