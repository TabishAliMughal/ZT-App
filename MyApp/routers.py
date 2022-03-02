class AppRouter:
    route_app_labels = {'admin','auth','Authentication','Main','Creator','social_django','contenttypes','sessions','messages','staticfiles','storages'}
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'app'
        return None
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'app'
        return None
    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels):
           return True
        return None
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'app'
        return None

class BlogRouter:
    route_app_labels = {'Blog', 'Bunch', 'Post','Tags'}
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'blog'
        return None
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'blog'
        return None
    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels):
           return True
        return None
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'blog'
        return None
        
class MatronomialRouter:
    route_app_labels = {'Info', 'Matching', 'Candidate'}
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'matrinomial'
        return None
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'matrinomial'
        return None
    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels):
           return True
        return None
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'matrinomial'
        return None

class ShopRouter:
    route_app_labels = {'Accounts', 'Cart', 'Customer', 'Delivery', 'Orders', 'Shop'}
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'shop'
        return None
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'shop'
        return None
    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels):
           return True
        return None
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'shop'
        return None

class SchoolRouter:
    route_app_labels = {'Admin','Checker','Content','Exam','Indivisuals','RegSchool','Requirments','Result','Teacher','Visitors'}
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'school'
        return None
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'school'
        return None
    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels):
           return True
        return None
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'school'
        return None


