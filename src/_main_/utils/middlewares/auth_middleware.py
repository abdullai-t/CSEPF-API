from __future__ import annotations

from typing import Any

import jwt

from _main_.settings import SECRET_KEY
from _main_.utils.context import Context
from _main_.utils.custom_response import CustomResponse
from _main_.utils.errors import CustomError


class AuthMiddleware:
	
	def __init__(self, get_response):
		self.get_response = get_response
	
	def __call__(self, request):
		response = self.get_response(request)
	
		return response
	
	def _get_decoded_token(self, token) -> tuple[Any, None] | tuple[None, CustomError]:
		try:
			payload = jwt.decode(token, SECRET_KEY, algorithm='HS256', options={"verify_exp": False})
			return payload, None
		except jwt.ExpiredSignatureError:
			return None, CustomError('session_expired')
		except jwt.DecodeError:
			return None, CustomError('token_decode_error')
		except jwt.InvalidTokenError:
			return None, CustomError('invalid_token')
		except Exception as e:
			print("Token Decode ERROR: ", str(e))
			return None, CustomError('invalid_token')
	
	def _get_clean_path(self, request):
		try:
			return request.path.split('/')[-1]
		except Exception:
			return request.path
	
	def process_view(self, request, view_func, *view_args, **view_kwargs):
		try:
			ctx = Context()
			
			# set request body
			ctx.set_request_body(request, filter_out=["__token"])
			
			# extract JWT auth token
			cookie_token = request.COOKIES.get('token', None)
			out_token = request.POST.get("__token", None)
			token = cookie_token or out_token
			if token:
				decoded_token, err = self._get_decoded_token(token)
				if err:
					err.delete_cookie('token')
					return err
				
				# at this point the user has an active session
				ctx.set_user_credentials(decoded_token)
				
				# Extend work time when working on the Admin portal so work is not lost
				MAX_AGE = 24 * 60 * 60  # one day
				response = CustomResponse(None)
				
				response.delete_cookie("token")

				response.set_cookie("token", secure=True, value=token, max_age=MAX_AGE, samesite='None')
			
			request.context = ctx
		
		except Exception as e:
			return CustomError(e)


class RemoveHeaders:
	
	def __init__(self, get_response):
		self.get_response = get_response
	
	def __call__(self, request):
		response = self.get_response(request)
		response['Server'] = ''
		return response

