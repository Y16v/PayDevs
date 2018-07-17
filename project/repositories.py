from account.models import UserORM
from project.entities import Project, WorkTask
from project.models import ProjectORM, HourPaymentORM, MonthPaymentORM, WorkTaskORM
from PayDevs.exceptions import EntityDoesNotExistException, InvalidEntityException, NoPermissionException


#------------------------ Project --------------------------------------------#

class ProjectRepo(object):

    def get_project(self, user_id, project_id=None, title=None):
        try:
            db_user = UserORM.objects.get(id=user_id)

            if project_id:
                db_project = db_user.projectorm_set.get(id=project_id)
            else:
                db_project = db_user.projectorm_set.get(title=title)

        except (UserORM.DoesNotExist, ProjectORM.DoesNotExist):
            raise EntityDoesNotExistException

        return self._decode_db_project(db_project)



    def create_project(self, user_id, title, description, type_of_payment, rate):
        try:
            db_user = UserORM.objects.get(id=user_id)
        except UserORM.DoesNotExist:
            raise NoPermissionException(message="Invalid user id")

        try:
            db_project = ProjectORM(title=title, description=description, user=db_user,
                                    type_of_payment=type_of_payment)
            db_project.save()
            self._set_rate(db_project, rate)
        except:
            raise InvalidEntityException(source='repositories', code='could not save',
                                         message="Unable to create such project")

        return self._decode_db_project(db_project)



    def get_all_projects(self, user_id):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_projects = db_user.projectorm_set.all()
        except (UserORM.DoesNotExist, ProjectORM.DoesNotExist):
            raise NoPermissionException(message="Invalid user id")

        projects = [self._decode_db_project(db_project) for db_project in db_projects]
        return projects



    def update_project(self, user_id, project_id, new_attrs):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = db_user.projectorm_set.get(id=project_id)
        except (UserORM.DoesNotExist, ProjectORM.DoesNotExist):
            raise NoPermissionException(message="Invalid user or project id")

        try:
            for key in new_attrs.keys():
                if new_attrs[key] is not None:
                    db_project.__dict__[key] = new_attrs[key]

            db_project.save()
        except:
            raise InvalidEntityException(source='repositories', code='not allowed',
                                         message="Unable to update project with provided attr "+ str(key))
        return self._decode_db_project(db_project)



    def get_total(self, user_id, project_id):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)
        except (UserORM.DoesNotExist, ProjectORM.DoesNotExist):
            raise NoPermissionException(message="Invalid user or project id")

        if (db_project.type_of_payment.lower() == 'h_p'):
            raise NotImplementedError
        elif (db_project.type_of_payment.lower() == 'm_p'):
            raise NotImplementedError
        else:
            return self._get_tasks_total(db_project)



    def _get_tasks_total(self, db_project):
        try:
            tasks = db_project.worktaskorm_set.all()
            total = 0
            for task in tasks:
                if (task.completed and not task.paid):
                    total += task.price
        except:
            raise InvalidEntityException(source='repositories', code='could not sum total',
                                         message="'%s' task attribute is invalid" % task.title)
        return total



    def _decode_db_project(self, db_project):
        fileds = {
            'id': db_project.id,
            'user': str(db_project.user),
            'title': db_project.title,
            'description': db_project.description,
            'start_date': str(db_project.start_date),
            'end_date': str(db_project.end_date),
            'type_of_payment': db_project.type_of_payment,
            'status': db_project.status
        }

        return Project(**fileds)


    def _set_rate(self, db_project, rate):
        if (db_project.type_of_payment.lower() == 'h_p'):
            HourPaymentORM(project=db_project, rate=rate).save()
        elif (db_project.type_of_payment.lower() == 'm_p'):
            MonthPaymentORM(project=db_project, rate=rate).save()


#-------------------------- Work Task ----------------------------------------#

class WorkTaskRepo(object):

    def get_task(self, user_id, project_id, task_id, title):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)
        except (UserORM.DoesNotExist, ProjectORM.DoesNotExist):
            raise NoPermissionException(message="Invalid user or project id")

        try:
            if task_id:
                db_work_task = WorkTaskORM.objects.get(project=db_project, id=task_id)
            else:
                db_work_task = WorkTaskORM.objects.get(project=db_project, title=title)
        except WorkTaskORM.DoesNotExist:
            raise EntityDoesNotExistException

        return self._decode_db_work_task(db_work_task)



    def create_work_task(self, user_id, project_id, title, description, price):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)
        except (UserORM.DoesNotExist, ProjectORM.DoesNotExist):
            raise NoPermissionException(message="Invalid user or project id")

        try:
            db_work_task = WorkTaskORM(project=db_project, title=title, description=description, price=price)
            db_work_task.save()
        except:
            raise InvalidEntityException(source='repositories', code='could not save',
                                         message="Unable to create such task")

        return self._decode_db_work_task(db_work_task)



    def get_all_tasks(self, user_id, project_id):
        try:
            db_user = UserORM.objects.get(id=user_id)
            db_project = ProjectORM.objects.get(user=db_user, id=project_id)
        except (UserORM.DoesNotExist, ProjectORM.DoesNotExist):
            raise NoPermissionException(message="Invalid user or project id")

        try:
            db_work_tasks = db_project.worktaskorm_set.all()
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
