class AppException(Exception):
    """Базовое исключение для всех ошибок"""


# ====== Ошибки, связанные с пользователями =====
class InvalidCredentialsError(AppException):
    """Вызывается при логине, если неверный email или пароль"""


class UserAlreadyDeletedError(AppException):
    """Вызывается, если профиль уже находится в процессе удаления или уже удален"""


class PasswordIdenticalToOldError(AppException):
    """Вызывается, если новый пароль совпадает со старым паролем"""


class InvalidPasswordError(AppException):
    """Вызывается при смене пароля, если старый пароль не совпадает"""


class NotAnAdminError(AppException):
    """Вызывается, если у пользователя нет прав администратора"""


class RoleAlreadyAssignedError(AppException):
    """Вызывается, если пользователь получает одинаковую роль"""


class UserAlreadyExistsError(AppException):
    """Вызывается при регистрации, если email уже занят"""


class UserNotFoundError(AppException):
    """Вызывается, если пользователь не найден в БД"""


class TokenExpiredError(Exception):
    """Вызывается, если время действия JWT-токена истекло"""


class InvalidTokenError(Exception):
    """Вызывается, если JWT-токен некорректен"""


# ======= Ошибки, связанные с товарами =====
class InvalidPriceError(AppException):
    """Вызывается при попытке установить отрицательную стоимость товара"""


class OutOfStockError(AppException):
    """Вызывается, если доступного на складе товара меньше, чем запросил пользователь"""


class ProductAlreadyExistsError(AppException):
    """Вызывается, если товар с таким SKU уже зарегистрирован"""


class ProductNotFoundError(AppException):
    """Вызывается, если запрашиваемый товар не существует"""


# ====== Ошибки, связанные с корзиной ====
class CartNotFoundError(AppException):
    """Вызывается, если корзина пользователя не найдена в базе данных"""


class InvalidQuantityError(AppException):
    """Вызывается, если переданное количество товара некорректно"""


class ItemNotInCartError(AppException):
    """Вызывается, если товара нет в корзине при попытке его изменить или удалить"""
