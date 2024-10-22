from products.models import (
    Group,
    Category,
    Brand,
    Supplier,
    Product,
    ProductCost,
    ProductPrice,
    Unit,
    PricingGroup,
    Barcode,
)

import pytest
from core.media.models import Media


@pytest.mark.django_db
def test_group_creation():
    """Test creation of a Group instance"""
    # إنشاء كائن Group بدون Parent أو صور
    group = Group.objects.create(
        number="12345",
        name="Electronics",
        name_en="Electronics EN",
        profit_margin=10,
        default_image="default.jpg",
    )

    # التحقق من أن الكائن تم إنشاؤه
    assert group is not None
    assert group.number == "12345"
    assert group.name == "Electronics"
    assert group.name_en == "Electronics EN"
    assert group.profit_margin == 10
    assert group.default_image == "default.jpg"
    assert group.parent is None
    assert group.images.count() == 0


@pytest.mark.django_db
def test_group_with_parent():
    """Test Group creation with a parent group"""
    parent_group = Group.objects.create(
        number="54321",
        name="Main Group",
        profit_margin=15,
    )

    child_group = Group.objects.create(
        number="67890",
        name="Sub Group",
        parent=parent_group,
        profit_margin=5,
    )

    # التحقق من أن المجموعة الرئيسية موجودة
    assert child_group.parent == parent_group
    assert child_group.name == "Sub Group"
    assert parent_group.children.count() == 1
    assert parent_group.children.first() == child_group


@pytest.mark.django_db
def test_group_str_method():
    """Test the __str__ method of the Group model"""
    group = Group.objects.create(
        number="11111",
        name="Fashion",
        profit_margin=20,
    )

    # التأكد من أن __str__ ترجع اسم المجموعة
    assert str(group) == "Fashion"
