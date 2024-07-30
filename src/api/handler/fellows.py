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
        self.add("/projects.list", self.list_projects)
        self.add("/projects.info", self.get_projects_info)

        self.add("/testimonials.list", self.list_testimonials)

        self.add("/trips.list", self.list_trips)
        self.add("/trips.info", self.get_trip_info)

    

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
            return CustomResponse(data=None, message=str(e))
        

    def list_projects(self, request):
        context = request.context
        args = context.args
        try:
            self.validator.expect("is_featured", bool, is_required=False)
            self.validator.expect("cohort", str, is_required=False)
            
            args, err = self.validator.verify(args, strict=True)
            if err:
                return err
    
            projects, err = self.views.list_projects(context, args)
            if err:
                return err
            
            return CustomResponse(data=projects, status=200)
        
        except Exception as e:
            return CustomResponse(data=None, error=str(e))
        

    def get_projects_info(self, request):
        context = request.context
        args = context.args

        self.validator.expect("project_id", str, is_required=True)

        args, err = self.validator.verify(args, strict=True)
        if err:
            return err
        
        projects, err = self.views.get_projects_info(context, args)
        if err:
            return err
        
        return CustomResponse(data=projects, status=200)
    

    def list_testimonials(self, request):
        context = request.context
        args = context.args

        try:
            self.validator.expect("is_featured", bool, is_required=False)
            args, err = self.validator.verify(args, strict=True)
            if err:
                return err

            testimonials, err = self.views.list_testimonials(context, args)
            if err:
                return err
            
            return CustomResponse(data=testimonials, status=200)
        
        except Exception as e:
            return CustomResponse(data=None, error=str(e))
    

    def list_trips(self, request):
        context = request.context
        args = context.args

        try:
            self.validator.expect("latest", bool, is_required=False)

            args, err = self.validator.verify(args, strict=True)
            if err:
                return err

            trips, err = self.views.list_trips(context, args)
            if err:
                return err
            
            return CustomResponse(data=trips, status=200)
        
        except Exception as e:
            return CustomResponse(data=None, error=str(e))
        
    
    def get_trip_info(self, request):
        context = request.context
        args = context.args

        try:
            self.validator.expect("trip_id", str, is_required=True)

            args, err = self.validator.verify(args, strict=True)
            if err:
                return err

            trip, err = self.views.get_trip_info(context, args)
            
            if err:
                return err
            
            return CustomResponse(data=trip, status=200)
        
        except Exception as e:
            return CustomResponse(data=None, error=str(e))

