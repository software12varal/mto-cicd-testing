# from testcase import TestCase
#
# from core import settings
# from super_admin.forms import SuperAdminUpdateProfileForm
# from super_admin.models import SuperAdmin
# from users.models import User
#
#
# class SuperAdminFormTestDbMixin:
#     settings.UNDER_TESTING = True
#     databases = {"vendor_os_db","varal_job_posting_db", }
#
#
# class SuperAdminUpdateProfileFormTest(SuperAdminFormTestDbMixin, TestCase):
#
#     @classmethod
#     def setUp(cls):
#
#         instance = SuperAdmin.objects.create(email='super@gmail.com', is_super_admin=True, is_active=True,
#
#                                              full_name='Super Admin', username='superadmin')
#         instance.set_password('1234')
#         instance.save()
#
#     def test_forms_superAdmin(self):
#         form_data = {'full_name': ' Super Admin', 'contact_number': '+254721212112', 'email': 'super@gmail.com',
#                      'designation': 'Managing Director'}
#
#         form = SuperAdminUpdateProfileForm(data=form_data)
#         # form.save()
#         # print(form)
#         self.assertTrue(form.is_valid())
