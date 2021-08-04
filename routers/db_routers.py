from django.conf import settings


# route_rw is the route for read and write.

class VendorOSRouter:
    """
    A router to control all database operations on models in the
    auth and accounts applications. This is related to vendorOS DB.
    """
    route_app_labels = {'mto'}
    route_rw = {'users', 'auth', 'contenttypes', 'sessions', 'admin', 'mto'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_rw:
            return 'vendor_os_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_rw:
            return 'vendor_os_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in self.route_rw or
                obj2._meta.app_label in self.route_rw
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            if settings.UNDER_TESTING:
                return True
            else:
                return db == 'vendor_os_db'
        return None


class VaralJobPostingDBRouter:
    """
    A router to control all database operations on models in the
    jobs and payments applications. This is related to VaralJobPostingDB.
    """
    route_app_labels = {'jobs', 'super_admin'}
    route_rw = {'users', 'auth', 'contenttypes', 'sessions', 'admin', 'jobs', 'super_admin'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_rw:
            return 'varal_job_posting_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_rw:
            return 'varal_job_posting_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in self.route_rw or
                obj2._meta.app_label in self.route_rw
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            if settings.UNDER_TESTING:
                return True
            else:
                return db == 'varal_job_posting_db'
        return None


class AccountsDBRouter:
    """
    A router to control all database operations on models in the
    payments and accounts applications. This is related to Accounts DB.
    """
    route_app_labels = {'accounts'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'accounts_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'accounts_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label in self.route_app_labels:
            return db == 'accounts_db'
        elif db == 'accounts_db':
            if settings.UNDER_TESTING:
                return None
            else:
                return False
        return None
