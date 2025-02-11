import pytest
from ecommerce.models import Categories

pytestmark = pytest.mark.django_db

@pytest.fixture
def create_category_save_slug():
    return Categories.objects.create(
        name='category with plus'
    )

@pytest.fixture
def create_category():
    return Categories.objects.create(
        name='category 1',
        slug='category-1'
    )

def test_create_category(create_category):
    category = Categories.objects.first()

    assert len(category.name) == 10
    assert category.slug == "category-1"

def test_verbose_name_plural(create_category):
    category = Categories.objects.first()

    assert category._meta.verbose_name_plural=="Categories"

def test_slug_save(create_category_save_slug):
    category = Categories.objects.first()
    category.save()

    assert category.slug == 'category-with-plus'

def test_str_title(create_category):
    category = Categories.objects.first()

    assert category.__str__() == "category 1".title()

