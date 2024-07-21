from _main_.utils.commons import serialize_all
from database.models import Application


class ApplicationsView:
    """
    Service Layer for all applications
    """

    def __init__(self):
        pass
    
    def get_all_applications(self, context, args):
        applications = Application.objects.all()
        res =  serialize_all(applications)
        return res, None
    
    

