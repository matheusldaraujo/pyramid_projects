print "view"
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
import os
from pyramid.security import authenticated_userid, remember, forget
from .security import groupfinder

def view(request):
    return HTTPFound(location='http://matheus-araujo.com') # any renderer avoided

from .models import (
    DBSession,
    MyModel,
    UserModel,
    )


@view_config(route_name='home', renderer='index.pt')
def my_view(request):
    print "my_view"
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
        usersDB = DBSession.query(UserModel).all()
        # imagesDB = DBSession.query(ImageModel).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)


    images = os.listdir("./tulio_project/static/personal_images")

    #Lambda to simplify :)
    from urllib import unquote_plus
    unquoteLambda = lambda x: unquote_plus(x)
    pathLambda = lambda x: "/static/personal_images/" + x
    
    imagesLinks = map(pathLambda,images)
    imagesNames = map(unquoteLambda,images)
    
    logged_in = authenticated_userid(request)
    if logged_in:
        logged_in = groupfinder(logged_in,request).name

    
    return {'one': one, 'project': 'Tulio Project','iNames':imagesNames,"iPath":imagesLinks, 'users':usersDB,'logged':logged_in}

@view_config(route_name="store_mp3", renderer="store_mp3.pt")
def my_python(request):
    if not authenticated_userid(request):
        return HTTPFound(location = "/")
    return {}

@view_config(name='login',renderer="templates/login.pt")
def login_before(request):
    login_url = request.resource_url(request.context, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from, go to index
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    showLogin = True
    if authenticated_userid(request):
        message = "Favor realizar logout antes de tentar logar novamente"
        showLogin = False
    if 'form.submitted' in request.params:
        print "submitted"
        login = request.params['login']
        user = groupfinder(login,request)
        if user != None:
            print "\tlogin tentado", login
            password = request.params['password']
            print "\tsemja tentado", password
            if user.senha == password:
                headers = remember(request, login)
                return HTTPFound(location = came_from,
                    headers = headers)
        message = '<i>Failed login</i>'
        showLogin = True

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        showLogin = showLogin,
        )

@view_config(name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.resource_url(request.context),
                     headers = headers)

@view_config(route_name="store_script")
def store_script(request):
    # ``filename`` contains the name of the file in string format.
    #
    # WARNING: this example does not deal with the fact that IE sends an
    # absolute file *path* as the filename.  This example is naive; it
    # trusts user input.
    
    from urllib import quote_plus

    FILES = request.POST.getall('mp3')
    for FILE in FILES:
        filename = quote_plus(FILE.filename)
        print filename
        input_file = FILE.file
        file_path = os.path.join('./tulio_project/static/personal_images', filename)
        output_file = open(file_path, 'wb')
        input_file.seek(0)
        while 1:
            data = input_file.read(2<<16)
            if not data:
                break
            output_file.write(data)
        output_file.close()

    
    # Using the filename like this without cleaning it is very
    # insecure so please keep that in mind when writing your own
    # file handling.
    

    # Finally write the data to the output file
    

    return HTTPFound(location="/")


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_tulio_project_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

