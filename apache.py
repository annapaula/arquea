import os
from mod_python import apache
from mod_python import util
from django.core.handlers.base import BaseHandler
from django.core.handlers.modpython import ModPythonRequest

class AccessHandler(BaseHandler):
    def __call__(self, req):
        from django.conf import settings
        # set up middleware
        if self._request_middleware is None:
            self.load_middleware()
	# populate the request object
	request = ModPythonRequest(req)
	# and apply the middleware to it
	# actually only session and auth middleware would be needed here
	for middleware_method in self._request_middleware:
		middleware_method(request)
	return request

def accesshandler(req):
    os.environ.update(req.subprocess_env)
    
    # check for PythonOptions
    _str_to_bool = lambda s: s.lower() in ('1', 'true', 'on', 'yes')

    options = req.get_options()
    permission_name = options.get('DjangoPermissionName', None)
    staff_only = _str_to_bool(options.get('DjangoRequireStaffStatus', "on"))
    superuser_only = _str_to_bool(options.get('DjangoRequireSuperuserStatus', "off"))
    settings_module = options.get('DJANGO_SETTINGS_MODULE', None)
    
    if settings_module:
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
    
    request=AccessHandler()(req)
    if request.user.is_authenticated():
	if permission_name and request.user.has_perm(permission_name):
	    return apache.OK
        else:
	    return apache.HTTP_UNAUTHORIZED
    else:
        util.redirect(req, str('%s?next=%s' % ('http://sistema.ansp.br/accounts/login', request.path)))
    return apache.HTTP_UNAUTHORIZED
