from django.apps import AppConfig



class BranchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'branches'

    def ready(self):
        from activity import registry
        registry.register(
            self.get_model('Branch'),
            self.get_model('BranchServiceZone'),
            self.get_model('DeliveryTimeSlot')
        )
