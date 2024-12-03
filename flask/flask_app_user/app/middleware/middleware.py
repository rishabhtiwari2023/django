from flask import request, jsonify

def validate_input(required_fields):
	def decorator(fn):
		def wrapper(*args, **kwargs):
			data = request.get_json()
			if not data:
				return jsonify({"msg": "Invalid input"}), 400
			for field in required_fields:
				if field not in data:
					return jsonify({"msg": f"Missing field: {field}"}), 400
			return fn(*args, **kwargs)
		return wrapper
	return decorator