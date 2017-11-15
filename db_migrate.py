from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from devobs import app

manager = Manager(app)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()

# Run: python db_migrate.py db migrate -m "comment"
# Run: python db_migrate.py db upgrade