from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from branches.models import Branch


class CustomerUtils:
    @staticmethod
    def get_browsing_key(request):
        if hasattr(request, "headers"):
            if request.headers.get("Browsing-Key"):
                from customers.models import BrowsingKey

                return BrowsingKey.objects.get(key=request.headers.get("Browsing-Key"))

        return None

    @staticmethod
    def get_session(request):
        if hasattr(request, "COOKIES"):
            if request.COOKIES.get("session_key"):
                from django.contrib.sessions.models import Session

                return Session.objects.get(
                    session_key=request.COOKIES.get("session_key")
                )
            return None

    @staticmethod
    def get_nearest_branch(latitude, longitude):
        """
        دالة لإرجاع أقرب فرع بناءً على الإحداثيات المدخلة.

        Args:
            latitude (float): خط العرض.
            longitude (float): خط الطول.

        Returns:
            Branch: أقرب فرع.
        """
        # إنشاء نقطة جغرافية باستخدام الإحداثيات المدخلة
        user_location = Point(longitude, latitude, srid=4326)

        # جلب أقرب فرع بناءً على المسافة من الموقع المدخل
        nearest_branch = (
            Branch.objects.annotate(distance=Distance("location", user_location))
            .order_by("distance")
            .first()
        )
        if not nearest_branch:
            return Branch.objects.first()

        return nearest_branch

    @staticmethod
    def get_country(branch):
        """
        دالة لجلب الدولة المرتبطة بالفرع.

        Args:
            branch (Branch): كائن الفرع

        Returns:
            Country: الدولة المرتبطة بالفرع.
        """
        if branch and branch.country:
            return branch.country
        return None

    @staticmethod
    def get_region(branch):
        """
        دالة لجلب المنطقة المرتبطة بالفرع.

        Args:
            branch (Branch): كائن الفرع

        Returns:
            Region: المنطقة المرتبطة بالفرع.
        """
        if branch and branch.region:
            return branch.region
        return None

    @staticmethod
    def get_city(branch):
        """
        دالة لجلب المدينة المرتبطة بالفرع.

        Args:
            branch (Branch): كائن الفرع

        Returns:
            City: المدينة المرتبطة بالفرع.
        """
        if branch and branch.city:
            return branch.city
        return None

    @staticmethod
    def create_point(latitude, longitude):
        """
        دالة لإنشاء نقطة جغرافية من خطوط العرض والطول.

        Args:
            latitude (float): خط العرض.
            longitude (float): خط الطول.

        Returns:
            Point: نقطة جغرافية.
        """
        return Point(float(longitude), float(latitude), srid=4326)

    @staticmethod
    def get_user_address(request):
        """
        دالة لجلب عنوان المستخدم من الطلب.

        Args:
            request (Request): كائن الطلب.

        Returns:
            UserAddress: عنوان المستخدم.
        """
        if hasattr(request, "user"):
            if request.user.is_authenticated:
                return request.user.addresses.filter(is_default=True).first()

        browsing_key = CustomerUtils.get_browsing_key(request)
        if browsing_key:
            return browsing_key.address

        return None

    @staticmethod
    def get_user_location(request):
        """
        دالة لجلب موقع المستخدم من الطلب.

        Args:
            request (Request): كائن الطلب.

        Returns:
            Point: موقع المستخدم.
        """
        if hasattr(request, "user"):
            if request.user.is_authenticated:
                return CustomerUtils.get_user_address(request).location

        return None

    @staticmethod
    def get_anonymous_customer(request):
        if hasattr(request, "COOKIES"):
            fingerprint = request.COOKIES.get("fingerprint", None)
            if fingerprint:
                from customers.models import AnonymousCustomer

                try:
                    return AnonymousCustomer.objects.get(fingerprint=fingerprint)
                except AnonymousCustomer.DoesNotExist:
                    return None
        return None
