from database.database import get_db
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from services.product_service import ProductService
from services.user_service import UserService


def manual_test():
    with get_db() as db:
        prod_repo = ProductRepository(db)
        user_repo = UserRepository(db)

        prod_serv = ProductService(prod_repo)
        user_serv = UserService(user_repo)

        try:
            print("=== Регистрация пользователей ===")
            d_user = user_serv.registration(1, "Dima", "mirza@gmail.com", "Z123qwe")
            print("-" * 45)
            print(
                f"ID: {d_user.id}",
                f"\nusername: {d_user.username},"
                f"\nemail: {d_user.email},"
                f"\npass_hash: {d_user.password_hash},",
            )
            print("-" * 45)

            m_user = user_serv.registration(2, "Max", "skor@email.ru", "ewq1123")
            print(
                f"ID: {m_user.id}",
                f"\nusername: {m_user.username},"
                f"\nemail: {m_user.email},"
                f"\npass_hash: {m_user.password_hash},",
            )
            print("-" * 45, "\n")
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Проверка дубликата email при регистрации ===")
            X_user = user_serv.registration(3, "Duck", "skor@email.ru", "2aaaa1")
            print(
                f"ID: {X_user.id}",
                f"\nusername: {X_user.username},"
                f"\nemail: {X_user.email},"
                f"\npass_hash: {X_user.password_hash},",
            )
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Cмена пароля ===")
            d_u = user_serv.change_password(1, "Z123qwe", "13qwe1X")
            print(f"Смена пароля успешна. Новый: {d_u.password_hash}", "\n")
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Удаление пользователя ===")
            user_serv.delete_user(2)
            print("Удаление успешно", "\n")
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Повторное удаление пользователя ===")
            user_serv.delete_user(2)
            print("Удаление успешно", "\n")
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Создание продукта ===")
            prod_one = prod_serv.create_product(1, 1001, "Кружка", 800, 70)
            print(f"Создание продукта {prod_one.product_name} успешно", "\n")
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Проверка дубликата SKU ===")
            prod_two = prod_serv.create_product(2, 1001, "Стол", 4000, 15)
            print(f"Создание продукта {prod_two.product_name} успешно", "\n")
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Изменение стоимости ===")
            prod = prod_serv.change_cost(1, 799)
            print(f"Стоимость продукта {prod.product_name} успешно обновлена", "\n")
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Пополнение склада  ===")
            prod = prod_serv.receive_stock(1, 5)
            print(f"Количество продукта {prod.product_name} успешно пополнено", "\n")
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Отгрузка со склада  ===")
            prod = prod_serv.ship_stock(1, 3)
            print(f"Количество продукта {prod.product_name} успешно уменьшено", "\n")
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Проверка остатка продукта на складе + Поиск по ID ===")
            prod = prod_serv.get_product(1)
            print(
                f"Продукт\nID: {prod.id}\nНазвание: {prod.product_name}\nОстаток: {prod.stock_quantity}",
                "\n",
            )
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Отгрузка сверх остатка  ===")
            prod = prod_serv.ship_stock(1, 80)
            print(f"Количество продукта {prod.product_name} успешно уменьшено", "\n")
        except ValueError as e:
            print(f"Ошибка: {e}", "\n")

        try:
            print("=== Поиск по SKU  ===")
            prod = prod_repo.get_by_sku(1001)
            print(
                f"Продукт\nSKU: {prod.sku}\nНазвание: {prod.product_name}\nОстаток: {prod.stock_quantity}",
                "\n",
            )
        except Exception as e:
            print(f"Ошибка: {e}", "\n")


if __name__ == "__main__":
    manual_test()
