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
        self.add("/fellows.list", self.list_fellows)
        self.add("/fellows.info", self.get_fellows_info)
    

    def get_fellows_info(self, request):
        context = request.context
        args = context.args
        
        fellows, err = self.views.get_fellows_info(context, args)
        if err:
            return err
        
        return CustomResponse(fellows)
        
    def list_fellows(self, request):
        context = request.context
        args = context.args
        
        fellows, err = self.views.list_fellows(context, args)
        if err:
            return err
        
        return CustomResponse(fellows)