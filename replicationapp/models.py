from datetime import datetime
from django.db import models
from django.utils import timezone

import datetime

class SyncHistory(models.Model):
    tablename = models.CharField(max_length=20)
    lastupdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['tablename']

class PostgreSQLDepartments(models.Model):
    if_indt = models.DateTimeField(default=timezone.now, blank=True, null=True)
    if_updt = models.DateTimeField(default=timezone.now, blank=True, null=True)
    if_seq = models.BigIntegerField(blank=True, null=True)
    if_stt = models.DateTimeField(blank=True, null=True)
    if_pmd = models.CharField(max_length=1, blank=True, null=True)
    hospitalcode = models.CharField(max_length=2, blank=True, null=True)
    deptcode = models.CharField(primary_key= True, max_length=2) # primary key
    deptname = models.CharField(max_length=20, blank=True, null=True)
    deptshortname = models.CharField(max_length=20, blank=True, null=True)
    deptspecialname = models.CharField(max_length=20, blank=True, null=True)
    deptstatus = models.CharField(max_length=1, blank=True, null=True)
    recedeptcode = models.CharField(max_length=2, blank=True, null=True)
    deptseq = models.IntegerField(blank=True, null=True)
    visiblestatus = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return self.deptname
    
    def wasUpdatedRecently(self):
        return self.if_updt >= timezone.now() - datetime.timedelta(minutes=5)

    class Meta:
        ordering = ['-if_updt', 'deptcode']

class SQLServerDepartments(models.Model):
    if_indt = models.DateTimeField(db_column='IF_INDT', blank=True, null=True)  # Field name made lowercase.
    if_updt = models.DateTimeField(db_column='IF_UPDT', blank=True, null=True)  # Field name made lowercase.
    if_seq = models.BigIntegerField(db_column='IF_SEQ', blank=True, null=True)  # Field name made lowercase.
    if_stt = models.DateTimeField(db_column='IF_STT', blank=True, null=True)  # Field name made lowercase.
    if_pmd = models.CharField(db_column='IF_PMD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hospitalcode = models.CharField(db_column='HOSPITALCODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.CharField(db_column='DEPTCODE', primary_key=True, max_length=2)  # Field name made lowercase.
    deptname = models.CharField(db_column='DEPTNAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    deptshortname = models.CharField(db_column='DEPTSHORTNAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    deptspecialname = models.CharField(db_column='DEPTSPECIALNAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    deptstatus = models.CharField(db_column='DEPTSTATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recedeptcode = models.CharField(db_column='RECEDEPTCODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    deptseq = models.IntegerField(db_column='DEPTSEQ', blank=True, null=True)  # Field name made lowercase.
    visiblestatus = models.CharField(db_column='VISIBLESTATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Departments'
        ordering = ['-if_updt', 'deptcode']

class PostgreSQLEvents(models.Model):
    id = models.IntegerField(primary_key=True) # primary key
    message_header_id = models.IntegerField()
    patient_number = models.CharField(max_length=10)
    patient_name_kana = models.CharField(max_length=60, blank=True, null=True)
    patient_name = models.CharField(max_length=30, blank=True, null=True)
    is_inpatient = models.CharField(max_length=1, blank=True, null=True)
    gender = models.CharField(max_length=4, blank=True, null=True)
    birthday = models.CharField(max_length=8, blank=True, null=True)
    order_number = models.CharField(max_length=37, blank=True, null=True)
    event_type = models.CharField(max_length=10)
    event_datetime = models.CharField(max_length=14)
    ope_room_name = models.CharField(max_length=50, blank=True, null=True)
    ope_order_date = models.CharField(max_length=8, blank=True, null=True)
    section_code = models.CharField(max_length=3, blank=True, null=True)
    gaia_pid = models.CharField(max_length=10)
    section_name = models.CharField(max_length=20, blank=True, null=True)
    disease_name = models.CharField(max_length=128, blank=True, null=True)
    pre_operation_name = models.CharField(max_length=512, blank=True, null=True)
    surgeon_doctor = models.CharField(max_length=120, blank=True, null=True)
    assistant = models.CharField(max_length=120, blank=True, null=True)
    anesth_doctor = models.CharField(max_length=120, blank=True, null=True)
    operation_name = models.CharField(max_length=512, blank=True, null=True)
    ope_room_name_from = models.CharField(max_length=50, blank=True, null=True)
    event_note = models.CharField(max_length=2269, blank=True, null=True)
    gw_received_at = models.DateTimeField(blank=True, null=True)
    gw_updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-gw_updated_at', 'id']

class SQLServerEvents(models.Model):
    id = models.IntegerField(primary_key=True)
    message_header_id = models.IntegerField()
    patient_number = models.CharField(max_length=10)
    patient_name_kana = models.CharField(max_length=60, blank=True, null=True)
    patient_name = models.CharField(max_length=30, blank=True, null=True)
    is_inpatient = models.CharField(max_length=1, blank=True, null=True)
    gender = models.CharField(max_length=4, blank=True, null=True)
    birthday = models.CharField(max_length=8, blank=True, null=True)
    order_number = models.CharField(max_length=37, blank=True, null=True)
    event_type = models.CharField(max_length=10)
    event_datetime = models.CharField(max_length=14)
    ope_room_name = models.CharField(max_length=50, blank=True, null=True)
    ope_order_date = models.CharField(max_length=8, blank=True, null=True)
    section_code = models.CharField(max_length=3, blank=True, null=True)
    gaia_pid = models.CharField(max_length=10)
    section_name = models.CharField(max_length=20, blank=True, null=True)
    disease_name = models.CharField(max_length=128, blank=True, null=True)
    pre_operation_name = models.CharField(max_length=512, blank=True, null=True)
    surgeon_doctor = models.CharField(max_length=120, blank=True, null=True)
    assistant = models.CharField(max_length=120, blank=True, null=True)
    anesth_doctor = models.CharField(max_length=120, blank=True, null=True)
    operation_name = models.CharField(max_length=512, blank=True, null=True)
    ope_room_name_from = models.CharField(max_length=50, blank=True, null=True)
    event_note = models.CharField(max_length=2269, blank=True, null=True)
    gw_received_at = models.DateTimeField(blank=True, null=True)
    gw_updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'
        ordering = ['-gw_updated_at', 'id']

class PostgreSQLInstrument(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    instrument_group_id = models.IntegerField()
    count = models.IntegerField()
    effective_start = models.DateField(blank=True, null=True)
    effective_end = models.DateField(blank=True, null=True)
    order_number = models.IntegerField()
    version = models.IntegerField()
    is_deleted = models.IntegerField()
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ['-updated_at', 'id']

class SQLServerInstrument(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    instrument_group_id = models.IntegerField()
    count = models.IntegerField()
    effective_start = models.DateField(blank=True, null=True)
    effective_end = models.DateField(blank=True, null=True)
    order_number = models.IntegerField()
    version = models.IntegerField()
    is_deleted = models.IntegerField()
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instrument'
        ordering = ['-updated_at', 'id']

class PostgreSQLInstrumentGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    order_number = models.IntegerField()
    version = models.IntegerField()
    is_deleted = models.IntegerField()
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ['-updated_at', 'id']

class SQLServerInstrumentGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    order_number = models.IntegerField()
    version = models.IntegerField()
    is_deleted = models.IntegerField()
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instrument_group'
        ordering = ['-updated_at', 'id']
