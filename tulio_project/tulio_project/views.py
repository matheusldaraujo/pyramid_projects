# -*- coding: utf-8 -*-
print "view"
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from os import listdir
from pyramid.security import authenticated_userid, remember, forget
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
import json

from .security import groupfinder
from .utils import fileType
from .models import (
    DBSession,
    MyModel,
    UserModel,
    CommentModel,
    )
import transaction

#Mail config


@view_config(name="send_email")
def send_email(request):
    mailer = request.registry['mailer']

    name = request.POST["name"]
    email = request.POST["email"]
    assunto = request.POST["assunto"]
    content = request.POST["content_message"]

    message = Message(subject="Contato Pelo Site",
                  sender="0matheus.araujo0@gmail.com",
                  recipients=["matheus.ld.araujo@gmail.com"],
                  body="Nome: %s\nEmail: %s \nAssunto: %s \nConteudo: %s \n" % (name,email,assunto,content))
    try:
        mailer.send_immediately(message, fail_silently=False)
    except:
        return Response("Desculpe houve um problema no envio")
    return HTTPFound(location = "/")

@view_config(name="addComment", renderer="json")
def add_comment(request):
    name = request.GET['name']
    comment = request.GET['comment']
    imgid = request.GET['imgid']
    dbComentario = CommentModel(name = name,comment= comment,imgid=imgid)
    try:
        DBSession.add(dbComentario)
    except :
        return {"message":"Houve um problema.<br/>Avise o desenvolvedor."}
    return {"message": "Comentario salvo com sucesso.<br/>"}

@view_config(name="getComments", renderer="json")
def get_comment(request):
    try:
        comments = DBSession.query(CommentModel).order_by("id desc").all()
        
    except :
        return {"message":"Houve um problema.<br/>Avise o desenvolvedor."}
    
    toReturn = []
    for comment in comments:
        d = {}
        d['comment'] = comment.comment
        d['name'] = comment.name
        d['imgid'] = comment.imgid
        d['id'] = comment.id
        toReturn.append(d)
    return json.dumps(toReturn)

@view_config(name="removeImg", renderer="json")
def remove_img(request):
    pathThumb = request.GET['path']
    pathImgOriginal = "/static/personal_images/" + pathThumb.split("/")[-1][2:]
    pathSmallThumb = "/static/personal_images/smallthumbs/" +"S" + pathThumb.split("/")[-1]

    import os
    try:
        os.remove("./tulio_project" + pathThumb)
        os.remove("./tulio_project" + pathImgOriginal)
        os.remove("./tulio_project" + pathSmallThumb)
    except:
        return {'message':'Houve um erro ao deletar os arquivos, contate o desenvolvedor.'}
    return {"message":"ok"}

@view_config(name="deleteComment", renderer="json")
def delete_comment(request):
    id = request.GET['id']
    try:
        DBSession.query(CommentModel).filter_by(id = id).delete()
    except :
        return {"message":"Houve um problema.<br/>Avise o desenvolvedor."}
    return {"message": "Comentário deletado"}


def view(request):
    return HTTPFound(location='http://matheus-araujo.com') # any renderer avoided

# @view_config(route_name='home', renderer='templates/index.pt')
# def my_view(request):
#     print "my_view"
#     try:
#         one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
#         usersDB = DBSession.query(UserModel).all()
#         # imagesDB = DBSession.query(ImageModel).all()
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)


#     images = os.listdir("./tulio_project/static/personal_images")
#     import ipdb;ipdb.set_trace()
#     # for image in images:
#     #     if image[0:2] == "T_":


#     #Lambda to simplify :)
#     from urllib import unquote_plus
#     unquoteLambda = lambda x: unquote_plus(x)
#     pathLambda = lambda x: "/static/personal_images/" + x
    
#     imagesLinks = map(pathLambda,images)
#     imagesNames = map(unquoteLambda,images)
    
#     logged_in = authenticated_userid(request)
#     if logged_in:
#         logged_in = groupfinder(logged_in,request).name

    
#     return {'one': one, 'project': 'Tulio Project','iNames':imagesNames,"iPath":imagesLinks, 'users':usersDB,'logged':logged_in}

@view_config(name="add_files", renderer="templates/add_files.pt")
def addFiles(request):
    if not authenticated_userid(request):
        return HTTPFound(location = "/")
    return {}

@view_config(route_name="index", renderer="templates/home.pt")
def my_python(request):
    print "my_view"
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
        usersDB = DBSession.query(UserModel).all()
        # imagesDB = DBSession.query(ImageModel).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)


    images = listdir("./tulio_project/static/personal_images")
    thumbs = listdir("./tulio_project/static/personal_images/thumbs")
    smallthumbs = listdir("./tulio_project/static/personal_images/smallthumbs")

    try:
        images.remove("smallthumbs")
        images.remove("thumbs")
    except:
        print "Erro em retirar diretorios de thumbs da lista de imagens"
        pass

    #Lambda to simplify :)
    from urllib import unquote_plus

    unquoteLambda = lambda x: unquote_plus(x)
    pathLambda = lambda x: "tulio_project/static/personal_images/" + x
    thumbsLambda = lambda x: "tulio_project/static/personal_images/thumbs/" + x
    smallthumbsLambda = lambda x: "tulio_project/static/personal_images/smallthumbs/" + x
    
    imagesLinks = map(pathLambda,images)
    imagesNames = map(unquoteLambda,images)

    thumbsLinks = map(thumbsLambda,thumbs)
    thumbsNames = map(unquoteLambda,thumbs)

    smallthumbsLinks = map(smallthumbsLambda,smallthumbs)
    smallthumbsNames = map(unquoteLambda,smallthumbs)

    #transform to fileType
    imagesFile = []
    thumbsFile = []
    smallthumbsFile = []

    import os.path, time
    
    for imageLink in imagesLinks:
        mtime = os.path.getctime(imageLink)
        name = imageLink.split("/")[-1]
        imageFile = fileType("/static/personal_images/" + name,name,mtime)
        imagesFile.append(imageFile)

    for imageLink in thumbsLinks:
        mtime = os.path.getctime(imageLink)
        name = imageLink.split("/")[-1]
        imageFile = fileType("/static/personal_images/thumbs/" + name,name,mtime)
        thumbsFile.append(imageFile)
    
    for imageLink in smallthumbsLinks:
        mtime = os.path.getctime(imageLink)
        name = imageLink.split("/")[-1]
        imageFile = fileType("/static/personal_images/smallthumbs/" + name,name,mtime)
        smallthumbsFile.append(imageFile)
    
    
    imagesFile.sort(key=lambda x: x.mtime, reverse=True)
    thumbsFile.sort(key=lambda x: x.mtime, reverse=True)
    smallthumbsFile.sort(key=lambda x: x.mtime, reverse=True)

    logged_in = authenticated_userid(request)
    if logged_in:
        logged_in = groupfinder(logged_in,request).name

    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    showLogin = True
    if authenticated_userid(request):
        message = "Favor realizar logout antes de tentar logar novamente"
        showLogin = False
    if 'login.submitted' in request.params:
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
    if 'contato.submitted' in request.params:
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
        one = one,
        project = "Tulio Project",
        users = usersDB,
        logged = logged_in,
        listImages = imagesFile,
        listThumbs = thumbsFile,
        listSmallThumbs = smallthumbsFile
        )
    
    # return {'one': one, 'project': 'Tulio Project', 'users':usersDB,'logged':logged_in,
    #         "listImages":imagesFile,'listThumbs':thumbsFile,'listSmallThumbs':smallthumbsFile}

# @view_config(name='login',renderer="templates/login.pt")
# def login_before(request):
#     login_url = request.resource_url(request.context, 'login')
#     referrer = request.url
#     if referrer == login_url:
#         referrer = '/' # never use the login form itself as came_from, go to index
#     came_from = request.params.get('came_from', referrer)
#     message = ''
#     login = ''
#     password = ''
#     showLogin = True
#     if authenticated_userid(request):
#         message = "Favor realizar logout antes de tentar logar novamente"
#         showLogin = False
#     if 'form.submitted' in request.params:
#         print "submitted"
#         login = request.params['login']
#         user = groupfinder(login,request)
#         if user != None:
#             print "\tlogin tentado", login
#             password = request.params['password']
#             print "\tsemja tentado", password
#             if user.senha == password:
#                 headers = remember(request, login)
#                 return HTTPFound(location = came_from,
#                     headers = headers)
#         message = '<i>Failed login</i>'
#         showLogin = True

#     return dict(
#         message = message,
#         url = request.application_url + '/login',
#         came_from = came_from,
#         login = login,
#         password = password,
#         showLogin = showLogin,
#         )

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
    if request.POST.get('imgs') == '':
        return HTTPFound(location="/")
    from urllib import quote_plus
    import os.path
    FILES = request.POST.getall('imgs')
    for FILE in FILES:
        filename = quote_plus(FILE.filename)
        filename = filename.replace("%","")

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

    import glob
    from PIL import Image
    #get thumbs names
    pathThumbs = glob.glob("tulio_project/static/personal_images/thumbs/*")
    thumbs = []
    for thumb in pathThumbs:
        thumbs.append(thumb.split("/")[-1][2:])

    # get all the jpg files from the current folder
    for pathImage in glob.glob("tulio_project/static/personal_images/*"):
        if pathImage == "tulio_project/static/personal_images/thumbs":
            continue
        if pathImage == "tulio_project/static/personal_images/smallthumbs":
            continue

        imageName = pathImage.split("/")[-1]
        
        imageName = pathImage.split("/")[-1]
        if imageName in thumbs:
            continue # Skipping a thumbnail
        try:
            im = Image.open(pathImage)
        except:
            print "Not image file"
            continue
        # convert to thumbnail image
        im.thumbnail((420, 420), Image.ANTIALIAS)
        im.save( "tulio_project/static/personal_images/thumbs/" + "T_" + imageName, im.format)

        im.thumbnail((75, 75), Image.ANTIALIAS)
        im.save( "tulio_project/static/personal_images/smallthumbs/" + "ST_" + imageName, im.format)
        
    
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

