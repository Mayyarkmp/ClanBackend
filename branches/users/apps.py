from django.apps import AppConfig


class BranchUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'branches.users'
    label = 'branches_users'

    def ready(self):
        from activity import registry

        registry.register(
            self.get_model('BranchUser'),
            self.get_model('Zone'),
            self.get_model('Preparer'),
            self.get_model('Staff'),
            self.get_model('Manager'),
            self.get_model('Delivery'),
            self.get_model('WorkPeriod'),
            self.get_model('Zone'),
            self.get_model('WorkPeriod')
        )

