from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from .models import (
    DBSession,
    MyModel,
    )


# @view_config(route_name='home', renderer='templates/mytemplate.pt')
# def my_view(request):
#     try:
#         one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)
#     return {'one': one, 'project': 'matheus_project'}

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
    return {'project': 'matheus_project'}

@view_config(name='sendEmail', renderer='json')
def sendEmail_view(request):
    mailer = request.registry['mailer']
    name = request.GET["name"]
    email = request.GET["email"]
    assunto = request.GET["subject"]
    content = request.GET["content"]

    message = Message(subject="Contato Pelo Site",
                  sender="0matheus.araujo0@gmail.com",
                  recipients=["matheus.ld.araujo@gmail.com"],
                  body="Nome: %s\nEmail: %s \nAssunto: %s \nConteudo: %s \n" % (name,email,assunto,content))
    try:
        # mailer.send_immediately(message, fail_silently=False)
        import time;time.sleep(1)
    except:
        return {'message': 'Desculpe houve um problema, tente me contactar pelo email.<br/>Sorry a problem happened, try to contact me by email'}
    return {'message': 'Email enviado.</br>Email sent.'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_matheus_project_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

