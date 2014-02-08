from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_mailer import Mailer

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    #Includes
    config.include('pyramid_mailer')
    config.registry['mailer'] = Mailer.from_settings(settings)

    config.include('pyramid_rewrite')
    config.add_rewrite_rule(r'http://www.matheus-araujo.com', r'/')
    config.scan()
    return config.make_wsgi_app()
