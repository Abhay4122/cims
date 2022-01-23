from rest_framework import status
from rest_framework.response import Response


def prin(arg):
	if arg:
		print(f'\n------------------------------\n{arg}\n------------------------------\n')
	else:
		print(f'\n------------------------------\nCheckpoint\n------------------------------\n')


def resp_fun(msg, lod_link, alert_type):
	if alert_type == 'success':
		title = 'Success'
	else:
		title = 'Please notice !'
	return {'title': title, 'msg': msg, 'lod_link': lod_link, 'alert_type': alert_type}

class MainUtils:
	def prin(*arg):
		if arg:
			print(f'\n------------------------------\n{arg}\n------------------------------\n')
		else:
			print(f'\n------------------------------\nCheckpoint\n------------------------------\n')


	def resp_fun(msg, lod_link, alert_type):
		if alert_type == 'success':
			title = 'Success'
		else:
			title = 'Please notice !'
		return {'title': title, 'msg': msg, 'lod_link': lod_link, 'alert_type': alert_type}


class ViewUtil(MainUtils):
	# def __int__(self, request):
	# 	self.request = request
		
	def get_model_data(self, model, id=None):
		if id:
			return model.objects.filter(id=id)
		else:
			return model.objects.all()

	def get(self, request, model, serializer, msg_prifix):
		'''
			Get is a method of the View util class which is used to
			get all data of a table OR specific row

			Argument will be request, model, serializer, message prefix
		'''
		if bool(dict(request.GET)):
			get_value = self.get_model_data(model, request.GET.get('id'))
			if get_value.exists():
				resp = serializer(get_value[0], many=False).data
			else:
				msg = f'{msg_prifix} data not found.'
				resp = {
					**{'status': status.HTTP_404_NOT_FOUND},
					**self.resp_fun(msg, '', 'error')
				}
		else:
			self.prin()
			resp = serializer(self.get_model_data(model), many=True).data
		
		return Response(resp)
	
	def post(self, request, model, serializer, msg_prifix):
		'''
			post is a method of the View util class which is used to
			Save the value in column

			Argument will be request, model, serializer, message prefix
		'''
		serialize = serializer(data=request.data)
		if serialize.is_valid():
			serialize.save()
			
			msg = f'{msg_prifix} successfully created !!'
			resp = {
				**{'status': status.HTTP_201_CREATED},
				**resp_fun(msg, '', 'success')
			}
		else:
			resp = serialize.errors
		
		return Response(resp)
	
	def put(self, request, model, serializer, msg_prifix):
		'''
			Get is a method of the View util class which is used to
			Update the row

			Argument will be request, model, serializer, message prefix
		'''
		if bool(dict(request.GET)):
			get_course = ViewUtil.get_model_data(model, request.GET.get('id'))
			if get_course.exists():
				serialize = serializer(get_course[0], request.data)
				if serialize.is_valid():
					serialize.save()
					resp = serialize.data 
				else:
					resp = serialize.errors
			else:
				msg = f'{msg_prifix} data not found'
				resp = {
					**{'status': status.HTTP_404_NOT_FOUND},
					**resp_fun(msg, '', 'error')
				}
		else:
			msg = f'{msg_prifix} data not found'
			resp = {
				**{'status': status.HTTP_404_NOT_FOUND},
				**resp_fun(msg, '', 'error')
			}
		
		return Response(resp)
	
	def delete(self, request, model, serializer, msg_prifix):
		if bool(dict(request.GET)):
			get_course = ViewUtil.get_model_data(model, request.GET.get('id'))
			if get_course.exists():
				course_name = get_course[0].cors_name
				get_course[0].delete()
				msg = f'{msg_prifix} {course_name} had been deleted successfully.'
				resp = {
					**{'status': status.HTTP_200_OK},
					**resp_fun(msg, '', 'success')
				}
			else:
				msg = f'{msg_prifix} data not found'
				resp = {
					**{'status': status.HTTP_404_NOT_FOUND},
					**resp_fun(msg, '', 'error')
				}
		else:
			msg = f'{msg_prifix} data not found'
			resp = {
				**{'status': status.HTTP_404_NOT_FOUND},
				**resp_fun(msg, '', 'error')
			}
		
		return Response(resp)