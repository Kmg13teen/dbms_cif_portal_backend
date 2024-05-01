Profile (student)
- Request_history (regardless of approval)
- Projects he is working on
- Work time of the student (for each project)



Projects(faculty)
- Shows the projects that the faculty is monitoring
- Faculty can add project
- Faculty can add students to existing projects.
- He can view project_details

When lab_incharge takes action
Request status will change directly to approved or rejected
{
    {
        "request_id":1,
        "student_id":112101037,
        "supervisor_approval": null
    },
    {
        "request_id":2,
        "student_id": 112101025,
        "supervisor_approval":null
    }
}

==>127.0.0.1/api/add_student_to_project

JSON request => { "request_id":1, "action":"accept"} 
JSON response => { "status":200, "message": "accepted request" }
