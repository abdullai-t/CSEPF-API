"""
Definition of the different Massenergize Error Types
"""
from _main_.utils.custom_response import CustomResponse


class APIError(CustomResponse):
	def __init__(self, msg="unknown_error", status=400):
		self.msg = msg
		self.status = status
		super().__init__(error=msg, status=200)
	
	def __str__(self):
		return self.msg


class NotAuthorizedError(APIError):
	def __init__(self):
		super().__init__("permission_denied", 403)


class InvalidResourceError(APIError):
	def __init__(self):
		super().__init__("invalid_resource", 404)


class ServerError(APIError):
	def __init__(self):
		super().__init__("server_error", 500)


class CustomError(APIError):
	def __init__(self, err_msg):
		super().__init__(str(err_msg), 200)
