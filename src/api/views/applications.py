from _main_.utils.commons import serialize
from _main_.utils.errors import CustomError
from _main_.utils.utils import send_universal_email
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

            send_universal_email(
                recipients=[args.get("email")],
                subject="Application Received",
                template="application_received",
                template_args={"full_name": args.get("full_name")},
            )

            return serialize(application), None

        except Exception as e:
            return None, CustomError(str(e), status=400)
