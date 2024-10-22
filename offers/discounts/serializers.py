from .models import Offer, OfferCondition, Coupon, MarketingCoupon
from core.base.serializers import SuperModelSerializer


class OfferSerializer(SuperModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class OfferConditionSerializer(SuperModelSerializer):
    class Meta:
        model = OfferCondition
        fields = "__all__"


class CouponSerializer(SuperModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class MarketingCouponSerializer(SuperModelSerializer):
    class Meta:
        model = MarketingCoupon
        fields = "__all__"
