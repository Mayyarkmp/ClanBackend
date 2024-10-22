from decimal import Decimal
from typing import Dict, Literal, Optional, Union

from moneyed import (
    Currency,
    CurrencyDoesNotExist,
    Money,
    get_currency,
)
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, Field, IntegerField
from rest_framework.serializers import Serializer


MoneyRepresentation = Dict[Literal["amount", "currency"], Union[int, str]]


class MoneySerializer(Serializer):
    amount = IntegerField()
    currency = CharField()

    def validate_currency(self, value: str) -> Currency:
        try:
            return get_currency(code=value)
        except CurrencyDoesNotExist as e:
            raise ValidationError(str(e))


class MoneyField(Field):
    def to_internal_value(
        self, data: Optional[Union[Money, MoneyRepresentation]]
    ) -> Optional[Money]:
        if data is None:
            return None

        if isinstance(data, Money):
            return data

        serializer = MoneySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        currency = validated_data["currency"]
        amount = Decimal(validated_data["amount"]) / currency.sub_unit

        return Money(amount=amount, currency=currency)

    def to_representation(
        self, value: Optional[Money]
    ) -> Optional[MoneyRepresentation]:
        if value is None:
            return None

        currency = value.currency
        amount = round(value.amount * currency.sub_unit)

        return {
            "amount": amount,
            "currency": currency.code,
        }



