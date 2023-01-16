from django.shortcuts import render
import io
from .serializers import StudentSerializer
from .models import Student
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def student_create(request):
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id', None)
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')

        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    # if request.method == 'POST':
    #     json_data = request.body
    #     stream = io.BytesIO(json_data)
    #     pythondata = JSONParser().parse(stream)
    #     serializer = StudentSerializer(data=pythondata)
    #     if serializer.is_valid():
    #         serializer.save()
    #         res = {'msg': 'Data Created'}
    #         json_data = JSONRenderer().render(res)
    #         print(json_data)
    #         return HttpResponse(json_data, content_type='application/json')
    #     json_data = JSONRenderer().render(serializer.errors)
    #     return HttpResponse(json_data, content_type='application/json')

    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        # serializer= Studentserializer(stu,data = pythondata)
        serializer = StudentSerializer(stu, data=pythondata, partial=True)
        if serializer.is_valid():
            res = {'msg', 'Data Updated'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        stu.delete()
        res = {'msg': 'Data Deleted'}
        return JsonResponse(res, safe=False)

