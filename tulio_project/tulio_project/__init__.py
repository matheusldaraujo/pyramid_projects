print "__init__"
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder

from .models import (
    DBSession,
    Base,
    )



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    print "main __init__"
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    
    #Security Stuff
    authn_policy = AuthTktAuthenticationPolicy(secret='sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    #Url stuff
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('store_mp3', '/store_mp3')
    config.add_route('store_script', '/store_mp3_view')
    config.scan()
    return config.make_wsgi_app()
