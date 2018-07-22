from datetime import datetime
from django.utils import timezone

from account.models import UserORM
from project.entities import Project, WorkTask, WorkedDay, WorkTime
from project.models import ProjectORM, HourPaymentORM, MonthPaymentORM, WorkTaskORM, WorkDayORM, WorkTimeORM
from PayDevs.exceptions import EntityDoesNotExistException, InvalidEntityException, NoPermissionException


#------------------------ Project --------------------------------------------#

class ProjectRepo(object):

    def get(self, user_id, project_id=None, title=None):
        try:
            db_user = UserORM.objects.get(id=user_id)

            if project_id:
                db_project = db_user.projectorm_set.get(id=project_id)
            else:
                db_project = db_user.projectorm_set.get(title=title)

        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise EntityDoesNotExistException

        return self._decode_db_project(db_project)



    def create(self, user_id, title, description, type_of_payment, rate):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM(title=title, description=description, user=db_user,
                                    type_of_payment=type_of_payment)
            db_project.save()
            self._set_rate(db_project, rate)
        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except:
            raise InvalidEntityException(source='repositories', code='could not save',
                                         message="Unable to create such project")

        return self._decode_db_project(db_project)



    def get_all(self, user_id):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_projects = db_user.projectorm_set.all()
        except (UserORM.DoesNotExist, ProjectORM.DoesNotExist):
            raise NoPermissionException(message="Invalid user id")

        projects = [self._decode_db_project(db_project) for db_project in db_projects]
        return projects


    # TODO add 'rate' to update method
    def update(self, user_id, project_id, new_attrs):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = db_user.projectorm_set.get(id=project_id)

            for attr in new_attrs.keys():
                if new_attrs[attr] is not None:
                    if (attr == 'start_date' or attr == 'end_date'):
                        db_project.__dict__[attr] = datetime.strptime(new_attrs[attr], "%Y-%m-%dT%H:%M:%S.%fZ")
                    else:
                        db_project.__dict__[attr] = new_attrs[attr]

            db_project.save()

        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")
        except (KeyError, ValueError):
            raise InvalidEntityException(source='repositories', code='not allowed',
                                         message="Unable to update project with provided attr '%s'" % attr)
        except:
            raise InvalidEntityException(source='repositories', code='not allowed',
                                         message="Unable to update project")
        return self._decode_db_project(db_project)



    def delete(self, user_id, project_id):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)

            project = self._decode_db_project(db_project)
            db_project.delete()
        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")

        return project




    def get_type_of_payment(self, user_id, project_id):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)

            type_of_payment = db_project.type_of_payment


        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")

        return type_of_payment



    def get_worked(self, project_id, type_of_payment, start_date_boundary=None, end_date_boundary=None):
        try:
            db_project = ProjectORM.objects.get(id=project_id)

            if (type_of_payment == 'H_P'):
                start_date_boundary = datetime.strptime(start_date_boundary, "%Y-%m-%dT%H:%M:%S.%fZ")
                end_date_boundary = datetime.strptime(end_date_boundary, "%Y-%m-%dT%H:%M:%S.%fZ")
                return self._get_worked_time(db_project, start_date_boundary, end_date_boundary)

            elif (type_of_payment == 'M_P'):
                return self._get_worked_days(db_project)

            else:
                return self._get_worked_tasks(db_project)


        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")
        except:
            raise InvalidEntityException(source='repositories', code='could not get worked',
                                         message="Unable to get worked in '%s' type of payment" % type_of_payment)


    def _get_worked_tasks(self, db_project):
        db_worked_tasks = db_project.worktaskorm_set.filter(completed=True, paid=False)

        worked_tasks = [WorkTaskRepo()._decode_db_work_task(db_work_task) for db_work_task in db_worked_tasks]

        return worked_tasks


    def _get_worked_days(self, db_project):
        db_month_payments = MonthPaymentORM.objects.filter(project=db_project)
        worked_days = list()

        for db_month_payment in db_month_payments:
            for db_worked_day in db_month_payment.workdayorm_set.exclude(day__gte=timezone.now().replace(day=1).date(),
                                                                         paid=False):
                worked_days.append(WorkDayRepo()._decode_db_work_day(db_worked_day, db_month_payment.rate))

        return worked_days


    def _get_worked_time(self, db_project, start_boundary, end_boundary):
        db_hour_payments = HourPaymentORM.objects.filter(project=db_project)
        worked_time_list = list()

        for db_hour_payment in db_hour_payments:
            for db_worked_time in db_hour_payment.worktimeorm_set.filter(start_work__gte=start_boundary,
                                                                         end_work__lte=end_boundary, paid=False):
                worked_time_list.append(WorkTimeRepo()._decode_db_work_time(db_worked_time, db_hour_payment.rate))

        return worked_time_list



    def get_bill(self, project_id, type_of_payment, timestamp, total):
        try:
            db_project = ProjectORM.objects.get(id=project_id)

            title = db_project.title

            bill = {
                'title': title,
                'type_of_payment': type_of_payment,
                'total': total
            }

            if (timestamp):
                bill.update(timestamp)


        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")

        return bill



    def _decode_db_project(self, db_project):
        fileds = {
            'id': db_project.id,
            'user': str(db_project.user),
            'title': db_project.title,
            'description': db_project.description,
            'start_date': db_project.start_date,
            'end_date': db_project.end_date,
            'type_of_payment': db_project.type_of_payment,
            'status': db_project.status
        }

        return Project(**fileds)


    def _set_rate(self, db_project, rate):

        if (db_project.type_of_payment == 'H_P'):
            HourPaymentORM(project=db_project, rate=rate).save()

        elif (db_project.type_of_payment == 'M_P'):
            MonthPaymentORM(project=db_project, rate=rate).save()


#-------------------------- Work Task ----------------------------------------#

class WorkTaskRepo(object):

    def get(self, user_id, project_id, task_id, title):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)

            if task_id:
                db_work_task = WorkTaskORM.objects.get(project=db_project, id=task_id)
            else:
                db_work_task = WorkTaskORM.objects.get(project=db_project, title=title)

        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")
        except WorkTaskORM.DoesNotExist:
            raise EntityDoesNotExistException

        return self._decode_db_work_task(db_work_task)



    def create(self, user_id, project_id, title, description, price):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)

            db_work_task = WorkTaskORM(project=db_project, title=title, description=description, price=price)
            db_work_task.save()

        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")
        except:
            raise InvalidEntityException(source='repositories', code='could not save',
                                         message="Unable to create such task")

        return self._decode_db_work_task(db_work_task)



    def update(self, user_id, project_id, task_id, new_attrs):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)
            db_work_task = WorkTaskORM.objects.get(project=db_project, id=task_id)

            for attr in new_attrs.keys():
                if new_attrs[attr] is not None:
                    db_work_task.__dict__[attr] = new_attrs[attr]

            db_work_task.save()

        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")
        except WorkTaskORM.DoesNotExist:
            raise NoPermissionException(message="Invalid task id")
        except (KeyError, ValueError):
            raise InvalidEntityException(source='repositories', code='could not update',
                                         message="'%s' attribute is invalid" % attr)
        except:
            raise InvalidEntityException(source='repositories', code='not allowed',
                                         message="Unable to update task")

        return self._decode_db_work_task(db_work_task)



    def delete(self, user_id, project_id, task_id):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)
            db_task = WorkTaskORM.objects.get(project=db_project, id=task_id)

            task = self._decode_db_work_task(db_task)
            db_task.delete()
        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")

        return task



    def get_all(self, user_id, project_id):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)

            db_work_tasks = db_project.worktaskorm_set.all()

        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")
        except:
            raise InvalidEntityException(source='repositories', code='could not find',
                                         message="Unable to find tasks in specified project")

        return [self._decode_db_work_task(db_task) for db_task in db_work_tasks]



    def _decode_db_work_task(self, db_work_task):
        fields = {
            'id': db_work_task.id,
            'project': str(db_work_task.project),
            'title': db_work_task.title,
            'description': db_work_task.description,
            'price': db_work_task.price,
            'completed': db_work_task.completed,
            'paid': db_work_task.paid
        }

        return WorkTask(**fields)


# ------------------------- Work Day -------------------------------------- #

class WorkDayRepo(object):

    def get(self, user_id, project_id, month_payment_id, work_day_id):
        try:
            db_project = ProjectORM.objects.get(user_id=user_id, id=project_id)
            db_month_payment = MonthPaymentORM.objects.get(project=db_project, id=month_payment_id)
            db_worked_day = WorkDayORM.objects.get(month_payment=db_month_payment, id=work_day_id)


        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user or project id")
        except MonthPaymentORM.DoesNotExist:
            raise InvalidEntityException(source='repositories', code='could not find',
                                         message="Unable to find specified month_payment")
        except:
            raise InvalidEntityException(source='repositories', code='could not find',
                                         message="Unable to find specified worked day")

        return self._decode_db_work_day(db_worked_day, db_month_payment.rate)




    def create(self, user_id, project_id, month_payment_id, day):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)

            db_month_payment = MonthPaymentORM.objects.get(project=db_project, id=month_payment_id)

            if day is not None:
                day = datetime.strptime(day, "%Y-%m-%d").date()

            db_worked_day = WorkDayORM(month_payment=db_month_payment, day=day)

            db_worked_day.save()

        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")
        except MonthPaymentORM.DoesNotExist:
            raise InvalidEntityException(source='repositories', code='not found',
                                         message="Invalid MonthPayment id")
        except:
            raise InvalidEntityException(source='repositories', code='could not save',
                                         message="Unable to create such worked day")
        return self._decode_db_work_day(db_worked_day, db_month_payment.rate)



    def update(self, user_id, project_id, month_payment_id, work_day_id, new_attrs):
        try:
            db_project = ProjectORM.objects.get(user_id=user_id, id=project_id)
            db_month_payment = MonthPaymentORM.objects.get(project=db_project, id=month_payment_id)
            db_worked_day = WorkDayORM.objects.get(month_payment=db_month_payment, id=work_day_id)

            for attr in new_attrs.keys():
                if new_attrs[attr] is None:
                    continue
                elif (attr == 'day'):
                    db_worked_day.__dict__[attr] = datetime.strptime(new_attrs[attr], "%Y-%m-%d").date()
                else:
                    db_worked_day.__dict__[attr] = new_attrs[attr]

            db_worked_day.save()

        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user or project id")
        except MonthPaymentORM.DoesNotExist:
            raise NoPermissionException(message="Invalid month_payment id")
        except (ValueError, KeyError):
            raise InvalidEntityException(source='repositories', code='could not update',
                                         message="'%s' attribute is invalid" % attr)
        except:
            raise InvalidEntityException(source='repositories', code='could not update',
                                         message="Unable to update this work_day")

        return self._decode_db_work_day(db_worked_day, db_month_payment.rate)



    def delete(self, user_id, project_id, month_payment_id, work_day_id):
        try:
            db_project = ProjectORM.objects.get(user_id=user_id, id=project_id)
            db_month_payment = MonthPaymentORM.objects.get(project=db_project, id=month_payment_id)
            db_worked_day = WorkDayORM.objects.get(month_payment=db_month_payment, id=work_day_id)

            deleted_work_day = self._decode_db_work_day(db_worked_day, db_month_payment.rate)
            db_worked_day.delete()

        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user or project id")
        except MonthPaymentORM.DoesNotExist:
            raise NoPermissionException(message="Invalid month_payment id")
        except:
            raise InvalidEntityException(source='repositories', code='could not update',
                                         message="Could not delete this work_day")

        return deleted_work_day



    def get_all(self, user_id, project_id):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)

            worked_days = list()

            for db_month_payment in db_project.monthpaymentorm_set.all():
                for db_work_day in db_month_payment.workdayorm_set.all():
                    worked_days.append(self._decode_db_work_day(db_work_day, db_month_payment.rate))

        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")
        except:
            raise InvalidEntityException(source='repositories', code='could not find',
                                         message="Unable to find work day in specified project")

        return worked_days



    def _decode_db_work_day(self, db_work_day, rate):
        fields = {
            'id': db_work_day.id,
            'day': db_work_day.day,
            'paid': db_work_day.paid,
            'rate': rate
        }

        return WorkedDay(**fields)


# ---------------------------- Work Time ------------------------------------ #

class WorkTimeRepo(object):

    def get(self, user_id, project_id, hour_payment_id, work_time_id):
        try:
            db_project = ProjectORM.objects.get(user_id=user_id, id=project_id)
            db_hour_payment = HourPaymentORM.objects.get(project=db_project, id=hour_payment_id)
            db_worked_time = WorkTimeORM.objects.get(hour_payment=db_hour_payment, id=work_time_id)

        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user or project id")
        except HourPaymentORM.DoesNotExist:
            raise InvalidEntityException(source='repositories', code='could not find',
                                         message="Unable to find specified hour_payment")
        except:
            raise InvalidEntityException(source='repositories', code='could not find',
                                         message="Unable to find specified worked time")

        return self._decode_db_work_time(db_worked_time, db_hour_payment.rate)



    def create(self, user_id, project_id, hour_payment_id, start_work, end_work):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)

            db_hour_payment = HourPaymentORM.objects.get(project=db_project, id=hour_payment_id)

            if start_work is not None:
                start_work = datetime.strptime(start_work, "%Y-%m-%dT%H:%M:%S.%fZ")
            if end_work is not None:
                end_work = datetime.strptime(end_work, "%Y-%m-%dT%H:%M:%S.%fZ")

            db_worked_time = WorkTimeORM(hour_payment=db_hour_payment, start_work=start_work, end_work=end_work)
            db_worked_time.save()

        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")
        except HourPaymentORM.DoesNotExist:
            raise InvalidEntityException(source='repositories', code='not found',
                                         message="Invalid HourPayment id")
        except:
            raise InvalidEntityException(source='repositories', code='could not save',
                                         message="Unable to create such worked day")
        return self._decode_db_work_time(db_worked_time, db_hour_payment.rate)



    def update(self, user_id, project_id, hour_payment_id, work_time_id, new_attrs):
        try:
            db_project = ProjectORM.objects.get(user_id=user_id, id=project_id)
            db_hour_payment = HourPaymentORM.objects.get(project=db_project, id=hour_payment_id)
            db_worked_time = WorkTimeORM.objects.get(hour_payment=db_hour_payment, id=work_time_id)

            for attr in new_attrs.keys():
                if new_attrs[attr] is None:
                    continue
                elif (attr == 'start_work' or attr == 'end_work'):
                    db_worked_time.__dict__[attr] = datetime.strptime(new_attrs[attr], "%Y-%m-%dT%H:%M:%S.%fZ")
                else:
                    db_worked_time.__dict__[attr] = new_attrs[attr]

            db_worked_time.save()

        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user or project id")
        except HourPaymentORM.DoesNotExist:
            raise NoPermissionException(message="Invalid hour_payment id ")
        except (ValueError, KeyError):
            raise InvalidEntityException(source='repositories', code='could not update',
                                         message="'%s' attribute is invalid" % attr)        
        except:
            raise InvalidEntityException(source='repositories', code='could not update',
                                         message="Unable to update this work_time")

        return self._decode_db_work_time(db_worked_time, db_hour_payment.rate)



    def delete(self, user_id, project_id, hour_payment_id, work_time_id):
        try:
            db_project = ProjectORM.objects.get(user_id=user_id, id=project_id)
            db_hour_payment = HourPaymentORM.objects.get(project=db_project, id=hour_payment_id)
            db_worked_time = WorkTimeORM.objects.get(hour_payment=db_hour_payment, id=work_time_id)

            deleted_work_time = self._decode_db_work_time(db_worked_time, db_hour_payment.rate)
            db_worked_time.delete()

        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user or project id")
        except HourPaymentORM.DoesNotExist:
            raise NoPermissionException(message="Invalid hour_payment id")
        except:
            raise InvalidEntityException(source='repositories', code='could not delete',
                                         message="Unable to delete the work_time")

        return deleted_work_time



    def get_all(self, user_id, project_id):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)

            worked_time_list = list()
            for db_hour_payment in db_project.hourpaymentorm_set.all():
                for db_work_time in db_hour_payment.worktimeorm_set.all():
                    worked_time_list.append(self._decode_db_work_time(db_work_time, db_hour_payment.rate))

        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")
        except ProjectORM.DoesNotExist:
            raise NoPermissionException(message="Invalid project id")
        except:
            raise InvalidEntityException(source='repositories', code='could not find',
                                         message="Unable to find tasks in specified project")

        return worked_time_list



    def _decode_db_work_time(self, db_work_time, rate):
        fields = {
            'id': db_work_time.id,
            'start_work': db_work_time.start_work,
            'end_work': db_work_time.end_work,
            'paid': db_work_time.paid,
            'rate': rate
        }

        return WorkTime(**fields)
