from server import create_app
from server.database.management import db_manager
from server.tools.stopwatch import Stopwatch

app = create_app()
stopwatch = Stopwatch(auto_start=True)

with app.app_context():
    print('delete db')
    db_manager.delete_db()

    print('create db')
    db_manager.create_db()

    print('init db with default values')
    db_manager.init_db_with_default_values()

stopwatch.stop()

print('==========')
print('DONE at {}'.format(stopwatch))
