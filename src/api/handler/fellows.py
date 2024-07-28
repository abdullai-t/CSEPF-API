"""Handler file for all routes pertaining to feature flags"""
from _main_.utils.custom_response import CustomResponse
from _main_.utils.route_handler import RouteHandler
from api.views.applications import ApplicationsView
from api.views.fellows_views import FellowsView


class FellowsHandler(RouteHandler):
    def __init__(self):
        super().__init__()
        self.views = FellowsView()
        self.registerRoutes()
    
    def registerRoutes(self) -> None:
        self.add("/fellows.list", self.list_fellows)
        self.add("/fellows.info", self.get_fellows_info)

        self.add("/presentations.list", self.list_presentations)
    

    def get_fellows_info(self, request):
        context = request.context
        args = context.args

        self.validator.expect("fellow_id", str, is_required=True)

        args, err = self.validator.verify(args, strict=True)
        if err:
            return err
        
        fellows, err = self.views.get_fellows_info(context, args)
        if err:
            return err
        
        return CustomResponse(data=fellows, status=200)
        
    def list_fellows(self, request):
        context = request.context
        args = context.args
        
        fellows, err = self.views.list_fellows(context, args)
        if err:
            return err
        
        return CustomResponse(data=fellows, status=200)
    

    def list_presentations(self, request):
        context = request.context
        args = context.args
        try:
            self.validator.expect("is_featured", bool, is_required=False)
            
            args, err = self.validator.verify(args, strict=True)
            if err:
                return err
    
            presentations, err = self.views.list_presentations(context, args)
            if err:
                return err
            
            return CustomResponse(data=presentations, status=200)
        
        except Exception as e:
            return CustomResponse(data=None, message=str(e), status=500)
