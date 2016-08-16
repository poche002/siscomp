from pecan import expose, abort
from webob.exc import status_map
from pecan.rest import RestController
import userController, clientSystemController

class RootController(RestController):

#    @expose(generic=True, template='index.html')
    def index(self):
        return dict()
	
    users = userController.UserController()
    clients = clientSystemController.ClientSystemController()    	    

#    @index.when(method='POST')
#    def index_post(self, q):
#        redirect('https://pecan.readthedocs.io/en/latest/search.html?q=%s' % q)

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
