"""Handler file for all routes pertaining to feature flags"""
from _main_.utils.custom_response import CustomResponse
from _main_.utils.route_handler import RouteHandler
from api.views.applications import ApplicationsView


class ApplicationsHandler(RouteHandler):
    def __init__(self):
        super().__init__()
        self.views = ApplicationsView()
        self.registerRoutes()
    
    def registerRoutes(self) -> None:
        self.add("/applications.create", self.create_application)
        self.add("/applications.list", self.list_applications)
    

    def create_application(self, request):
        context = request.context
        args = context.args
        
        self.validator.expect("full_name", str, is_required=True)
        self.validator.expect("email", str, is_required=True)
        self.validator.expect("school", str, is_required=True)
        self.validator.expect("program", str, is_required=True)
        self.validator.expect("phone_number", str, is_required=True)
        self.validator.expect("address", str, is_required=True)
        
        args, err = self.validator.verify(args, strict=True)
        if err:
            return err
        
        application, err = self.views.create_application(args)
        if err:
            return err
        return CustomResponse(application)
    
    def list_applications(self, request):
        context = request.context
        args = context.args
        
        applications, err = self.views.get_all_applications(context, args)
        if err:
            return err
        
        return CustomResponse(applications)
    