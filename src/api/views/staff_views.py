from _main_.utils.commons import serialize, serialize_all
from _main_.utils.errors import CustomError
from database.models import Staff


class StaffView:
    """
    Service Layer for all applications
    """

    def __init__(self):
        pass
    
    def get_staff_info(self, context, args) -> (dict, any):  # type: ignore
        try:
            id = args.get("staff_id")
            if not id:
                return None, CustomError("staff_id is required", status=400)
            
            staff = Staff.objects.get(id=id)

            if not staff:
                return None, CustomError("Staff not found", status=404)

            return serialize(staff), None

        except Exception as e:
            return None, CustomError(str(e), status=500)
    
    

    def list_staff(self, context, args) -> (list, any):  # type: ignore
        try:
            is_feature = args.get("featured", None)
            filter = {}
            if is_feature:
                filter["featured"] = is_feature

            staff = Staff.objects.filter(**filter).order_by("-created_at")

            return serialize_all(staff), None
        
        except Exception as e:
            print("=====", e)
            return None, CustomError(str(e))
    