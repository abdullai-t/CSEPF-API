"""Handler file for all routes pertaining to feature flags"""
from _main_.utils.custom_response import CustomResponse
from _main_.utils.route_handler import RouteHandler
from api.views.staff_views import StaffView


class StaffHandler(RouteHandler):
    def __init__(self):
        super().__init__()
        self.views = StaffView()
        self.registerRoutes()
    
    def registerRoutes(self) -> None:
        self.add("/staff.list", self.list_staff)
        self.add("/staff.info", self.get_staff_info)
    

    def get_staff_info(self, request):
        context = request.context
        args = context.args

        self.validator.expect("staff_id", str, is_required=True)

        args, err = self.validator.verify(args, strict=True)
        if err:
            return err
        
        staff, err = self.views.get_staff_info(context, args)
        if err:
            return err
        
        return CustomResponse(data=staff, status=200)
        
    def list_staff(self, request):
        context = request.context
        args = context.args
        
        staff, err = self.views.list_staff(context, args)
        if err:
            return err
        
        return CustomResponse(data=staff, status=200)