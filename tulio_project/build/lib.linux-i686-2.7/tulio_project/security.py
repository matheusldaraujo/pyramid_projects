from .models import UserModel, DBSession
from sqlalchemy.exc import DBAPIError


GROUPS = {'editor':['group:editors']}

def groupfinder(userid, request):
	try:
		usersDB = DBSession.query(UserModel).all()
	except DBAPIError:
		return Response(conn_err_msg, content_type='text/plain', status_int=500)
	for user in usersDB:
		if user.login == userid:
			return user
	return None