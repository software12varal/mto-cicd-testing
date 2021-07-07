class VendorOSRouter:
    """
    A router to control all database operations on models in the
    auth and accounts applications. This is related to vendorOS DB.
    """
    route_app_labels = {'users', 'auth',
                        'contenttypes', 'sessions', 'admin', 'mto'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'vendor_os_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'vendor_os_db'
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
            return db == 'vendor_os_db'
        return None


class VaralJobPostingDBRouter:
    """
    A router to control all database operations on models in the
    jobs and payments applications. This is related to VaralJobPostingDB.
    """
    route_app_labels = {'users', 'auth',
                        'contenttypes', 'sessions', 'admin', 'jobs'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'varal_job_posting_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'varal_job_posting_db'
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
        return None
