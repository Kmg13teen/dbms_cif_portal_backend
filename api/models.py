# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Equipment(models.Model):
    equipment_id = models.IntegerField(primary_key=True)
    equipment_name = models.CharField(max_length=100)
    equipment_model = models.CharField(max_length=100)
    staff_incharge = models.ForeignKey('LabStaff', models.DO_NOTHING)
    faculty_incharge = models.ForeignKey('Faculty', models.DO_NOTHING)
    manufacturer = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price_per_hour = models.FloatField(blank=True, null=True)
    condition_of_equipment = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'equipment'


class Faculty(models.Model):
    faculty_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.CharField(unique=True, max_length=50)
    designation = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    office_phone = models.BigIntegerField()
    personal_phone = models.BigIntegerField()
    total_funds = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'faculty'


class LabStaff(models.Model):
    staff_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.CharField(unique=True, max_length=50)
    office_phone = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'lab_staff'


class Project(models.Model):
    project_id = models.IntegerField(primary_key=True)
    project_name = models.CharField(unique=True, max_length=100)
    faculty = models.ForeignKey(Faculty, models.DO_NOTHING)
    project_funds = models.FloatField()

    class Meta:
        managed = False
        db_table = 'project'


class ProjectOfStudent(models.Model):
    project = models.OneToOneField(Project, models.DO_NOTHING, primary_key=True)  # The composite primary key (project_id, active_student_id) found, that is not supported. The first column is selected.
    active_student = models.ForeignKey('Student', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'project_of_student'
        unique_together = (('project', 'active_student'),)


class Request(models.Model):
    request_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Student', models.DO_NOTHING)
    project = models.ForeignKey(Project, models.DO_NOTHING)
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING)
    from_time = models.DateTimeField(blank=True, null=True)
    to_time = models.DateTimeField(blank=True, null=True)
    supervisor_approval = models.BooleanField(blank=True, null=True)
    faculty_incharge_approval = models.BooleanField(blank=True, null=True)
    lab_incharge_approval = models.BooleanField(blank=True, null=True)
    request_status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'request'


class Student(models.Model):
    student_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.CharField(unique=True, max_length=50)
    programme = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    supervisor = models.ForeignKey(Faculty, models.DO_NOTHING)
    personal_phone = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'student'
