from django.http import HttpResponse
from django.template import loader
# from django.db import connections # to get data using sql syntax
from django.utils import timezone

from .models import \
    PostgreSQLDepartments, SQLServerDepartments, \
    PostgreSQLEvents, SQLServerEvents, \
    PostgreSQLInstrument, SQLServerInstrument, \
    PostgreSQLInstrumentGroup,  SQLServerInstrumentGroup, \
    SyncHistory

def index(request):
    syncList = list(SyncHistory.objects.all())

    # initialize the values
    if len(syncList) == 0:
        tableNames = ['instrument_group', 'instrument', 'events', 'departments']

        for tableName in tableNames:
            syncHistory = SyncHistory()
            syncHistory.tablename = tableName
            syncHistory.lastupdate = timezone.now()
            syncHistory.save()

            if tableName == 'departments':
                # populate data to the department table in PostgreSQL
                sqlServerData = list(SQLServerDepartments.objects.using('customers').all())
                for data in sqlServerData:
                    # create procedure
                    if not PostgreSQLDepartments.objects.filter(deptcode=data.deptcode).exists():
                        postgreSQLData = PostgreSQLDepartments()
                        fields = data._meta.get_fields()
                        for field in fields:
                            setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                        postgreSQLData.save()

            elif tableName == 'events':
                # populate data to the event table in PostgreSQL
                sqlServerData = list(SQLServerEvents.objects.using('customers').all())
                for data in sqlServerData:
                    # create procedure
                    if not PostgreSQLEvents.objects.filter(id=data.id).exists():
                        postgreSQLData = PostgreSQLEvents()
                        fields = data._meta.get_fields()
                        for field in fields:
                            setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                        postgreSQLData.save()

            elif tableName == 'instrument':
                # populate data to the instrument table in PostgreSQL
                sqlServerData = list(SQLServerInstrument.objects.using('customers').all())
                for data in sqlServerData:
                    # create procedure
                    if not PostgreSQLInstrument.objects.filter(id=data.id).exists():
                        postgreSQLData = PostgreSQLInstrument()
                        fields = data._meta.get_fields()
                        for field in fields:
                            setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                        postgreSQLData.save()

            elif tableName == 'instrument_group':
                # populate data to the instrument_group table in PostgreSQL
                sqlServerData = list(SQLServerInstrumentGroup.objects.using('customers').all())
                for data in sqlServerData:
                    # create procedure
                    if not PostgreSQLInstrumentGroup.objects.filter(id=data.id).exists():
                        postgreSQLData = PostgreSQLInstrumentGroup()
                        fields = data._meta.get_fields()
                        for field in fields:
                            setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                        postgreSQLData.save()

    # get the synchronization history
    syncList = list(SyncHistory.objects.all())

    template = loader.get_template('replicationapp/index.html')
    context = {
        'syncList': syncList,
    }

    return HttpResponse(template.render(context, request))

    # to get data using sql syntax
    # to use this please uncomment "from django.db import connections"
    # with connections['customers'].cursor() as cursor:
    #     cursor.execute("SELECT * FROM departments")
    #     row = cursor.fetchall()    
    # return HttpResponse(row)

def testing(request):
    # updating a row into Department table in SQL Server
    # the same data in PostgreSQL will be updated with this change
    sqlServerData = SQLServerDepartments.objects.using('customers').get(pk='18')
    sqlServerData.deptname = '皮膚科'
    sqlServerData.if_updt = timezone.now()
    sqlServerData.save()

    # adding a row into Department table in PostgreSQL
    # this data will be deleted because it does not exist in SQL Server
    deletedData = PostgreSQLDepartments()
    deletedData.deptcode = '99'
    deletedData.deptname = 'delete me'
    deletedData.save()

    # updating a row into Event table in SQL Server
    # the same data in PostgreSQL will be updated with this change
    sqlServerData = SQLServerEvents.objects.using('customers').get(pk='10')
    sqlServerData.gw_updated_at = timezone.now()
    sqlServerData.save()

    # adding a row into Event table in PostgreSQL
    # this data will be deleted because it does not exist in SQL Server
    postgreSQLData = PostgreSQLEvents()
    postgreSQLData.id = '99'
    postgreSQLData.message_header_id = 99
    postgreSQLData.patient_number = 'delete me'
    postgreSQLData.save()

    # updating a row into Instrument table in SQL Server
    # the same data in PostgreSQL will be updated with this change
    sqlServerData = SQLServerInstrument.objects.using('customers').get(pk='233')
    sqlServerData.name = 'サンダービート'
    sqlServerData.updated_at = timezone.now()
    sqlServerData.save()

    # adding a row into Instrument table in PostgreSQL
    # this data will be deleted because it does not exist in SQL Server
    postgreSQLData = PostgreSQLInstrument()
    postgreSQLData.id = '999'
    postgreSQLData.name = '消して'
    postgreSQLData.instrument_group_id = 46
    postgreSQLData.count = 0
    postgreSQLData.order_number = 0
    postgreSQLData.version = 0
    postgreSQLData.is_deleted = 0
    postgreSQLData.updated_at = timezone.now()
    postgreSQLData.created_at = timezone.now()
    postgreSQLData.save()

    # updating a row into Instrument_Group table in SQL Server
    # the same data in PostgreSQL will be updated with this change
    sqlServerData = SQLServerInstrumentGroup.objects.using('customers').get(pk='46')
    sqlServerData.name = '＜顕微鏡＞'
    sqlServerData.updated_at = timezone.now()
    sqlServerData.save()

    # adding a row into Instrument_Group table in PostgreSQL
    # this data will be deleted because it does not exist in SQL Server
    postgreSQLData = PostgreSQLInstrumentGroup()
    postgreSQLData.id = '99'
    postgreSQLData.name = '消して'
    postgreSQLData.order_number = 0
    postgreSQLData.version = 0
    postgreSQLData.is_deleted = 0
    postgreSQLData.updated_at = timezone.now()
    postgreSQLData.created_at = timezone.now()
    postgreSQLData.save()

    # test updating the synchronization history
    # oneData = SyncHistory.objects.get(tablename='departments')
    # oneData.lastupdate = timezone.now()
    # oneData.save()

    return HttpResponse("Testing data has been generated successfuly.")

def department(request):
    sqlServerData = list(SQLServerDepartments.objects.using('customers').all())
    postgreSQLData = list(PostgreSQLDepartments.objects.all())
    template = loader.get_template('replicationapp/department.html')
    context = {
        'sqlServerData': sqlServerData,
        'postgreSQLData': postgreSQLData
    }
    return HttpResponse(template.render(context, request))

def event(request):
    sqlServerData = list(SQLServerEvents.objects.using('customers').all())
    postgreSQLData = list(PostgreSQLEvents.objects.all())
    template = loader.get_template('replicationapp/event.html')
    context = {
        'sqlServerData': sqlServerData,
        'postgreSQLData': postgreSQLData
    }
    return HttpResponse(template.render(context, request))

def instrument(request):
    sqlServerData = list(SQLServerInstrument.objects.using('customers').all())
    postgreSQLData = list(PostgreSQLInstrument.objects.all())
    template = loader.get_template('replicationapp/instrument.html')
    context = {
        'sqlServerData': sqlServerData,
        'postgreSQLData': postgreSQLData
    }
    return HttpResponse(template.render(context, request))

def instrument_group(request):
    sqlServerData = list(SQLServerInstrumentGroup.objects.using('customers').all())
    postgreSQLData = list(PostgreSQLInstrumentGroup.objects.all())
    template = loader.get_template('replicationapp/instrument_group.html')
    context = {
        'sqlServerData': sqlServerData,
        'postgreSQLData': postgreSQLData
    }
    return HttpResponse(template.render(context, request))

def synchronize(request):
    synchronizedData = []
    
    # get the last synchronization time 
    syncList = list(SyncHistory.objects.all())
    for table in syncList:
        lastUpdate = table.lastupdate

        # check the Departments table
        if table.tablename == 'departments':

            # find data from SQL Server with update time > last synchronization time
            sqlServerData = list(SQLServerDepartments.objects \
                            .using('customers') \
                            .filter(if_updt__gte=lastUpdate))

            # synchronize the data
            for data in sqlServerData:
                # create or update procedures
                if PostgreSQLDepartments.objects.filter(pk=data.pk).exists():
                    postgreSQLData = PostgreSQLDepartments.objects.get(pk=data.pk)
                    fields = data._meta.get_fields()
                    for field in fields:
                        setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                    postgreSQLData.save()
                    synchronizedData.append(['departments', 'Update', postgreSQLData.pk])
                else:
                    postgreSQLData = PostgreSQLDepartments()
                    fields = data._meta.get_fields()
                    for field in fields:
                        setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                    postgreSQLData.save()
                    synchronizedData.append(['departments', 'Create', postgreSQLData.pk])

                # update synchronization history
                s = SyncHistory.objects.get(tablename='departments')
                s.lastupdate = timezone.now()
                s.save()

        # check the Events table
        elif table.tablename == 'events':

            # find data from SQL Server with update time > last synchronization time
            sqlServerData = list(SQLServerEvents.objects \
                            .using('customers') \
                            .filter(gw_updated_at__gte=lastUpdate))

            # synchronize the data
            for data in sqlServerData:
                # create or update procedures
                if PostgreSQLEvents.objects.filter(pk=data.pk).exists():
                    postgreSQLData = PostgreSQLEvents.objects.get(pk=data.pk)
                    fields = data._meta.get_fields()
                    for field in fields:
                        setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                    postgreSQLData.save()
                    synchronizedData.append(['events', 'Update', postgreSQLData.pk])
                else:
                    postgreSQLData = PostgreSQLEvents()
                    fields = data._meta.get_fields()
                    for field in fields:
                        setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                    postgreSQLData.save()
                    synchronizedData.append(['events', 'Create', postgreSQLData.pk])

                # update synchronization history
                s = SyncHistory.objects.get(tablename='events')
                s.lastupdate = timezone.now()
                s.save()

        # check the Instrument table
        elif table.tablename == 'instrument':

            # find data from SQL Server with update time > last synchronization time
            sqlServerData = list(SQLServerInstrument.objects \
                            .using('customers') \
                            .filter(updated_at__gte=lastUpdate))

            # synchronize the data
            for data in sqlServerData:
                # create or update procedures
                if PostgreSQLInstrument.objects.filter(pk=data.pk).exists():
                    postgreSQLData = PostgreSQLInstrument.objects.get(pk=data.pk)
                    fields = data._meta.get_fields()
                    for field in fields:
                        setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                    postgreSQLData.save()
                    synchronizedData.append(['instrument', 'Update', postgreSQLData.pk])
                else:
                    postgreSQLData = PostgreSQLInstrument()
                    fields = data._meta.get_fields()
                    for field in fields:
                        setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                    postgreSQLData.save()
                    synchronizedData.append(['instrument', 'Create', postgreSQLData.pk])

                # update synchronization history
                s = SyncHistory.objects.get(tablename='instrument')
                s.lastupdate = timezone.now()
                s.save()
        
        # check the InstrumentGroup table
        elif table.tablename == 'instrument_group':

            # find data from SQL Server with update time > last synchronization time
            sqlServerData = list(SQLServerInstrumentGroup.objects \
                            .using('customers') \
                            .filter(updated_at__gte=lastUpdate))

            # synchronize the data
            for data in sqlServerData:
                # create or update procedures
                if PostgreSQLInstrumentGroup.objects.filter(pk=data.pk).exists():
                    postgreSQLData = PostgreSQLInstrumentGroup.objects.get(pk=data.pk)
                    fields = data._meta.get_fields()
                    for field in fields:
                        setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                    postgreSQLData.save()
                    synchronizedData.append(['instrument_group', 'Update', postgreSQLData.pk])
                else:
                    postgreSQLData = PostgreSQLInstrumentGroup()
                    fields = data._meta.get_fields()
                    for field in fields:
                        setattr(postgreSQLData, field.attname, getattr(data, field.attname))
                    postgreSQLData.save()
                    synchronizedData.append(['instrument_group', 'Create', postgreSQLData.pk])

                # update synchronization history
                s = SyncHistory.objects.get(tablename='instrument_group')
                s.lastupdate = timezone.now()
                s.save()
    
    # delete data in PostgreSQL that does not exist in SQL Server
    for table in syncList:
        
        # check departments table
        if table.tablename == 'departments':
            postgreSQLData = list(PostgreSQLDepartments.objects.all())
            for data in postgreSQLData:
                if not SQLServerDepartments.objects.using('customers').filter(pk=data.pk).exists():
                    synchronizedData.append(['departments', 'Delete', data.pk])
                    data.delete()

        # check events table
        elif table.tablename == 'events':
            postgreSQLData = list(PostgreSQLEvents.objects.all())
            for data in postgreSQLData:
                if not SQLServerEvents.objects.using('customers').filter(pk=data.pk).exists():
                    synchronizedData.append(['events', 'Delete', data.pk])
                    data.delete()

        # check instrument table
        elif table.tablename == 'instrument':
            postgreSQLData = list(PostgreSQLInstrument.objects.all())
            for data in postgreSQLData:
                if not SQLServerInstrument.objects.using('customers').filter(pk=data.pk).exists():
                    synchronizedData.append(['instrument', 'Delete', data.pk])
                    data.delete()
                    
        # check instrument_group table
        elif table.tablename == 'instrument_group':
            postgreSQLData = list(PostgreSQLInstrumentGroup.objects.all())
            for data in postgreSQLData:
                if not SQLServerInstrumentGroup.objects.using('customers').filter(pk=data.pk).exists():
                    synchronizedData.append(['instrument_group', 'Delete', data.pk])
                    data.delete()

    synchronizedData.sort()
    template = loader.get_template('replicationapp/synchronization.html')
    context = {
        'synchronizedData': synchronizedData
    }

    return HttpResponse(template.render(context, request))