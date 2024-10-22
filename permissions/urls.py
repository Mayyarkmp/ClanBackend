from rest_framework_nested import routers
from permissions import views

app_name = 'permissions'

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'permissions', views.PermissionViewSet)
group_router = routers.NestedSimpleRouter(router, r'groups', lookup='group')
group_router.register(r'permissions', views.PermissionViewSet, basename='group-permissions')

urlpatterns = []
urlpatterns += router.urls + group_router.urls
