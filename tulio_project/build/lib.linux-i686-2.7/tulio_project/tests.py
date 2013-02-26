import unittest
import transaction

from pyramid import testing

from .models import DBSession


class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            MyModel,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = MyModel(name='one', value=55)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'tulio_project')

from pyramid import testing

class TestViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_mailer.testing')

    def tearDown(self):
        testing.tearDown()

    def test_some_view(self):
        from pyramid.testing import DummyRequest
        from pyramid_mailer import get_mailer
        from .views import send_email

        request = DummyRequest()
        import ipdb;ipdb.set_trace()
        mailer = get_mailer(request)
        response = send_email(request)
        
        self.assertEqual(len(mailer.outbox), 1)
        self.assertEqual(mailer.outbox[0].subject, "hello world")
        self.assertEqual(len(mailer.queue), 1)
        self.assertEqual(mailer.queue[0].subject, "hello world")