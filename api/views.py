import django.db.utils
from django.db import connection
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import *
import re



'''
Helper functions
'''
def extract_password(email):
    # Split the email address by '@' symbol and return the part before it
    return email.split('@')[0]
def get_role(email):
    # Regular expression to match the domain part of an email
    pattern = r"@([\w\.-]+)$"
    match = re.search(pattern, email)
    if match:

        if match.group(1) == 'smail.iitpkd.ac.in':
            return 'student'
        elif match.group(1) == 'iitpkd.ac.in':
            return 'faculty'
        elif match.group(1) == 'staff.iitpkd.ac.in':
            return 'lab_staff'
        else:
            return 'Invalid email'
    else:
        return None
def get_email_from_role(name):
    if name.lower() == 'student':
        return '@smail.iitpkd.ac.in'
    elif name.lower() == 'faculty':
        return '@iitpkd.ac.in'
    elif name.lower() == 'lab_staff':
        return '@staff.iitpkd.ac.in'
    else:
        return 'Invalid email'




'''
    Send email and password entered by the user to get his name(id) and role
'''
@api_view(['POST'])
def login(request):
    try:
        data = request.data
        print(data)
        email = data['email']

        # gets the role based on the provided email
        role = get_role(email)

        if role == 'Invalid email':
            return Response({
                'message': 'Invalid email or password',
                'status':402
            })
        password = data['password']
        if password != extract_password(email):
            return Response({
                'message': 'Invalid email or password',
                'status':402
            })
        return Response({
            'name': extract_password(email),
            'status': 200,
            'role': role
        })
    except Exception as e:
        return Response({
            "status": 500,
            "message": 'Internal server error',
            "error": str(e)
        })

'''
    Send name(got from login) and role to get first_name, last_name and ID
'''
@api_view(['POST'])
def whoami(request):
    try:
        data = request.data
        print(data) # role, name
        email = data['name'].lower() + get_email_from_role(data['role'])
        print(email)
        query = f'''
            SELECT * FROM {data['role']} WHERE email_id= '{email}';
        '''
        print(query)
        try:

            ID = 0
            if data['role'] == 'faculty':
                result = Faculty.objects.raw(query)[0]
                first_name = result.first_name
                last_name = result.last_name
                ID = result.faculty_id
            elif data['role'] == 'student':
                result = Student.objects.raw(query)[0]
                first_name = result.first_name
                last_name = result.last_name
                ID = result.student_id
            elif data['role'] == 'lab_staff':
                result = LabStaff.objects.raw(query)[0]
                first_name = result.first_name
                last_name = result.last_name
                ID = result.staff_id
            else:
                first_name = 'null'
                last_name = 'null'
                ID = -1
        except IndexError as e:
            return Response({
                'message': 'User not found',
                'status':402
            })
        return Response({
            "first_name": first_name,
            "last_name": last_name,
            "role": data['role'],
            "id": ID,
            "email": email
        })
    except Exception as e:
        return Response({
            "status": 500,
            "message": 'Internal server error',
            "error": str(e)
        })


'''
    Send the email of the supervisor to get all the requests made to him.
'''
@api_view(['POST'])
def supervisor_requests(request):
    try:
        data = request.data
        email=data['email']
        with connection.cursor() as cursor:
            cursor.execute('''
                   SELECT out_request_id, out_student_id, out_project_id, out_equipment_id, out_equipment_name
                   FROM request_for_supervisor(%s);
               ''', [email])
            raw_query_set = cursor.fetchall()
        result_list = []
        for row in raw_query_set:
            result_list.append({
                'out_request_id': row[0],
                'out_student_id': row[1],
                'out_project_id': row[2],
                'out_equipment_id': row[3],
                'out_equipment_name': row[4]
            })

        return Response({
            "status": 200,
            "result": result_list
        })
    except Exception as e:
        return Response({
            "status": 500,
            "message": 'Internal server error',
            "error": str(e)
        })


'''
    Send the email of the faculty_incharge to get all the requests made to him
'''
@api_view(['POST'])
def faculty_incharge_requests(request):
    try:
        data = request.data
        email = data['email']
        with connection.cursor() as cursor:
            cursor.execute('''
                       SELECT out_request_id, out_student_id, out_project_id, out_equipment_id, out_equipment_name
                       FROM request_for_faculty_incharge(%s);
                   ''', [email])
            raw_query_set = cursor.fetchall()
        result_list = []
        for row in raw_query_set:
            result_list.append({
                'out_request_id': row[0],
                'out_student_id': row[1],
                'out_project_id': row[2],
                'out_equipment_id': row[3],
                'out_equipment_name': row[4]
            })
        return Response({
            "status": 200,
            "result": result_list
        })
    except Exception as e:
        return Response({
            "status": 500,
            "message": 'Internal server error',
            "error": str(e)
        })


@api_view(['POST'])
def lab_staff_requests(request):
    try:
        data = request.data
        email = data['email']
        with connection.cursor() as cursor:
            cursor.execute('''
                       SELECT out_request_id, out_student_id, out_project_id, out_equipment_id, out_equipment_name
                       FROM request_for_lab_incharge(%s);
                   ''', [email])
            raw_query_set = cursor.fetchall()
        result_list = []
        for row in raw_query_set:
            result_list.append({
                'out_request_id': row[0],
                'out_student_id': row[1],
                'out_project_id': row[2],
                'out_equipment_id': row[3],
                'out_equipment_name': row[4]
            })
        return Response({
            "status": 200,
            "result": result_list
        })
    except Exception as e:
        return Response({
            "status": 500,
            "message": 'Internal server error',
            "error": str(e)
        })


'''
    Send request_id and action string as 'true' or 'false'
'''
@api_view(['POST'])
def take_action_supervisor(request):
    try:
        data = request.data
        print(data)
        request_id = data['request_id']
        action = data['action']
        email = data['email']
        query = f'''
                CALL take_action_supervisor({request_id},'{action}','{email}');
            '''
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
        except django.db.utils.InternalError as e:
            return Response({
                'message': 'Exception raised while taking action for supervisor',
                'status':500,
                'error': str(e)
            })
        return Response({
            "status": 200,
            "message": "Action taken successfully",
            "action": action,
        })
    except Exception as e:
        return Response({
            'message': 'Internal error',
            'status':500,
            'error': str(e)
        })


'''
    Send request_id and action string as 'true' or 'false'
'''
@api_view(['POST'])
def take_action_faculty_incharge(request):
    try:
        data = request.data
        print(data)
        request_id = data['request_id']
        action = data['action']
        email = data['email']
        query = f'''
                   CALL take_action_faculty_incharge({request_id},'{action}','{email}');
               '''
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
        except django.db.utils.InternalError as e:
            return Response({
                'message': 'Exception raised while taking action for faculty incharge',
                'status': 500,
                'error': str(e)
            })
        return Response({
            "status": 200,
            "message": "Action taken successfully",
            "action": action,
        })
    except Exception as e:
        return Response({
            'message': 'Internal error',
            'status': 500,
            'error': str(e)
        })


'''
    Send the request_id  and the action string as 'true' or 'false'
'''
@api_view(['POST'])
def take_action_lab_incharge(request):
    try:
        data = request.data
        print(data)
        request_id = data['request_id']
        action = data['action']
        email = data['email']
        query = f'''
                   CALL take_action_lab_incharge({request_id},'{action}','{email}');
               '''
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
        except django.db.utils.InternalError as e:
            return Response({
                'message': 'Exception raised while taking action for lab incharge',
                'status': 500,
                'error': str(e)
            })
        return Response({
            "status": 200,
            "message": "Action taken successfully",
            "action": action,
        })
    except Exception as e:
        return Response({
            'message': 'Internal error',
            'status': 500,
            'error': str(e)
        })