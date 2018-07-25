
from project.factories.repo_factories import ProjectRepoFactory, WorkTaskRepoFactory, HourPaymentRepoFactory, \
    WorkTimeRepoFactory
from project.factories.validator_factories import UserPermissionsValidatorFactory, ProjectDateTimeValidatorFactory


from project.factories.repo_factories import ProjectRepoFactory
from project.factories.validator_factories import UserPermissionsValidatorFactory, ProjectDateTimeValidatorFactory

from project.interactors import CreateProjectInteractor, UpdateProjectInteractor, DeleteProjectInteractor, \
    GetProjectInteractor, GetAllProjectsInteractor, CreateTaskInteractor, GetTaskInteractor, UpdateTaskInteractor, \
    DeleteTaskInteractor, GetAllTasksInteractor, CreateHourPaymentInteractor, GetHourPaymentInteractor, \
    UpdateHourPaymentInteractor, DeleteHourPaymentInteractor, GetAllHourPaymentInteractor, CreateWorkTimeInteractor


class CreateProjectInteractorFactory(object):
    @staticmethod
    def create():
        project_repo = ProjectRepoFactory.create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        project_date_time = ProjectDateTimeValidatorFactory.create()
        return CreateProjectInteractor(project_repo, validate_user_project, project_date_time)


class UpdateProjectInteractorFactory(object):
    @staticmethod
    def create():
        project_repo = ProjectRepoFactory.create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        return UpdateProjectInteractor(project_repo, validate_user_project)


class DeleteProjectInteractorFactory(object):
    @staticmethod
    def create():
        project_repo = ProjectRepoFactory.create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        return DeleteProjectInteractor(project_repo, validate_user_project)



class GetProjectInteractorFactory(object):
    @staticmethod
    def create():
        project_repo = ProjectRepoFactory.create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        return GetProjectInteractor(project_repo, validate_user_project)




class GetAllProjectsInteractorFactory(object):
    @staticmethod
    def create():
        project_repo = ProjectRepoFactory.create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        return GetAllProjectsInteractor(project_repo, validate_user_project)



class CreateTaskInteractorFactory(object):

    @staticmethod
    def create():
        create_task_repo = WorkTaskRepoFactory().create()
        create_project_repo = ProjectRepoFactory().create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        return CreateTaskInteractor(create_task_repo, create_project_repo, validate_user_project)



class GetTaskInteractorFactory(object):
    @staticmethod
    def create():
        create_task_repo = WorkTaskRepoFactory().create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        return GetTaskInteractor(create_task_repo, validate_user_project)





class UpdateTaskInteractorFactory(object):
    @staticmethod
    def create():
        create_task_repo = WorkTaskRepoFactory().create()
        create_project_repo = ProjectRepoFactory().create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        return UpdateTaskInteractor(create_task_repo, create_project_repo, validate_user_project)


class DeleteTaskInteractorFactory(object):
    @staticmethod
    def create():
        create_task_repo = WorkTaskRepoFactory().create()
        create_project_repo = ProjectRepoFactory().create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        return DeleteTaskInteractor(create_task_repo, create_project_repo, validate_user_project)


class GetAllTaskInteractorFactory(object):
    @staticmethod
    def create():
        create_task_repo = WorkTaskRepoFactory().create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        create_project_repo = ProjectRepoFactory().create()
        return GetAllTasksInteractor(create_task_repo, create_project_repo, validate_user_project)



class CreateHourPaymentInteractorFactory():
    @staticmethod
    def create():
        create_hour_payment_repo = HourPaymentRepoFactory().create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        create_project_repo = ProjectRepoFactory().create()
        return CreateHourPaymentInteractor(create_hour_payment_repo, create_project_repo, validate_user_project)



class GetHourPaymentInteractorFactory(object):
    @staticmethod
    def create():
        create_hour_payment_repo = HourPaymentRepoFactory().create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        return GetHourPaymentInteractor(create_hour_payment_repo, validate_user_project)


class GetAllHourPaymentInteractorFactory(object):
    @staticmethod
    def create():
        create_hour_payment_repo = HourPaymentRepoFactory().create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        create_project_repo = ProjectRepoFactory().create()
        return GetAllHourPaymentInteractor(create_hour_payment_repo, create_project_repo, validate_user_project)


class UpdateHourPaymentInteractorFactory(object):
    @staticmethod
    def create():
        create_hour_payment_repo = HourPaymentRepoFactory().create()
        validate_user_project = UserPermissionsValidatorFactory.create()
        create_project_repo = ProjectRepoFactory().create()
        return UpdateHourPaymentInteractor(create_hour_payment_repo, create_project_repo, validate_user_project)


class DeleteHourPaymentInteractorFactory(object):
    @staticmethod
    def create():
        create_hour_payment_repo = HourPaymentRepoFactory().create()
        validate_user_project = UserPermissionsValidatorFactory().create()
        create_project_repo = ProjectRepoFactory().create()
        return DeleteHourPaymentInteractor(create_hour_payment_repo, create_project_repo, validate_user_project)



class CreateWorkTimeInteractorFactory(object):
    @staticmethod
    def create():
        create_hour_payment_repo = WorkTimeRepoFactory().create()
        validate_user_project = UserPermissionsValidatorFactory().create()
        create_project_repo = HourPaymentRepoFactory().create()
        project_date_time = ProjectDateTimeValidatorFactory.create()
        return CreateWorkTimeInteractor(create_hour_payment_repo, create_project_repo,
                                        validate_user_project, project_date_time)
