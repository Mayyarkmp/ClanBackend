from django.db.models import Sum
from django.utils import timezone

from offers.models import PromotionUsage, PromotionCondition, PromotionAnalytics


def check_promotion_conditions(promotion, customer, cart_total, cart_items, branch, region, payment_service, delivery_type, platform):
    condition = promotion.get_conditions()
    if not condition:
        return True  # لا توجد شروط، العرض قابل للتطبيق

    now = timezone.now()

    # التحقق من تاريخ البدء والانتهاء
    if condition.start_date and now < condition.start_date:
        return False
    if condition.end_date and now > condition.end_date:
        return False

    # التحقق من الفترات الزمنية (PromotionTimeSlot)
    if condition.time_slots.exists():
        time_slot_matched = False
        for slot in condition.time_slots.all():
            if slot.day == now.date():
                if slot.start_time <= now.time() <= slot.end_time:
                    time_slot_matched = True
                    break
        if not time_slot_matched:
            return False  # الوقت الحالي لا يطابق أي فترة زمنية محددة

    # التحقق من الحد الأدنى لإجمالي السلة
    if condition.min_cart_total and cart_total < condition.min_cart_total.amount:
        return False

    # التحقق من المنصات المطبقة
    if condition.applicable_platforms != PromotionCondition.Platform.BOTH:
        if platform != condition.applicable_platforms:
            return False

    # التحقق من طرق التوصيل المطبقة
    if condition.applicable_delivery_types != PromotionCondition.DeliveryType.BOTH:
        if delivery_type != condition.applicable_delivery_types:
            return False

    # التحقق من الدول والمناطق والفروع المطبقة
    if condition.applicable_countries.exists():
        if customer.country not in condition.applicable_countries.all():
            return False
    if condition.applicable_regions.exists():
        if region not in condition.applicable_regions.all():
            return False
    if condition.applicable_sub_regions.exists():
        if customer.sub_region not in condition.applicable_sub_regions.all():
            return False
    if condition.applicable_cities.exists():
        if customer.city not in condition.applicable_cities.all():
            return False
    if condition.applicable_branches.exists():
        if branch not in condition.applicable_branches.all():
            return False

    # التحقق من خدمات الدفع المطبقة
    if condition.included_payment_services.exists():
        if payment_service not in condition.included_payment_services.all():
            return False
    if condition.excluded_payment_services.exists():
        if payment_service in condition.excluded_payment_services.all():
            return False

    # التحقق من الحد الأقصى لعدد الاستخدامات لكل عميل
    if condition.max_uses_per_customer:
        usage_count = PromotionUsage.objects.filter(
            promotion_condition=condition,
            customer=customer
        ).count()
        if usage_count >= condition.max_uses_per_customer:
            return False

    # التحقق من الحدود الإجمالية للعملاء
    if condition.max_total_customers is not None:
        total_customers_used = PromotionUsage.objects.filter(
            promotion_condition=condition
        ).values('customer').distinct().count()
        if total_customers_used >= condition.max_total_customers:
            return False

    # التحقق من الحدود المخصصة للفرع (عدد العملاء)
    if branch:
        branch_limit = condition.branch_limits.filter(branch=branch).first()
        if branch_limit and branch_limit.max_customers is not None:
            branch_customers_used = PromotionUsage.objects.filter(
                promotion_condition=condition,
                branch=branch
            ).values('customer').distinct().count()
            if branch_customers_used >= branch_limit.max_customers:
                return False

    # التحقق من الحدود المخصصة للمنطقة (عدد العملاء)
    if region:
        region_limit = condition.region_limits.filter(region=region).first()
        if region_limit and region_limit.max_customers is not None:
            region_customers_used = PromotionUsage.objects.filter(
                promotion_condition=condition,
                region=region
            ).values('customer').distinct().count()
            if region_customers_used >= region_limit.max_customers:
                return False

    # حساب إجمالي الكمية للمنتجات المشمولة في العرض داخل السلة
    total_quantity_in_cart = cart_items_quantity(cart_items, condition)

    # التحقق من الحدود الإجمالية للكمية
    if condition.max_total_quantity is not None:
        total_quantity_used = PromotionUsage.objects.filter(
            promotion_condition=condition
        ).aggregate(total=Sum('quantity'))['total'] or 0
        if total_quantity_used + total_quantity_in_cart > condition.max_total_quantity:
            return False

    # التحقق من الحدود المخصصة للفرع (الكمية)
    if branch:
        branch_limit = condition.branch_limits.filter(branch=branch).first()
        if branch_limit and branch_limit.max_quantity is not None:
            branch_quantity_used = PromotionUsage.objects.filter(
                promotion_condition=condition,
                branch=branch
            ).aggregate(total=Sum('quantity'))['total'] or 0
            if branch_quantity_used + total_quantity_in_cart > branch_limit.max_quantity:
                return False

    # التحقق من الحدود المخصصة للمنطقة (الكمية)
    if region:
        region_limit = condition.region_limits.filter(region=region).first()
        if region_limit and region_limit.max_quantity is not None:
            region_quantity_used = PromotionUsage.objects.filter(
                promotion_condition=condition,
                region=region
            ).aggregate(total=Sum('quantity'))['total'] or 0
            if region_quantity_used + total_quantity_in_cart > region_limit.max_quantity:
                return False

    # التحقق من المنتجات والمجموعات والتصنيفات والموردين المشمولين والمستبعدين
    if not is_cart_eligible_for_promotion(cart_items, condition):
        return False

    # جميع الشروط متحققة
    return True



def cart_items_quantity(cart_items, promotion_condition):
    total_quantity = 0
    for item in cart_items:
        product = item.product
        if is_product_in_promotion(product, promotion_condition):
            total_quantity += item.quantity
    return total_quantity



def is_product_in_promotion(product, promotion_condition):
    # التحقق من المنتجات المشمولة والمستثناة
    if promotion_condition.included_products.exists():
        if product not in promotion_condition.included_products.all():
            return False
    if promotion_condition.excluded_products.exists():
        if product in promotion_condition.excluded_products.all():
            return False

    # التحقق من المجموعات المشمولة والمستثناة
    if promotion_condition.included_groups.exists():
        if product.group not in promotion_condition.included_groups.all():
            return False
    if promotion_condition.excluded_groups.exists():
        if product.group in promotion_condition.excluded_groups.all():
            return False

    # التحقق من التصنيفات المشمولة والمستثناة
    if promotion_condition.included_categories.exists():
        if not product.categories.filter(id__in=promotion_condition.included_categories.all()).exists():
            return False
    if promotion_condition.excluded_categories.exists():
        if product.categories.filter(id__in=promotion_condition.excluded_categories.all()).exists():
            return False

    # التحقق من الموردين المشمولين والمستثنين
    if promotion_condition.included_suppliers.exists():
        if product.supplier not in promotion_condition.included_suppliers.all():
            return False
    if promotion_condition.excluded_suppliers.exists():
        if product.supplier in promotion_condition.excluded_suppliers.all():
            return False

    # إذا اجتاز جميع التحقق، فالمنتج مشمول في العرض
    return True

def record_promotion_usage(promotion_condition, customer, branch, region, cart_items):
    quantity = cart_items_quantity(cart_items, promotion_condition)
    PromotionUsage.objects.create(
        promotion_condition=promotion_condition,
        customer=customer,
        branch=branch,
        region=region,
        quantity=quantity,
    )


def is_product_in_promotion(product, promotion_condition):
    # التحقق من المنتجات المستبعدة
    if promotion_condition.excluded_products.exists():
        if product in promotion_condition.excluded_products.all():
            return False

    # التحقق من المنتجات المشمولة
    if promotion_condition.included_products.exists():
        if product not in promotion_condition.included_products.all():
            return False

    # التحقق من المجموعات المستبعدة
    if promotion_condition.excluded_groups.exists():
        if product.group in promotion_condition.excluded_groups.all():
            return False

    # التحقق من المجموعات المشمولة
    if promotion_condition.included_groups.exists():
        if product.group not in promotion_condition.included_groups.all():
            return False

    # التحقق من التصنيفات المستبعدة
    if promotion_condition.excluded_categories.exists():
        if product.categories.filter(id__in=promotion_condition.excluded_categories.values_list('id', flat=True)).exists():
            return False

    # التحقق من التصنيفات المشمولة
    if promotion_condition.included_categories.exists():
        if not product.categories.filter(id__in=promotion_condition.included_categories.values_list('id', flat=True)).exists():
            return False

    # التحقق من الموردين المستبعدين
    if promotion_condition.excluded_suppliers.exists():
        if product.supplier in promotion_condition.excluded_suppliers.all():
            return False

    # التحقق من الموردين المشمولين
    if promotion_condition.included_suppliers.exists():
        if product.supplier not in promotion_condition.included_suppliers.all():
            return False

    return True


def is_cart_eligible_for_promotion(cart_items, promotion_condition):
    eligible = False
    for item in cart_items:
        if is_product_in_promotion(item.product, promotion_condition):
            eligible = True
        else:
            return False  # إذا كان هناك منتج غير مشمول، نرجع False
    return eligible



def log_impression(promotion=None, advertisement=None, customer=None, branch=None, region=None, platform=None, device=None, request=None):
    PromotionAnalytics.objects.create(
        promotion=promotion,
        advertisement=advertisement,
        event_type=PromotionAnalytics.EventType.IMPRESSION,
        customer=customer,
        branch=branch,
        region=region,
        platform=platform,
        device=device,
        session_id=request.session.session_key if request else None,
        ip_address=get_client_ip(request) if request else None,
        user_agent=request.META.get('HTTP_USER_AGENT') if request else None,
    )


def log_click(promotion=None, advertisement=None, customer=None, branch=None, region=None, platform=None, device=None, request=None):
    PromotionAnalytics.objects.create(
        promotion=promotion,
        advertisement=advertisement,
        event_type=PromotionAnalytics.EventType.CLICK,
        customer=customer,
        branch=branch,
        region=region,
        platform=platform,
        device=device,
        session_id=request.session.session_key if request else None,
        ip_address=get_client_ip(request) if request else None,
        user_agent=request.META.get('HTTP_USER_AGENT') if request else None,
    )


def log_order(promotion=None, advertisement=None, customer=None, branch=None, region=None, platform=None, device=None, request=None):
    PromotionAnalytics.objects.create(
        promotion=promotion,
        advertisement=advertisement,
        event_type=PromotionAnalytics.EventType.ORDER,
        customer=customer,
        branch=branch,
        region=region,
        platform=platform,
        device=device,
        session_id=request.session.session_key if request else None,
        ip_address=get_client_ip(request) if request else None,
        user_agent=request.META.get('HTTP_USER_AGENT') if request else None,
    )


def log_purchase(promotion=None, advertisement=None, customer=None, branch=None, region=None, platform=None, device=None, request=None):
    PromotionAnalytics.objects.create(
        promotion=promotion,
        advertisement=advertisement,
        event_type=PromotionAnalytics.EventType.PURCHASE,
        customer=customer,
        branch=branch,
        region=region,
        platform=platform,
        device=device,
        session_id=request.session.session_key if request else None,
        ip_address=get_client_ip(request) if request else None,
        user_agent=request.META.get('HTTP_USER_AGENT') if request else None,
    )


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

