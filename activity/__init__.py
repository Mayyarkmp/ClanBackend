try:
    from activity.signals import action
except:
    pass

try:
    import django
except:
    pass
else:
    if django.VERSION < (3, 2):
        default_app_config = 'activity.apps.ActivityConfig'


__version__ = '2.0.0'
__author__ = 'Asif Saif Uddin, Justin Quick <justquick@gmail.com>'
