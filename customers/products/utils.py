from django.db.models import Q
from django.utils import timezone
from products.models import Product, ProductUnit, PricingGroup
from offers.discounts.models import Offer, OfferCondition
from offers.models import PromotionUsage
from branches.settings.utils import get_branch_settings
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 20  # يمكنك تغيير العدد الافتراضي للصفحة
    page_size_query_param = "page_size"
    max_page_size = 100


def get_available_products(branch):
    """
    جلب المنتجات المتاحة لفروع محددة مع دعم البحث.
    """
    products = ProductUnit.objects.filter(
        branches__branch=branch, branches__quantities__quantity__gt=0
    )

    return products


def get_products(
    request,
    branch=None,
    customer=None,
    city=None,
    country=None,
    region=None,
    sub_region=None,
    browsing_key=None,
    address=None,
    location=None,
    check_offer=True,
):
    """
    جلب المنتجات مع دعم pagination والبحث مع عرض بيانات المنتج الكاملة.
    """

    # جلب المنتجات المتاحة بناءً على الفرع ومعلمات البحث
    products = get_available_products(branch)

    products_with_price = []
    for product in products:
        product_data = get_price_for_product(
            product,
            branch=branch,
            city=city,
            customer=customer,
            country=country,
            region=region,
            sub_region=sub_region,
            browsing_key=browsing_key,
            address=address,
            location=location,
            check_offer=check_offer,
        )
        products_with_price.append(product_data)

    return products_with_price


def get_price_for_product(
    product,
    branch=None,
    customer=None,
    city=None,
    country=None,
    region=None,
    sub_region=None,
    browsing_key=None,
    address=None,
    location=None,
    check_offer=True,
):
    """
    دالة لحساب سعر المنتج وأفضل العروض وإرجاع جميع بيانات المنتج.
    """
    offers = None
    best_offer = None
    final_price = None
    original_price = None

    # جلب مجموعة التسعير الافتراضية
    pricing_group = get_default_pricing_group(branch, browsing_key=browsing_key)

    # التحقق من أن مجموعة التسعير صالحة (ليست None وليست قيمة غير متوقعة)
    if not isinstance(pricing_group, PricingGroup):
        return {"error": "خطأ في مجموعة التسعير. تحقق من إعدادات الفرع."}, None, None

    # جلب السعر بناءً على مجموعة التسعير
    price = product.prices.filter(
        pricing_group=pricing_group.id, unit__is_factor=True
    ).first()

    # التأكد من أسعار الفروع
    if not price:
        branch_prices = product.branches.filter(branch=branch).first()
        if branch_prices:
            price = branch_prices.prices.filter(
                pricing_group=pricing_group.id, unit__is_factor=True
            ).first()

    if not price:
        price = product.prices.filter(pricing_group=pricing_group.id).first()

    # ضبط الأسعار النهائية والأساسية
    if price:
        final_price = price.price
        original_price = getattr(price, "original_price", final_price)
    else:
        # إذا لم يكن هناك سعر، نعيد رسالة توضيحية
        return {"error": "لا يوجد تسعير متاح لهذا المنتج."}, None, None

    # التحقق من العروض المتاحة
    if check_offer and final_price:
        offers = get_available_offers(
            product,
            branch=branch,
            customer=customer,
            city=city,
            country=country,
            region=region,
            sub_region=sub_region,
            browsing_key=browsing_key,
            address=address,
            location=location,
        )

    # تحديد أفضل عرض
    if offers:
        best_offer = select_best_offer(offers, final_price)

    # إذا كان هناك عرض، نخصم قيمته من السعر
    if best_offer and final_price:
        discount_value = calculate_offer_value(best_offer, final_price)
        discounted_price = final_price - discount_value
    else:
        discounted_price = final_price

    # إرجاع السعر الأصلي، السعر النهائي، وأفضل عرض
    return original_price, discounted_price, best_offer


def get_default_pricing_group(branch, browsing_key=None):
    branch_settings = get_branch_settings(branch)
    pricing_group = None

    if "pricing_group" in branch_settings.values():
        try:
            pricing_group = PricingGroup.objects.get(
                id=getattr(branch_settings, "pricing_group")["value"]
            )
        except PricingGroup.DoesNotExist:
            print("No pricing group found for this branch settings.")

    if not pricing_group:
        if hasattr(branch, "zones"):
            zones = branch.zones.filter(pricing_group__isnull=False)
            if hasattr(browsing_key, "zone") and browsing_key.zone in zones:
                pricing_group = browsing_key.zone.pricing_group

            elif zones.exists():
                pricing_group = zones.first().pricing_group

        elif not pricing_group:
            pricing_group = PricingGroup.objects.first()

    return pricing_group


def calculate_offer_value(offer, product_price):
    value = 0

    # 1. خصم بالنسبة المئوية
    if offer.type == Offer.Type.PERCENTAGE:
        for condition in offer.conditions.all():
            if condition.type == OfferCondition.ConditionType.DISCOUNT:
                discount_value = (condition.value / 100) * product_price
                value += discount_value

    # 2. خصم بقيمة نقدية مباشرة
    elif offer.type == Offer.Type.AMOUNT:
        for condition in offer.conditions.all():
            if condition.type == OfferCondition.ConditionType.DISCOUNT:
                value += condition.value

    # 3. المنتجات المجانية
    elif offer.type == Offer.Type.FREE_PRODUCT:
        for condition in offer.conditions.all():
            if condition.type == OfferCondition.ConditionType.FREE_PRODUCT:
                # نضيف القيمة الافتراضية للمنتجات المجانية
                # يمكنك تعديل هذا الجزء لتأخذ قيمة المنتجات المجانية
                free_product_value = sum(
                    [product.price for product in condition.products_get.all()]
                )
                value += free_product_value

    # 4. الكاش باك
    elif offer.type == Offer.Type.CASHBACK:
        for condition in offer.conditions.all():
            if condition.type == OfferCondition.ConditionType.CASHBACK:
                value += condition.value

    return value


def select_best_offer(offers, product_price):
    best_offer = None
    best_value = 0

    for offer in offers:
        # 1. التحقق من تحقيق الحد الأدنى للشراء إن وجد
        if offer.min_purchase_amount and product_price < offer.min_purchase_amount:
            continue

        # 2. حساب قيمة العرض بناءً على نوعه
        offer_value = calculate_offer_value(offer, product_price)

        # 3. إذا كانت قيمة العرض الحالي أفضل من العرض السابق، نقوم بتحديث العرض الأفضل
        if offer_value > best_value:
            best_offer = offer
            best_value = offer_value

    return best_offer


def get_available_offers(
    product,
    branch=None,
    customer=None,
    city=None,
    country=None,
    region=None,
    sub_region=None,
    browsing_key=None,
    address=None,
    location=None,
):
    now = timezone.now()

    # تصفية العروض بناءً على المنتج وتوافره في الوقت الحالي
    offers = Offer.objects.filter(
        Q(conditions__included_products__in=product)
        | Q(conditions__included_groups__products__in=product)
        | Q(conditions__included_categories__products__in=product)
        | Q(conditions__included_brands__products=product)
        | Q(conditions__included_suppliers__products=product)
        | Q(offer_conditions__product_buy__in=product)
        | Q(offer_conditions__groups_buy__products__in=product)
        | Q(offer_conditions__brands_buy__products__in=product)
        | Q(offer_conditions__categories_buy__products__in=product)
        | Q(offer_conditions__packs_buy__products__in=product),
        start_date__lte=now,
        end_date__gte=now,
        is_active=True,
        is_draft=False,
    )

    if customer:

        used_offer_ids = PromotionUsage.objects.filter(customer=customer).values_list(
            "promotion_condition__offer_id", flat=True
        )
        offers = offers.exclude(id__in=used_offer_ids)

    if branch:
        offers = offers.filter(conditions__applicable_branches__in=branch)
    # تصفية بناءً على المدينة
    if city:
        offers = offers.filter(conditions__applicable_cities=city)

    # تصفية بناءً على الدولة
    if country:
        offers = offers.filter(conditions__applicable_countries=country)

    # تصفية بناءً على المنطقة
    if region:
        offers = offers.filter(conditions__applicable_regions=region)

    # تصفية بناءً على المنطقة الفرعية
    if sub_region:
        offers = offers.filter(conditions__applicable_sub_regions=sub_region)

    # تصفية بناءً على مفتاح التصفح
    if browsing_key:
        offers = offers.filter(
            Q(conditions__applicable_branches__in=browsing_key.branch)
            | Q(conditions__applicable_delivery_type=browsing_key.delivery_type)
        )

    # تصفية بناءً على العنوان أو الموقع
    if address or location:
        if address:
            # استخدام العنوان لتحديد المنطقة أو الموقع
            region = address.region
            sub_region = address.sub_region
            offers = offers.filter(
                Q(conditions__applicable_regions=region)
                | Q(conditions__applicable_sub_regions=sub_region)
            )
        elif location:
            # يمكن تطبيق المنطق بناءً على الموقع إذا تم تمرير موقع جغرافي
            # يمكنك استخدام منطق مخصص للتحقق من الموقع هنا
            pass

    return offers.distinct()
