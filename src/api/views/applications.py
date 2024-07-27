from _main_.utils.commons import serialize, serialize_all
from _main_.utils.errors import CustomError
from database.models import Application


class ApplicationsView:
    """
    Service Layer for all applications
    """

    def __init__(self):
        pass

    def create_application(self, context, args) -> (dict, any):  # type: ignore
        """
        Create a new application
        """
        try:
            application = Application.objects.create(
                full_name=args.get("full_name"),
                email=args.get("email"),
                school=args.get("school"),
                program=args.get("program"),
                picture=args.get("picture"),
                resume=args.get("resume"),
                motivation=args.get("motivation"),
            )

            # TODO: add a background task to send an email to the user

            return serialize(application), None

        except Exception as e:
            return None, CustomError(str(e), status=400)
