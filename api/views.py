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
                'status':400
            })
        password = data['password']
        if password != extract_password(email):
            return Response({
                'message': 'Invalid email or password',
                'status':400
            })
        return Response({
            'name': extract_password(email),
            'email': email,
            'status': 200,
            'role': role
        })
    except Exception as e:
        return Response({
            "status": 500,
            "message": 'Internal server error',
            "error": str(e),
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
                'status': 400
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
    TODO: Return the response in names instead of ids
'''
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
                'request_id': row[0],
                'student_id': row[1],
                'project_id': row[2],
                'equipment_id': row[3],
                'equipment_name': row[4]
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
                       SELECT out_request_id, out_student_id, out_project_id, out_equipment_id, out_equipment_name, out_project_name, out_full_name
                       FROM gpt_request_for_faculty_incharge(%s);
                   ''', [email])
            raw_query_set = cursor.fetchall()
        result_list = []
        for row in raw_query_set:
            result_list.append({
                'request_id': row[0],
                'student_id': row[1],
                'project_id': row[2],
                'project_name': row[5],
                'equipment_name': row[4],
                'student_name': row[6]
                # 'equipment_name': row[5]
            })
        return Response({
            "status": 200,
            "result": result_list
        })
    except Exception as e:
        print(str(e))
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
                'request_id': row[0],
                'student_id': row[1],
                'project_id': row[2],
                'equipment_id': row[3],
                'equipment_name': row[4]
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
    Send request_id, email and action string as 'true' or 'false'
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
    Send request_id, email and action string as 'true' or 'false'
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
    Send the request_id, email and the action string as 'true' or 'false'
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


'''
    TODO: Add calculate_work_time for student
    TODO: Make sure all triggers are executed properly
    TODO: student request history
    TODO: student project and work hours
    TODO: add student to project, add equipment, add project
    TODO: project_name, number_of_students and remaining funds
    TODO: make requests for students
    
'''
@api_view(['GET'])
def equipment_details(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                select e.equipment_id,e.equipment_name,l.first_name||' '||l.last_name as staff_incharge_name,
                        f.first_name||' '||f.last_name as faculty_incharge_name
                from
                equipment e,lab_staff l,faculty f
                where
                e.faculty_incharge_id=f.faculty_id and e.staff_incharge_id=l.staff_id;
            ''')
            raw_query_set = cursor.fetchall()
        result_list = []
        for row in raw_query_set:
            result_list.append({
                'equipment_id': row[0],
                'equipment_name': row[1],
                'staff_incharge_name': row[2],
                'faculty_incharge_name': row[3],
            })
        return Response({
            "status": 200,
            "equipment": result_list
        })
    except Exception as e:
        return Response({
            'status': 500,
            'message': 'Internal error',
            'error': str(e)
        })

@api_view(['POST'])
def project_details(request):
    try:
        data=request.data
        print(data)
        request_date=data['request_date']

        with connection.cursor() as cursor:
            cursor.execute(f'''
                select r.from_time,r.to_time from request r 
                where DATE(from_time)='{request_date}' and r.request_status='Approved'
                order by r.from_time asc;
            ''')
            raw_query_set = cursor.fetchall()
        result_list = []
        for row in raw_query_set:
            result_list.append({
                'from_time': row[0],
                'to_time': row[1],
            })
        return Response({
            "status": 200,
            "equipment": result_list
        })
    except Exception as e:
        return Response({
            'status': 500,
            'message': 'Internal error',
            'error': str(e)
        })

@api_view(['POST'])
def project_table_update(request):
    try:
        data = request.data
        print(data)
        student_id=data['student_id']
        project_id=data['project_id']
        email_id=data['email']
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'''
                    call add_student_to_project({project_id},{student_id},'{email_id}');
                ''')
        except django.db.utils.InternalError as e:
            return Response({
                'message': 'Exception raised while adding student to project',
                'status': 400,
                'error': str(e)
            })
        return Response({
            "status": 200,
            "message": "student added successfully",
        })
    except Exception as e:
        return Response({
            'status': 500,
            'message': 'Internal error',
            'error': str(e)
        })


