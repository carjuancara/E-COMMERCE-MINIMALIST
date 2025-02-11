import pytest
from ecommerce.models import Products, Categories
from faker import Faker

faker = Faker()
pytestmark = pytest.mark.django_db

@pytest.fixture
def create_product_valid():
    category =Categories.objects.create(
        name= faker.sentence(nb_words=3)
    )

    return Products.objects.create(    
        category = category,
        name=faker.name(),
        description = faker.sentence(nb_words=5),
        price = faker.pydecimal(positive=True, left_digits=3, right_digits=2),
        discount = faker.pydecimal(positive=True, left_digits=3, right_digits=2),
        stock = faker.random_number(digits=4),
        image =  faker.image_url(),
        created_at = faker.date_time()
    )


def test_create_product(create_product_valid):
    product = Products.objects.first()

    assert type(product.name) is str