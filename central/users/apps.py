from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'central.users'
    verbose_name = 'Users'
    label = 'central_users'

    def ready(self):
        from activity import registry
        registry.register(
            self.get_model('CentralUser'),
            self.get_model('Grade'),
            self.get_model('AssignedBranches'),
            self.get_model('WorkPeriod')
        )
