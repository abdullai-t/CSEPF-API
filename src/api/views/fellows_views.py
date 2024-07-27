from _main_.utils.commons import serialize_all
from database.models import Application


class FellowsView:
    """
    Service Layer for all applications
    """

    def __init__(self):
        pass
    
    def get_fellows_info(self, context, args):
        applications = Application.objects.all()
        res =  serialize_all(applications)
        return res, None
    
    

    def list_fellows(self, context, args):
        try:
            applications = Application.objects.filter(context_filter)  # Add appropriate filters
            res = serialize_all(applications)
            return res, None
        except Exception as e:
            return None, str(e)
    