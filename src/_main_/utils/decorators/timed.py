import functools
import threading
import time


def timed(func):
	"""
	When you add this annotation on top of a function, it will compute the latency of that
	function and send it to cloudwatch for logging and tracking.

	"""
	
	@functools.wraps(func)
	def wrap(*args, **kwargs):
		start_time = time.time()
		try:
			return func(*args, **kwargs)
		finally:

			# If the random number exceeds the chance/capture_rate, just just stop
			# calculate the execution time in milliseconds
			execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
			# Log the execution time
			print(f"Execution time for {func.__name__} is {execution_time}ms")
	
	wrap.__doc__ = func.__doc__
	wrap.__name__ = func.__name__
	return wrap