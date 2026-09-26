# Лабораторна робота №2. Створення та використання функцій, реалізація рекурсії
# Варіант: 6
# ПІБ: Довгай Владислав Володимирович

from functools import lru_cache, reduce
from typing import Callable, Dict, List, Tuple


# -------------------
# 1. Звичайні функції
# -------------------


def monthly_loan_payment(principal: float, annual_rate: float, months: int) -> float:
    """Розраховує щомісячний платіж за кредитом.

    Args:
        principal (float): Сума кредиту.
        annual_rate (float): Річна відсоткова ставка у відсотках.
        months (int): Термін кредиту в місяцях.

    Returns:
        float: Розмір щомісячного платежу.
    """
    if principal <= 0 or months <= 0 or annual_rate < 0:
        raise ValueError("Сума й термін мають бути додатними, ставка — невід'ємною.")
    r = annual_rate / 100 / 12
    if r == 0:
        return principal / months
    return principal * r / (1 - (1 + r) ** -months)


def calculate_budget_balance(income: float, expenses: float) -> Tuple[float, float]:
    """Повертає баланс бюджету та норму заощаджень (%).

    Args:
        income (float): Дохід за період.
        expenses (float): Витрати за період.

    Returns:
        Tuple[float, float]: (баланс, відсоток заощаджень від доходу).
    """
    if income <= 0:
        raise ValueError("Дохід має бути більшим за нуль.")
    balance = income - expenses
    return balance, balance / income * 100


# -----------------------------------------
# 2. Функція з параметрами за замовчуванням
# -----------------------------------------


def compound_interest(principal: float, annual_rate: float, years: float,
                      periods_per_year: int = 12) -> float:
    """Розраховує підсумкову суму вкладу зі складним відсотком.

    Args:
        principal (float): Початкова сума вкладу.
        annual_rate (float): Річна ставка у відсотках.
        years (float): Термін вкладу в роках.
        periods_per_year (int, optional): Кількість капіталізацій на рік.
            За замовчуванням 12 (щомісяця).

    Returns:
        float: Сума на кінець терміну.
    """
    if principal < 0 or annual_rate < 0 or years < 0 or periods_per_year <= 0:
        raise ValueError("Некоректні параметри вкладу.")
    n = periods_per_year
    return principal * (1 + annual_rate / 100 / n) ** (n * years)


# ------------------------------------------
# 3. Функція зі змінною кількістю аргументів
# ------------------------------------------


def average_expense(*expenses: float) -> float:
    """Обчислює середню витрату з довільної кількості значень.

    Args:
        *expenses (float): Довільна кількість сум витрат.

    Returns:
        float: Середня витрата (0, якщо значень немає).
    """
    if not expenses:
        return 0.0
    return sum(expenses) / len(expenses)


# ---------------------------------------------------------------------------
# 4. Лямбда-функції
# ---------------------------------------------------------------------------

# Сума з ПДВ (за замовчуванням 20%)
price_with_vat = lambda price, vat=20: price * (1 + vat / 100)
# Зміна ціни/суми у відсотках
percent_change = lambda old, new: (new - old) / old * 100


# --------------------------------------------------------------------
# 5. Рекурсивна функція: оптимальний набір покупок (задача про рюкзак)
# --------------------------------------------------------------------


def best_purchases(items: List[Dict], budget: int) -> Tuple[int, List[str]]:
    """Рекурсивно підбирає набір покупок з максимальною сумарною
    пріоритетністю, не перевищуючи бюджет (задача про рюкзак).

    Для ефективності проміжні результати кешуються (lru_cache), тому
    кількість викликів обмежена кількістю пар (індекс, залишок бюджету).

    Args:
        items (List[Dict]): Список товарів: {'name', 'price' (int), 'value' (int)}.
        budget (int): Доступний бюджет.

    Returns:
        Tuple[int, List[str]]: (сумарна пріоритетність, назви обраних товарів).
    """

    @lru_cache(maxsize=None)
    def solve(index: int, left: int) -> Tuple[int, Tuple[str, ...]]:
        # Базовий випадок: товари закінчились або бюджет вичерпано
        if index == len(items) or left <= 0:
            return 0, ()
        item = items[index]
        # Рекурсивний випадок 1: пропускаємо товар
        skip_value, skip_names = solve(index + 1, left)
        # Рекурсивний випадок 2: беремо товар (якщо вистачає грошей)
        if item["price"] <= left:
            take_value, take_names = solve(index + 1, left - item["price"])
            take_value += item["value"]
            if take_value > skip_value:
                return take_value, (item["name"],) + take_names
        return skip_value, skip_names

    value, names = solve(0, budget)
    return value, list(names)


# -------------------------------------------------
# 6. Функція вищого порядку + map / filter / reduce
# -------------------------------------------------


def apply_to_amounts(data: List[Dict], func: Callable[[float], float]) -> List[Dict]:
    """Функція вищого порядку: застосовує func до поля 'amount' кожної операції.

    Args:
        data (List[Dict]): Список операцій.
        func (Callable[[float], float]): Функція перетворення суми.

    Returns:
        List[Dict]: Новий список операцій з оновленими сумами.
    """
    return [{**item, "amount": func(item["amount"])} for item in data]


# Набір даних: 20 витрат за місяць
TRANSACTIONS: List[Dict] = [
    {"date": "2024-05-01", "category": "Оренда", "amount": 9000.0},
    {"date": "2024-05-01", "category": "Продукти", "amount": 850.0},
    {"date": "2024-05-02", "category": "Транспорт", "amount": 120.0},
    {"date": "2024-05-03", "category": "Розваги", "amount": 450.0},
    {"date": "2024-05-04", "category": "Продукти", "amount": 620.0},
    {"date": "2024-05-05", "category": "Комунальні", "amount": 1800.0},
    {"date": "2024-05-06", "category": "Транспорт", "amount": 95.0},
    {"date": "2024-05-07", "category": "Здоров'я", "amount": 700.0},
    {"date": "2024-05-08", "category": "Продукти", "amount": 540.0},
    {"date": "2024-05-09", "category": "Розваги", "amount": 300.0},
    {"date": "2024-05-10", "category": "Одяг", "amount": 2200.0},
    {"date": "2024-05-11", "category": "Транспорт", "amount": 150.0},
    {"date": "2024-05-12", "category": "Продукти", "amount": 910.0},
    {"date": "2024-05-13", "category": "Освіта", "amount": 1500.0},
    {"date": "2024-05-14", "category": "Розваги", "amount": 380.0},
    {"date": "2024-05-15", "category": "Продукти", "amount": 480.0},
    {"date": "2024-05-16", "category": "Транспорт", "amount": 110.0},
    {"date": "2024-05-17", "category": "Здоров'я", "amount": 260.0},
    {"date": "2024-05-18", "category": "Одяг", "amount": 1300.0},
    {"date": "2024-05-19", "category": "Продукти", "amount": 730.0},
]

# Список бажаних покупок (price — грн, value — пріоритет 1..10)
WISHLIST: List[Dict] = [
    {"name": "Навушники", "price": 2500, "value": 7},
    {"name": "Ноутбук-сумка", "price": 1200, "value": 4},
    {"name": "Курс Python", "price": 3000, "value": 9},
    {"name": "Кросівки", "price": 2800, "value": 6},
    {"name": "Монітор", "price": 6000, "value": 8},
    {"name": "Книги", "price": 900, "value": 5},
    {"name": "Клавіатура", "price": 1800, "value": 6},
    {"name": "Рюкзак", "price": 1500, "value": 3},
]


def total_by_category(data: List[Dict], category: str) -> float:
    """Сума витрат за категорією: filter + map + reduce."""
    selected = filter(lambda t: t["category"].lower() == category.lower(), data)
    amounts = map(lambda t: t["amount"], selected)
    return reduce(lambda a, b: a + b, amounts, 0.0)


# --------------------------------------
# Допоміжні функції введення (валідація)
# --------------------------------------


def read_float(prompt: str, min_value: float = None) -> float:
    """Зчитує число з клавіатури, повторюючи запит при помилці."""
    while True:
        try:
            value = float(input(prompt).replace(",", "."))
            if min_value is not None and value < min_value:
                print(f"  Значення має бути не менше {min_value}.")
                continue
            return value
        except ValueError:
            print("  Помилка: введіть число.")


def read_int(prompt: str, min_value: int = None) -> int:
    """Зчитує ціле число з клавіатури, повторюючи запит при помилці."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"  Значення має бути не менше {min_value}.")
                continue
            return value
        except ValueError:
            print("  Помилка: введіть ціле число.")


# -----------
# Пункти меню
# -----------


def show_transactions() -> None:
    print(f"\n{'Дата':<12}{'Категорія':<14}{'Сума, грн':>10}")
    print("-" * 36)
    for t in TRANSACTIONS:
        print(f"{t['date']:<12}{t['category']:<14}{t['amount']:>10.2f}")
    total = reduce(lambda acc, t: acc + t["amount"], TRANSACTIONS, 0.0)
    print("-" * 36)
    print(f"{'Разом':<26}{total:>10.2f}")


def menu_loan() -> None:
    principal = read_float("Сума кредиту, грн: ", 1)
    rate = read_float("Річна ставка, %: ", 0)
    months = read_int("Термін, місяців: ", 1)
    payment = monthly_loan_payment(principal, rate, months)
    print(f"Щомісячний платіж: {payment:,.2f} грн")
    print(f"Загальна виплата:  {payment * months:,.2f} грн")
    print(f"Переплата:         {payment * months - principal:,.2f} грн")


def menu_deposit() -> None:
    principal = read_float("Сума вкладу, грн: ", 0)
    rate = read_float("Річна ставка, %: ", 0)
    years = read_float("Термін, років: ", 0)
    raw = input("Капіталізацій на рік (Enter — 12): ").strip()
    if raw:
        result = compound_interest(principal, rate, years, int(raw))
    else:
        result = compound_interest(principal, rate, years)
    print(f"Сума наприкінці терміну: {result:,.2f} грн (дохід {result - principal:,.2f} грн)")


def menu_budget() -> None:
    income = read_float("Місячний дохід, грн: ", 0.01)
    expenses = read_float("Місячні витрати, грн: ", 0)
    balance, rate = calculate_budget_balance(income, expenses)
    print(f"Баланс: {balance:,.2f} грн, норма заощаджень: {rate:.1f}%")
    if rate < 10:
        print("Порада: намагайтесь відкладати щонайменше 10% доходу.")


def menu_average() -> None:
    raw = input("Введіть суми витрат через пробіл: ").split()
    values = [float(x.replace(",", ".")) for x in raw]
    print(f"Середня витрата: {average_expense(*values):.2f} грн")


def menu_categories() -> None:
    categories = sorted(set(map(lambda t: t["category"], TRANSACTIONS)))
    print("Категорії:", ", ".join(categories))
    cat = input("Введіть категорію: ").strip()
    if cat.lower() not in (c.lower() for c in categories):
        print("Такої категорії немає.")
        return
    print(f"Разом за категорією «{cat}»: {total_by_category(TRANSACTIONS, cat):.2f} грн")


def menu_convert() -> None:
    rate = read_float("Курс (грн за 1 одиницю валюти): ", 0.0001)
    converted = apply_to_amounts(TRANSACTIONS, lambda x: x / rate)
    print("Перші 5 витрат у валюті:")
    for t in converted[:5]:
        print(f"{t['date']}  {t['category']:<12}{t['amount']:.2f}")


def menu_vat() -> None:
    price = read_float("Ціна без ПДВ, грн: ", 0)
    print(f"Ціна з ПДВ 20%: {price_with_vat(price):.2f} грн")
    vat = read_float("Інша ставка ПДВ, %: ", 0)
    print(f"Ціна з ПДВ {vat:g}%: {price_with_vat(price, vat):.2f} грн")
    old = read_float("Стара ціна для порівняння: ", 0.01)
    print(f"Зміна ціни: {percent_change(old, price):+.1f}%")


def menu_wishlist() -> None:
    print("\nСписок бажаних покупок:")
    for i in WISHLIST:
        print(f"  {i['name']:<15}{i['price']:>6} грн  пріоритет {i['value']}")
    budget = read_int("Ваш бюджет, грн: ", 0)
    value, names = best_purchases(WISHLIST, budget)
    if not names:
        print("З таким бюджетом нічого не вдасться купити.")
        return
    cost = sum(i["price"] for i in WISHLIST if i["name"] in names)
    print(f"Оптимальний набір: {', '.join(names)}")
    print(f"Вартість: {cost} грн, сумарний пріоритет: {value}")


# ----------------
# Головна програма
# ----------------


def main() -> None:
    actions = {
        1: ("Показати витрати за місяць", show_transactions),
        2: ("Розрахувати платіж за кредитом", menu_loan),
        3: ("Розрахувати вклад (складний відсоток)", menu_deposit),
        4: ("Баланс бюджету та заощадження", menu_budget),
        5: ("Середня витрата (довільна кількість значень)", menu_average),
        6: ("Сума витрат за категорією (filter/map/reduce)", menu_categories),
        7: ("Перевести витрати у валюту (функція вищого порядку)", menu_convert),
        8: ("Ціна з ПДВ та зміна ціни (lambda)", menu_vat),
        9: ("Оптимальні покупки за бюджетом (рекурсія)", menu_wishlist),
    }
    print("Вітаємо в програмі «Особисті фінанси»!")
    while True:
        print("\nОберіть операцію:")
        for key, (title, _) in actions.items():
            print(f"{key}. {title}")
        print("0. Вийти")
        try:
            choice = int(input("Ваш вибір: "))
            if choice == 0:
                print("Дякуємо за використання програми!")
                break
            if choice in actions:
                actions[choice][1]()
            else:
                print("Невірний вибір. Спробуйте ще раз.")
        except ValueError as e:
            print(f"Помилка введення: {e}")
        except ZeroDivisionError:
            print("Помилка: ділення на нуль.")
        except (KeyboardInterrupt, EOFError):
            print("\nВихід з програми.")
            break


if __name__ == "__main__":
    main()
