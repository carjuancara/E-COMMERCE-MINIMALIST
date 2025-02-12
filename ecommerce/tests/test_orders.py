import pytest
from .test_profile import user, user_profile
from ecommerce.models import Orders
from faker import Faker
import datetime
from decimal import Decimal

faker = Faker()

pytestmark = pytest.mark.django_db

ORDER_STATE = (
    "pending",
    "processing",
    "shipped",
    "delivered",
    "cancelled"
)


def is_type_decimal(value): return isinstance(value, type(Decimal('0')))
def is_type_datetime(value): return isinstance(value, datetime.datetime)
def is_type_string(value): return isinstance(value, str)


@pytest.fixture
def create_order(user, user_profile):
    return Orders.objects.create(
        user=user,
        date_ordered=faker.date_time(),
        total_amount=faker.pydecimal(
            positive=True, left_digits=3, right_digits=2),
        shipping_address=faker.address(),
        status=faker.random_choices(ORDER_STATE, length=1)
    )


def test_create_order(create_order):
    assert Orders.objects.count() == 1


def test_validate_type(create_order):
    order = Orders.objects.first()

    assert is_type_decimal(order.total_amount)
    assert is_type_datetime(order.date_ordered)
    assert is_type_string(order.shipping_address)
    assert is_type_string(order.status)

def test__str__(create_order):
    order = Orders.objects.first()
    print(order._meta.__str__())
    assert is_type_string(order._meta.__str__())
    