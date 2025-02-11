import pytest
from django.contrib.auth.models import User
from ecommerce.models import Profile


@pytest.fixture
def user():
    """Fixture para crear un usuario."""
    return User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123'
    )

@pytest.fixture
def user_profile(user):
    """Fixture para crear un perfil de usuario asociado al usuario."""
    return Profile.objects.create(
        user=user,
        address='Calle Falsa 123',
        phone='+573001234567'  # Número de teléfono válido
    )


@pytest.mark.django_db
def test_user_profile_creation(user_profile, user):
    """Prueba que el perfil se crea correctamente."""
    assert user_profile.user == user
    assert user_profile.address == 'Calle Falsa 123'
    assert str(user_profile.phone) == '+573001234567'


@pytest.mark.django_db
def test_user_profile_str_representation(user_profile, user):
    """Prueba la representación en cadena del perfil."""
    expected_str = f"Perfil de {user.username}"
    assert str(user_profile) == expected_str


@pytest.mark.django_db
def test_user_profile_on_delete_cascade():
    user = User.objects.create_user(username='testuser', password='password') # Guarda el usuario!
    profile = Profile.objects.create(user=user, address="test", phone="123")
    user.delete()
    assert not Profile.objects.filter(pk=profile.pk).exists()


@pytest.mark.django_db

def test_user_profile_unique_constraint(db, user):
    """Prueba que no se puede crear más de un perfil para el mismo usuario."""
    Profile.objects.create(user=user, address='Calle Falsa 123')
    with pytest.raises(Exception):  # Puede ser IntegrityError
        Profile.objects.create(user=user, address='Otra dirección')


@pytest.mark.django_db
def test_address_field_blank_and_null():
    user = User.objects.create_user(username='testuser', password='password')
    profile = Profile.objects.create(user=user) # Crea el perfil *después* de crear el usuario
    assert profile.address == None

@pytest.mark.django_db
def test_phone_field_blank_and_null():
    user = User.objects.create_user(username='testuser', password='password')
    profile = Profile.objects.create(user=user) # Crea el perfil *después* de crear el usuario
    assert profile.phone == None