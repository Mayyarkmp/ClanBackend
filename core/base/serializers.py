from rest_framework import serializers
from djmoney.models.fields import MoneyField
from rest_framework.relations import PrimaryKeyRelatedField

from .fileds import MoneyField as CustomMoneyField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework.serializers import HyperlinkedModelSerializer


from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField


class RelatedFieldsMixin(serializers.ModelSerializer):
    """
    Mixin لتحويل الحقول المرتبطة إلى كائنات مفصلة بدلاً من معرفات.
    يدعم ForeignKey، ManyToManyField، و OneToOneField.
    يتجاوز الحقول المعرفة يدويًا في الـ Serializer.
    """

    def set_fields_representation(self, related_obj):
        obj = {}

        # تحديد الحقول بناءً على السمات المتاحة في الكائن المرتبط
        if hasattr(related_obj, "name") and related_obj.name:
            obj["name"] = related_obj.name
            obj["name_en"] = getattr(related_obj, "name_en", "")
        elif hasattr(related_obj, "title") and related_obj.title:
            obj["title"] = related_obj.title
            obj["title_en"] = getattr(related_obj, "title_en", "")
        elif hasattr(related_obj, "email") and related_obj.email:
            obj["email"] = related_obj.email
            if (
                hasattr(related_obj, "first_name")
                and hasattr(related_obj, "last_name")
                and related_obj.first_name
                and related_obj.last_name
            ):
                obj["full_name"] = f"{related_obj.first_name} {related_obj.last_name}"
            else:
                obj["username"] = getattr(related_obj, "username", "")

        elif hasattr(related_obj, "file"):
            obj["url"] = getattr(related_obj, "file").url
        else:
            obj["id"] = related_obj.id
            obj["uid"] = getattr(related_obj, "uid", None)

        # تضمين 'id' دائمًا إذا كان متاحًا
        if "id" not in obj and hasattr(related_obj, "id"):
            obj["id"] = related_obj.id

        return obj

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        model = instance.__class__

        serializer_fields = set(self.fields.keys())
        model_field_names = set(f.name for f in model._meta.get_fields())
        custom_fields = serializer_fields - model_field_names
        source_to_serializer = {}
        for field_name in serializer_fields:
            field = self.fields[field_name]
            if isinstance(field, PrimaryKeyRelatedField) and field.source:
                source_to_serializer[field.source] = field_name

        for field in model._meta.get_fields():
            if not isinstance(field, (ForeignKey, OneToOneField, ManyToManyField)):
                continue

            field_name = field.name

            serializer_field_name = source_to_serializer.get(field_name, field_name)

            if serializer_field_name in custom_fields:
                continue

            if serializer_field_name not in self.fields:
                continue

            if not isinstance(
                self.fields[serializer_field_name], serializers.PrimaryKeyRelatedField
            ) and not isinstance(
                self.fields[serializer_field_name], serializers.ManyRelatedField
            ):
                continue

            if isinstance(field, (ForeignKey, OneToOneField)):
                related_obj = getattr(instance, field_name, None)
                if related_obj is not None:
                    representation[serializer_field_name] = (
                        self.set_fields_representation(related_obj)
                    )
                else:
                    representation[serializer_field_name] = None
            elif isinstance(field, ManyToManyField):
                related_qs = getattr(instance, field_name).all()
                representation[serializer_field_name] = [
                    self.set_fields_representation(obj) for obj in related_qs
                ]

        return representation


class DynamicFieldsSerializerMixin:
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
        self.fields.pop("deleted_at", None)
        self.fields.pop("is_deleted", None)

        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class MoneyFieldSerializerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, MoneyField):
                self.fields[field_name] = CustomMoneyField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name in representation.keys():
            if isinstance(self.fields[field_name], CustomMoneyField):
                money_value = getattr(instance, field_name)
                representation[field_name] = CustomMoneyField().to_representation(
                    money_value
                )
        return representation

    def to_internal_value(self, data):
        for field_name, field in self.fields.items():
            if isinstance(field, CustomMoneyField):
                if field_name in data:
                    money_data = data[field_name]
                    data[field_name] = CustomMoneyField().to_internal_value(money_data)
        return super().to_internal_value(data)


class SuperSerializer(
    DynamicFieldsSerializerMixin, RelatedFieldsMixin, serializers.Serializer
):
    pass


class SuperModelSerializer(
    DynamicFieldsSerializerMixin, RelatedFieldsMixin, serializers.ModelSerializer
):
    pass


class SuperHyperlinkedModelSerializer(
    DynamicFieldsSerializerMixin, RelatedFieldsMixin, HyperlinkedModelSerializer
):
    pass


class SuperNestedHyperlinkedModelSerializer(
    DynamicFieldsSerializerMixin, RelatedFieldsMixin, NestedHyperlinkedModelSerializer
):
    pass


"""
['Meta', '__class__', '__class_getitem__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_args', '_context', '_creation_counter', '_declared_fields', '_get_model_fields', '_kwargs', '_pop_translated_data', '_read_only_defaults', '_readable_fields', '_writable_fields', 'allow_null', 'bind', 'build_field', 'build_nested_field', 'build_property_field', 'build_relational_field', 'build_standard_field', 'build_unknown_field', 'build_url_field', 'context', 'create', 'data', 'default', 'default_empty_html', 'default_error_messages', 'default_validators', 'error_messages', 'errors', 'fail', 'field_name', 'fields', 'get_attribute', 'get_default', 'get_default_field_names', 'get_extra_kwargs', 'get_field_names', 'get_fields', 'get_initial', 'get_translatable_fields', 'get_translated_field', 'get_unique_for_date_validators', 'get_unique_together_constraints', 'get_unique_together_validators', 'get_uniqueness_extra_kwargs', 'get_validators', 'get_value', 'help_text', 'include_extra_kwargs', 'initial', 'initial_data', 'instance', 'is_valid', 'label', 'language', 'many_init', 'parent', 'partial', 'read_only', 'required', 'root', 'run_validation', 'run_validators', 'save', 'save_translations', 'serializer_choice_field', 'serializer_field_mapping', 'serializer_related_field', 'serializer_related_to_field', 'serializer_url_field', 'set_value', 'source', 'style', 'to_internal_value', 'to_representation', 'update', 'url_field_name', 'validate', 'validate_empty_values', 'validated_data', 'validators', 'write_only']

"""
