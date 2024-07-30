from _main_.utils.commons import serialize, serialize_all
from _main_.utils.errors import CustomError
from database.models import Fellow, Presentation, Project, SiteTrip, Testimonial


class FellowsView:
    """
    Service Layer for all applications
    """

    def __init__(self):
        pass
    
    def get_fellows_info(self, context, args) -> (dict, any):  # type: ignore
        try:
            id = args.get("fellow_id")
            if not id:
                return None, CustomError("Fellow ID is required", status=400)
            
            fellow = Fellow.objects.get(id=id)

            if not fellow:
                return None, CustomError("Fellow not found", status=404)

            return serialize(fellow), None

        except Exception as e:
            return None, CustomError(str(e), status=500)
    
    

    def list_fellows(self, context, args) -> (list, any):  # type: ignore
        try:
            cohort = args.get("cohort", None)
            filter = {}
            if cohort:
                filter["user__cohort"] = cohort

            fellow = Fellow.objects.filter(**filter).order_by("-user__cohort")

            return serialize_all(fellow), None
        
        except Exception as e:
            return None, CustomError(str(e), status=500)
        

    def list_presentations(self, context, args) -> (list, any):  # type: ignore
        try:
            is_featured = args.get("is_featured", False)
            filter = {}
            if is_featured:
                filter["is_featured"] = is_featured
            
            presentations = Presentation.objects.filter(**filter).order_by("-created_at")

            return serialize_all(presentations), None
        
        except Exception as e:
            return None, CustomError(str(e))
        

    def get_projects_info(self, context, args) -> (list, any):  # type: ignore
        try:
            id = args.get("project_id")
            if not id:
                return None, CustomError("project_id is required")
            
            project = Project.objects.get(id=id)

            if not project:
                return None, CustomError("Project not found")

            return serialize(project), None

        except Exception as e:
            return None, CustomError(str(e))
        

    def list_projects(self, context, args) -> (list, any):  # type: ignore
        try:
            is_featured = args.get("is_featured", False)
            cohort = args.get("cohort", None)
            filter = {}
            if is_featured:
                filter["is_featured"] = is_featured
            if cohort:
                filter["fellow__cohort"] = cohort
            
            projects = Project.objects.filter(**filter).order_by("-created_at")

            return serialize_all(projects), None
        
        except Exception as e:
            return None, CustomError(str(e))
        

    def list_testimonials(self, context, args) -> (list, any): # type: ignore
        try:
            is_featured = args.get("is_featured", False)
            filter = {}
            if is_featured:
                filter["is_featured"] = is_featured
            
            testimonials = Testimonial.objects.filter(**filter).order_by("-created_at")

            return serialize_all(testimonials), None
        
        except Exception as e:
            return None, CustomError(str(e))
        

    def list_trips(self, context, args) -> (list, any): # type: ignore
        try:
            latest = args.get("latest", False)

            if latest:
                trips = SiteTrip.objects.all().order_by("-created_at")[:5]
            else:
                trips = SiteTrip.objects.all().order_by("-created_at")


            return serialize_all(trips), None
        
        except Exception as e:
            return None, CustomError(str(e))
        

    def get_trip_info(self, context, args) -> (dict, any):
        try:
            id = args.get("trip_id")
            if not id:
                return None, CustomError("trip_id is required")
            
            trip = SiteTrip.objects.get(id=id)

            if not trip:
                return None, CustomError("Trip not found")

            return serialize(trip), None

        except Exception as e:
            return None, CustomError(str(e))
    