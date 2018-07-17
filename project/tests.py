from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from account.models import UserORM
from project.models import ProjectORM, HourPaymentORM, WorkTimeORM, WorkTaskORM, MonthPaymentORM, WorkDayORM
from project.repositories import ProjectRepo, WorkTaskRepo


# -------------------------- Project_Tests ------------------------------------- #

class ProjectMethodTest(TestCase):

    def setUp(self):
        user = UserORM(username="islam", password='sizam123')
        user.save()
        self.user_id = user.id

        self.project = ProjectORM(title="My Firs Project", user=user, type_of_payment='T_P')
        self.project.save()
        self.project_id = self.project.id




# ------------------------ TaskWork_Tests -------------------------------------- #

class WorkTaskMethodTest(TestCase):

    def setUp(self):
        user = UserORM(username="admin", password='qwert12345')
        user.save()
        self.user_id = user.id

        self.project = ProjectORM(title="My Firs Project", user=user, type_of_payment='T_P')
        self.project.save()
        self.project_id = self.project.id


    def test_method_get_total(self):
        for i in range(10):
            worked_task = WorkTaskORM(title='My Task number %s' % i, price=10 * (i + 1), completed=True, project=self.project)
            worked_task.save()

        total = ProjectRepo().get_total(user_id=self.user_id, project_id=self.project_id)

        self.assertEqual(type(total), float)
        self.assertEqual(total, 550)


    def test_method_get_total_paid(self):
        worked_task = WorkTaskORM(title='My Task number %s' % 100, price=100000, completed=True, paid=True, project=self.project)
        worked_task.save()

        total = ProjectRepo().get_total(user_id=self.user_id, project_id=self.project_id)

        self.assertEqual(type(total), int)
        self.assertEqual(total, 0)



# class HourPaymentMethodTest(TestCase):
#     def setUp(self):
#         user = User(username="admin", password='qwert12345')
#         user.save()
#         self.project = ProjectModel(name="My Firs Project", user=user, type_of_payment='H_P')
#         self.project.save()
#         self.hour_pay = HourPaymentModel(project=self.project, rate=10.0, start_rout_date=timezone.now() - timedelta(days=1),
#                                          end_rout_date=timezone.now() + timedelta(days=1))
#         self.hour_pay.save()


#     def test_method_total_type(self):
#         for i in range(10):
#             wt = WorkTime(rate=self.hour_pay, start_work=timezone.now()-timedelta(hours=2),
#                           end_work=timezone.now()-timedelta(hours=1))
#             wt.save()
#         self.assertEqual(type(self.hour_pay.total()), float)
#         self.assertEqual(self.hour_pay.total(), 100.0)



# class MonthPaymentMethodTest(TestCase):
#     def setUp(self):
#         user = User(username="admin", password='qwert12345')
#         user.save()
#         self.project = ProjectModel(name="My Firs Project", user=user, type_of_payment='M_P')
#         self.project.save()
#         self.month_pay = MonthPayment(project=self.project, rate=50.0)
#         self.month_pay.save()


#     def test_method_total_month(self):
#         for i in range(30):
#             workday = WorkDay(month_payment=self.month_pay, day=(timezone.now()-timedelta(days=1)).date(),
#                               have_worked=True)
#             workday.save()

#         self.assertEqual(self.month_pay.total(), 1500)



# class ProjectMethodTest(TestCase):
#     def setUp(self):
#         user = User(username="admin", password='qwert12345')
#         user.save()
#         self.project_task = ProjectModel(name="My Project Task", user=user, type_of_payment='T_P')
#         self.project_task.save()
#         self.project_hour = ProjectModel(name="My Project Hour Payment", user=user, type_of_payment='H_P')
#         self.project_hour.save()
#         self.project_month = ProjectModel(name="My Project Hour Payment", user=user, type_of_payment='M_P')
#         self.project_month.save()




#     def test_method_total_task(self):
#         for i in range(10):
#             hour_pay = TaskPayment(name='My Task number %s' % i, cost=10 * (i + 1), status=True,
#                                    project=self.project_task)
#             hour_pay.save()

#         self.assertEqual(self.project_task.total(), 550)

#     def test_method_total_hour(self):
#         for i in range(2):
#             hour_pay = HourPaymentModel(project=self.project_hour, rate=1.0,
#                                         start_rout_date=timezone.now()-timedelta(days=1),
#                                         end_rout_date=timezone.now() + timedelta(days=1))
#             hour_pay.save()
#             for j in range(10):
#                 wt = WorkTime(rate=hour_pay, start_work=timezone.now() - timedelta(hours=2),
#                               end_work=timezone.now() - timedelta(hours=1))
#                 wt.save()

#         self.assertEqual(type(self.project_hour.total()), float)
#         self.assertEqual(self.project_hour.total(), 20)

#     def test_method_total_month(self):
#         for i in range(10):
#             month_pay = MonthPayment(project=self.project_month, rate=1.0)
#             month_pay.save()

#             for j in range(30):
#                 workday = WorkDay(month_payment=month_pay, day=(timezone.now() - timedelta(days=(i + 1))).date(),
#                                   have_worked=(i % 2 == 0))
#                 workday.save()

#         self.assertEqual(self.project_month.total(), 150)
