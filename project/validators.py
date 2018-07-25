from time import localtime

from PayDevs.exceptions import NoLoggedException, NoPermissionException, InvalidEntityException
import datetime


class UserPermissionValidator:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def validate_permission(self, logged_id, user_id=None):
        if logged_id is None:
            raise NoLoggedException
        if user_id is not None and logged_id != user_id:
            raise NoPermissionException


    def validate_type_of_payment(self, type_of_payment):
        if type_of_payment not in ('T_P', 'M_P', 'H_P'):
            raise InvalidEntityException(source='validator',  code='other_type_of_payment',
                                         message="The type of payment must be only one of T_P, H_P and M_P")


    def validate_task_payment(self, type_of_payment):
        self._validate_project_payment(type_of_payment, 'T_P')

    def validate_month_payment(self, type_of_payment):
        self._validate_project_payment(type_of_payment, 'M_P')

    def validate_hour_payment(self, type_of_payment):
        self._validate_project_payment(type_of_payment, 'H_P')



    def _validate_project_payment(self, type_of_payment,eq_type_of_payment):
        if type_of_payment != eq_type_of_payment:
            raise InvalidEntityException(source='validate', code='other_type_of_payment',
                                         message="The type of payment for the project must be %s" % eq_type_of_payment)




class ProjectDateTimeValidator:
    def date_time_format(self, date_string):
        if date_string is None:
            return None
        try:
            return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ%z")
        except:
            raise InvalidEntityException(source='validator',  code='invalid_format', message="Invalid datetime format")