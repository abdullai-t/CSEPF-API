from _main_.utils.commons import serialize, serialize_all
from _main_.utils.errors import CustomError
from database.models import Application, Fellow


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
    