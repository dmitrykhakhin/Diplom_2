class Url:
    URL = 'https://stellarburgers.nomoreparties.site'
    REGISTER_USER_HANDLE = '/api/auth/register'
    AUTHORIZATION_USER_HANDLE = '/api/auth/user'
    LOGIN_USER_HANDLE = '/api/auth/login'
    ORDERS_HANDLE = '/api/orders'


class Message:
    USER_ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INCORRECT_DATA = "email or password are incorrect"
    SHOULD_AUTHORISED = "You should be authorised"
    INGREDIENTS_MUST_PROVIDED = "Ingredient ids must be provided"


class Ingredients:
    FLUORESCENT_BUN = "61c0c5a71d1f82001bdaaa6d"
    KRATOR_BUN = "61c0c5a71d1f82001bdaaa6c"
    IMMORTAL_PROTOSTOMIA_MEAT = "61c0c5a71d1f82001bdaaa6f"
    BEEF_METEORITE = "61c0c5a71d1f82001bdaaa70"
    SPACE_SAUCE = "61c0c5a71d1f82001bdaaa73"
    TRADITIONAL_GALACTIC_SAUCE = "61c0c5a71d1f82001bdaaa74"
