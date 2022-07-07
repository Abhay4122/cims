from rest_framework import status
from rest_framework.response import Response
from django.db import connection

class MainUtils:
	def prin(self, *arg):
		if arg:
			print(f'\n------------------------------\n{arg}\n------------------------------\n')
		else:
			print(f'\n------------------------------\nCheckpoint\n------------------------------\n')


	def resp_fun(self, msg, lod_link, alert_type):
		if alert_type == 'success':
			title = 'Success'
		else:
			title = 'Please notice !'
		return {'title': title, 'msg': msg, 'lod_link': lod_link, 'alert_type': alert_type}


class ViewUtil(MainUtils):
	# def __int__(self):
	# 	self.cursor = connection.cursor()
		
	def get_model_data(self, model, id=None):
		if id:
			return model.objects.filter(id=id)
		else:
			return model.objects.all()


	def get_query(self, query, msg_prifix, load_link=''):
		cursor = connection.cursor()
		cursor.execute(query)
		data = cursor.fetchall()

		if data:
			resp = data
		else:
			msg = f'{msg_prifix} data not found.'
			resp = {
				**{'status': status.HTTP_404_NOT_FOUND},
				**self.resp_fun(msg, load_link, 'error')
			}

		return Response(resp)


	def get(self, request, model, listSerializer, detailSerializer, msg_prifix, load_link='', extra_query = '-'):
		'''
			Get is a method of the View util class which is used to
			get all data of a table OR specific row

			Argument will be request, model, serializer, message prefix
		'''
		if bool(dict(request.GET)):
			# Raw query data
			# get_value = model.objects.raw(f'''select * from eduapi_student where id = {request.GET.get('id')}''')
			if request.GET.get('id'):
				get_value = model.objects.filter(id=request.GET.get('id'))

				if get_value.exists():
					resp = detailSerializer(get_value[0], many=False).data
				else:
					msg = f'{msg_prifix} data not found.'
					resp = {
						**{'status': status.HTTP_404_NOT_FOUND},
						**self.resp_fun(msg, load_link, 'error')
					}

			elif request.GET.get('is_enrolled'):
				resp = listSerializer(model.objects.filter(is_enrolled=request.GET.get('is_enrolled')), many=True).data

		else:
			resp = listSerializer(extra_query if extra_query != '-' else model.objects.all(), many=True).data
		
		return Response(resp)
	
	def post(self, request, serializer, msg_prifix, load_link=''):
		'''
			post is a method of the View util class which is used to
			Save the value in column

			Argument will be request, model, serializer, message prefix
		'''
		serialize = serializer(data=request.data)
		if serialize.is_valid():
			serialize.save()
			
			msg = f'{msg_prifix} successfully !!'
			resp = {
				**{'status': status.HTTP_201_CREATED},
				**self.resp_fun(msg, load_link, 'success')
			}
		else:
			resp = serialize.errors
		
		return Response(resp)
	
	def put(self, request, model, serializer, msg_prifix, load_link=''):
		'''
			Get is a method of the View util class which is used to
			Update the row

			Argument will be request, model, serializer, message prefix
		'''
		if bool(dict(request.GET)):
			get_data = model.objects.filter(id=request.GET.get('id'))
			if get_data.exists():
				serialize = serializer(get_data[0], request.data)
				if serialize.is_valid():
					serialize.save()
					
					msg = f'{msg_prifix} successfully !!'
					resp = {
						**{'status': status.HTTP_201_CREATED},
						**self.resp_fun(msg, load_link, 'success')
					}
				else:
					resp = serialize.errors
			else:
				msg = f'{msg_prifix} data not found'
				resp = {
					**{'status': status.HTTP_404_NOT_FOUND},
					**self.resp_fun(msg, load_link, 'error')
				}
		else:
			msg = f'{msg_prifix} data not found'
			resp = {
				**{'status': status.HTTP_404_NOT_FOUND},
				**self.resp_fun(msg, load_link, 'error')
			}
		
		return Response(resp)
	
	def delete(self, request, model, msg_prifix, load_link=''):
		if bool(dict(request.GET)):
			get_data = model.objects.filter(id=request.GET.get('id'))
			if get_data.exists():
				return_str = get_data[0].__str__()
				get_data.delete()
				msg = f'{msg_prifix} {return_str} had been deleted successfully.'
				resp = {
					**{'status': status.HTTP_200_OK},
					**self.resp_fun(msg, load_link, 'success')
				}
			else:
				msg = f'{msg_prifix} data not found'
				resp = {
					**{'status': status.HTTP_404_NOT_FOUND},
					**self.resp_fun(msg, load_link, 'error')
				}
		else:
			msg = f'{msg_prifix} data not found'
			resp = {
				**{'status': status.HTTP_404_NOT_FOUND},
				**self.resp_fun(msg, load_link, 'error')
			}
		
		return Response(resp)