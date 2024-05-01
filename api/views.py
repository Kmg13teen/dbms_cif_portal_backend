from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['POST'])
def login(request):
    data = request.data
    print(data)
    username = data['username']
    password = data['password']
    # query to check if it is okay
    authentication = f'''
        SELECT CASE
           WHEN EXISTS (SELECT 1 FROM  WHERE 'username'='{username}' and 'password'='{password}')
           THEN 1
           ELSE 0
       END AS result;
     '''
    print(authentication)
    return Response({
        'username': username,
        'password': password
    })
