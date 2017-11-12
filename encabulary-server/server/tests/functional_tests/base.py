import unittest

from flask import json

from server import create_app
from server.database import db
from server.database.management import db_manager
from server.database.model import DbUser, DbLanguage
from server.globals import get_root_dir


class BaseTestCase(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{path}/{db_name}'.format(path=get_root_dir(), db_name='test.dictionary.db')

    def create_test_app(self):

        app = create_app({'SQLALCHEMY_DATABASE_URI': self.SQLALCHEMY_DATABASE_URI})

        return app

    def setUp(self):
        self.app = self.create_test_app()
        self.client = self.app.test_client()
        self.test_user_id = None

        with self.app.app_context():
            db_manager.delete_db()
            db_manager.create_db()
            db_manager.init_db_with_default_values()

            test_user = DbUser('test', DbLanguage.RU, 'test')
            db.session.add(test_user)
            db_manager.save_db_changes()

            self.test_user_id = test_user.id_user

            db.session.remove()

    def tearDown(self):
        pass

    def get_json_response(self, url, params=None, headers=None, method=None):
        method = method or 'POST'

        if method in ['POST', 'PUT']:
            params = json.dumps(params)

        raw_response = self.client.open(
            url,
            method=method,
            data=params,
            headers=headers,
            content_type='application/json'
        ).data

        try:
            return json.loads(raw_response)
        except Exception as ex:
            print(raw_response)
            return None

    def get_json_multipart_response(self, url, params=None, headers=None):
        raw_response = self.client.post(url, content_type='multipart/form-data', data=params, headers=headers).data

        return json.loads(raw_response)

    def get_login_response(self):
        return self.get_json_response(
            '/api/login',
            dict(
                email='test',
                password='test'
            )
        )

    def print_json(self, json_dict, message=None):
        print('{}\n{}\n---------------\n'.format(message, json.dumps(json_dict, indent=3, sort_keys=True, ensure_ascii=False)))


class BaseAuthTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.get_login_response()
