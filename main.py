from hackers.app import app
from hackers.database.init_db import init_db

def main():
    init_db()
    app.run()

if __name__ == '__main__':
    main()