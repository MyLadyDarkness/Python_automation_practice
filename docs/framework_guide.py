"""
GUIDE для фреймворка автоматизации тестирования (Python + Pytest + Selenium).
Содержит базовые шаблоны для быстрого старта нового проекта или восстановления в памяти ключевых конструкций.
Цель: обеспечить единый код-стайл и ускорить разработку стандартных компонентов.
"""


""" РАЗДЕЛ 1: БАЗОВЫЙ КАРКАС ФРЕЙМВОРКА """

# ------------------------------------------------------------
# 1.1. ФИКСТУРЫ PYTEST
import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)  # Неявное ожидание (осторожно!)
    yield driver  # Тест выполняется здесь
    driver.quit()  # Выполнится после теста

# ------------------------------------------------------------
# 1.2. PAGE OBJECT PATTERN (БАЗОВАЯ СТРАНИЦА)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Явное ожидание

    def find(self, locator):
        return self.driver.find_element(*locator)

    def wait_for_element(self, locator):
        """Ждем КЛИКАБЕЛЬНОСТИ элемента"""
        return self.wait.until(EC.element_to_be_clickable(locator))

# ------------------------------------------------------------
# 1.3. ПРИМЕР ТЕСТА
def test_login(driver):
    page = LoginPage(driver)  # Ваш класс
    page.login("username", "password")
    assert page.is_logged_in()


"""
РАЗДЕЛ 2: ТИПИЧНЫЕ КОНСТРУКЦИИ PYTHON В АВТОТЕСТАХ
Примеры использования базового синтаксиса для решения практических задач QA.
"""

# ------------------------------------------------------------
# 2.1 РАБОТА СО СЛОВАРЯМИ (DICT): ПОДГОТОВКА И ПРОВЕРКА ТЕСТОВЫХ ДАННЫХ
# ------------------------------------------------------------
from selenium.common.exceptions import NoSuchElementException

def merge_test_data(default_config, user_config):
    """
    Слияние конфигураций: значения из user_config перезаписывают default_config.
    Типичный случай: дефолтные настройки теста + специфичные параметры для кейса.
    """
    return {**default_config, **user_config}

def assert_dict_contains(expected_subset, actual_dict):
    """
    Проверяет, что actual_dict содержит ВСЕ пары ключ-значение из expected_subset.
    Используется, когда нужно проверить часть ответа API или объекта.
    """
    for key, expected_value in expected_subset.items():
        assert key in actual_dict, f"Ключ '{key}' отсутствует в {actual_dict}"
        assert actual_dict[key] == expected_value, f"Значение для ключа '{key}': ожидалось {expected_value}, получено {actual_dict[key]}"
    return True  # Если все ассерты прошли

# ------------------------------------------------------------
# 2.2 ОБРАБОТКА ИСКЛЮЧЕНИЙ (TRY/EXCEPT/FINALLY): ДЕЛАЕМ ТЕСТЫ УСТОЙЧИВЫМИ
# ------------------------------------------------------------

def get_element_text_safe(driver, locator, default="Элемент не найден"):
    """
    Безопасное получение текста элемента. Если элемент не найден,
    возвращает default-значение вместо падения теста.
    Полезно для проверок в нестабильных условиях.
    """
    try:
        return driver.find_element(*locator).text
    except NoSuchElementException:
        print(f"Предупреждение: элемент {locator} не найден. Возвращаю default.")
        return default
    # Блок finally здесь не нужен, т.к. нет ресурсов для очистки

# КЛАССИЧЕСКИЙ ПАТТЕРН: ОЧИСТКА ТЕСТОВЫХ ДАННЫХ В FINALLY
def test_create_and_delete_user(api_client):
    """
    Шаблон теста, где созданные данные нужно удалить ЛЮБОЙ ЦЕНОЙ,
    даже если сам тест упал. Гарантирует чистоту окружения.
    """
    test_user = None
    try:
        # 1. Подготовка
        test_user = api_client.create_user({"name": "Test"})
        user_id = test_user["id"]

        # 2. Основная логика теста
        fetched_user = api_client.get_user(user_id)
        assert fetched_user["name"] == "Test"

        # 3. Тест может упасть здесь, но...
        # some_operation_that_might_fail()

    except AssertionError:
        # 4. ...этот блок перехватит падение ассерта
        print("Тест упал на ассерте, но данные всё равно будут очищены")
        raise  # Поднимаем исключение снова, чтобы тест был отмечен как упавший
    except Exception as e:
        # 5. ...а этот блок - любое другое исключение
        print(f"Тест упал с ошибкой: {e}")
        raise
    finally:
        # 6. ВЫПОЛНИТСЯ ВСЕГДА: даже если тест прошёл, даже если упал
        if test_user:
            print("Очистка: удаляю тестового пользователя")
            api_client.delete_user(test_user["id"])

# ------------------------------------------------------------
# 2.3 ИТЕРАЦИИ (FOR/IN): АНАЛИЗ КОЛЛЕКЦИЙ В ТЕСТАХ
# ------------------------------------------------------------

def check_all_items_in_list(actual_items, expected_items):
    """
    Проверяет, что все элементы из expected_items присутствуют в actual_items.
    Читаемее, чем множества, когда важен порядок или нужно детальное логирование.
    """
    missing_items = []
    for item in expected_items:
        if item not in actual_items:
            missing_items.append(item)
    
    assert not missing_items, f"Эти элементы не найдены: {missing_items}"
    return True

def find_failed_tests(test_results):
    """
    Фильтрация коллекции: отбор только упавших тестов.
    Показывает типичное использование filter() и list comprehension.
    """
    # Способ 1: Через list comprehension (питонично и читаемо)
    failed_listcomp = [test for test in test_results if test["status"] == "FAILED"]
    
    # Способ 2: Через filter и lambda (функциональный стиль)
    failed_filter = list(filter(lambda test: test["status"] == "FAILED", test_results))
    
    # В реальном коде выберите один стиль и придерживайтесь его
    return failed_listcomp


"""
РАЗДЕЛ 3: АРХИТЕКТУРА: СТРУКТУРА ПРОЕКТА И КОНВЕНЦИИ
---------------------------------------------------------------
Цель: единый источник правды по организации кода.
Зачем: новая команда (или вы через месяц) сможет быстро разобраться.
"""

PROJECT_STRUCTURE = """
python-automation-practice/          # Корень репозитория
│
├── .github/workflows/               # CI/CD: автоматический запуск тестов
│   └── run-tests.yml               # Паттерн имени: <что-делает>.yml
│
├── docs/                            # ДОКУМЕНТАЦИЯ (не код!)
│   ├── framework_guide.py          # Этот файл. Главная шпаргалка.
│   ├── decisions.md                # Архитектурные решения (почему выбрали Pydantic?)
│   └── api_coverage.md             # Какие эндпоинты покрыты тестами
│
├── src/                             # ИСХОДНЫЙ КОД фреймворка (переиспользуемый)
│   ├── pages/                      # PAGE OBJECTS: по одному файлу на страницу/попап
│   │   ├── __init__.py             # Делает папку Python-пакетом
│   │   ├── base_page.py            # BasePage с общими методами (find, click, wait)
│   │   ├── login_page.py           # LoginPage(BasePage) - наследует BasePage
│   │   └── cart_page.py            # Соглашение: <name>_page.py
│   │
│   ├── api/                        # API КЛИЕНТЫ и модели данных
│   │   ├── __init__.py
│   │   ├── client.py               # Главный класс APIClient (синглтон)
│   │   ├── models.py               # Pydantic-модели для валидации ответов
│   │   └── endpoints/              # Отдельная папка, если эндпоинтов много
│   │       └── auth_api.py         # AuthApi(APIClient) - для работы с /auth
│   │
│   ├── utils/                      # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (статические)
│   │   ├── __init__.py
│   │   ├── file_helpers.py         # read_json, write_csv
│   │   ├── wait_helpers.py         # custom_wait, click_first_enabled
│   │   └── data_generators.py      # fake_email, random_string
│   │
│   └── config/                     # КОНФИГУРАЦИЯ (окружение, настройки)
│       ├── __init__.py
│       ├── settings.py             # Загружает .env, задаёт BASE_URL
│       └── constants.py            # TIMEouts, DEFAULT_USER, Colors
│
├── tests/                          # ТЕСТЫ (используют код из src/)
│   ├── ui/                         # UI-тесты
│   │   ├── __init__.py
│   │   ├── test_login.py          # Паттерн: test_<фича>[_<деталь>].py
│   │   ├── test_cart.py
│   │   └── smoke/                 # Подпапка для маркера @pytest.mark.smoke
│   │       └── test_smoke_ui.py
│   │
│   ├── api/                        # API-тесты
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   └── test_user_crud.py      # CRUD = Create, Read, Update, Delete
│   │
│   └── conftest.py                 # ФИКСТУРЫ PYTEST: драйвер, api_client
│
├── data/                           # ТЕСТОВЫЕ ДАННЫЕ (отдельно от кода)
│   ├── users.json                 # Список тестовых пользователей
│   ├── products.csv
│   └── schemas/                   # JSON-схемы для валидации API
│       └── user_schema.json
│
├── reports/                        # ОТЧЁТЫ (в .gitignore, создаются автоматически)
│   ├── html/                       # pytest-html
│   └── allure-results/             # Allure
│
├── .gitignore                     # Игнорировать reports/, .env, __pycache__/
├── requirements.txt               # Зависимости: pytest, selenium, requests...
├── pytest.ini                     # Конфиг pytest: маркеры, параметры
├── docker-compose.yml            # Запуск тестов в контейнере
└── README.md                     # Визитка: как запустить, технологии
"""

# ------------------------------------------------------------
# КЛЮЧЕВЫЕ КОНВЕНЦИИ ИМЁН (CODING CONVENTIONS)
# ------------------------------------------------------------

NAMING_RULES = """
ФАЙЛЫ:
- Python-файлы: в snake_case (login_page.py, test_user_crud.py)
- Папки: в snake_case (test_data, api_client)
- Тесты: начинаются с test_ (test_login_success, test_login_invalid_password)

КЛАССЫ:
- Page Objects: <Name>Page (LoginPage, CartPage) - PascalCase
- API Clients: <Name>Client (AuthClient, UserClient) - PascalCase
- Исключения: <Name>Error (ElementNotFoundError) - PascalCase

ПЕРЕМЕННЫЕ И ФУНКЦИИ:
- переменные: snake_case (user_name, timeout_seconds)
- функции: snake_case (click_element, read_config_file)
- константы: UPPER_SNAKE_CASE (DEFAULT_TIMEOUT, BASE_URL)

ЛОКАТОРЫ (в Page Objects):
- Для Selenium: <ELEMENT>_<TYPE> (USERNAME_INPUT, LOGIN_BUTTON, ERROR_SPAN)
- Для Appium: добавлять префикс ANDROID_ или IOS_ (ANDROID_LOGIN_BUTTON)

ФИКСТУРЫ PYTEST:
- Имя = что возвращает (driver, api_client, chrome_options)
- scope: 'function' (по умолчанию), 'class', 'module', 'session'
"""

# ------------------------------------------------------------
# ЧТО КУДА КЛАСТЬ: БЫСТРАЯ СПРАВКА
# ------------------------------------------------------------

WHERE_TO_PUT = {
    "Новый UI-тест для корзины": "tests/ui/test_cart.py",
    "Новый метод 'отправить сообщение' на странице чата": "src/pages/chat_page.py",
    "Функция для генерации тестового email": "src/utils/data_generators.py",
    "Фикстура для подключения к БД": "tests/conftest.py",
    "Константа с URL staging-окружения": "src/config/constants.py",
    "Модель Pydantic для ответа API пользователя": "src/api/models.py",
    "JSON-схема для валидации заказа": "data/schemas/order_schema.json",
    "Новый маркер pytest '@pytest.mark.slow'": "pytest.ini",
    "Шаги для запуска в Docker": "docker-compose.yml",
    "Описание архитектуры фреймворка": "docs/decisions.md"
}

def explain_structure():
    """Печатает пояснение структуры (для запуска в консоли)."""
    print("=" * 60)
    print("СТРУКТУРА ПРОЕКТА АВТОМАТИЗАЦИИ")
    print("=" * 60)
    print("\n1. src/ - КОД ФРЕЙМВОРКА (переиспользуемый, логика)")
    print("   pages/    - Page Objects (один файл = одна страница)")
    print("   api/      - API клиенты и модели данных")
    print("   utils/    - Вспомогательные функции (статичные)")
    print("   config/   - Настройки и константы")
    
    print("\n2. tests/ - ТЕСТЫ (используют код из src/)")
    print("   ui/      - UI-тесты (Selenium)")
    print("   api/     - API-тесты (requests)")
    print("   conftest.py - Фикстуры (драйвер, api_client)")
    
    print("\n3. data/ - ТЕСТОВЫЕ ДАННЫЕ (отдельно от кода)")
    print("   *.json, *.csv - Данные для параметризации")
    print("   schemas/ - JSON-схемы для валидации API")
    
    print("\n4. docs/ - ДОКУМЕНТАЦИЯ")
    print("   framework_guide.py - Эта шпаргалка")
    print("   decisions.md - Почему выбрали ту или иную архитектуру")
    
    print("\nПолный путь см. в переменной PROJECT_STRUCTURE выше.")

# Пример использования в коде:
if __name__ == "__main__":
    # Можете запустить файл, чтобы посмотреть структуру
    explain_structure()     

"""
РАЗДЕЛ 4: Conventional Commits
---------------------------------------------------------------
Цель: единый источник правды по организации кода.
Зачем: новая команда (или вы через месяц) сможет быстро разобраться.
"""

Префиксы (Conventional Commits):

feat: — новая функциональность
fix: — исправление бага
docs: — изменения в документации
build: — изменения в сборке/структуре
refactor: — рефакторинг без изменения функциональности

""" РАЗДЕЛ: КАК РЕШАТЬ ОБЩИЕ ПРОБЛЕМЫ """
# ----------------------------------------------
# ПРОБЛЕМА: Элемент устарел (StaleElementReferenceException)
# РЕШЕНИЕ: Повторно найти элемент внутри цикла/ожидания
def safe_click(driver, locator):
    try:
        driver.find_element(*locator).click()
    except StaleElementReferenceException:
        # Ждем и пробуем снова с обновленным элементом
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(locator)
        ).click()
