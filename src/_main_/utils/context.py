import json
from _main_.utils.commons import get_request_contents, parse_bool


class Context:
    def __init__(self):
        self.args = {}
        self.is_prod = False
        self.user_is_logged_in = False
        self.user_id = None
        self.user_email = None
        self.request = None

    def set_user_credentials(self, decoded_token):
        self.user_is_logged_in = True
        self.user_email = decoded_token.get("email", None)
        self.user_id = decoded_token.get("user_id", None)

    def set_request_body(self, request, **kwargs):
        # get the request args
        self.args = get_request_contents(request, **kwargs)
        self.request = request

    def get_request_body(self):
        return self.args

    def __str__(self):
        return str(
            {
                "args": self.args,
                "is_prod": self.is_prod,
                "user_is_logged_in": self.user_is_logged_in,
                "user_id": self.user_id,
                "user_email": self.user_email,
            }
        )
