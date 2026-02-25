# 🚀 Python Automation Practice

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Pytest](https://img.shields.io/badge/Pytest-Testing-green.svg)](https://docs.pytest.org)
[![Selenium](https://img.shields.io/badge/Selenium-Automation-orange.svg)](https://selenium.dev)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://www.conventionalcommits.org/)


**Практический репозиторий для системного роста от Junior к Middle QA Automation Engineer на Python.**

---
[Аллюр отчеты](https://myladydarkness.github.io/Python_automation_practice/4/index.html)

## 📌 Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone https://github.com/<ваш-логин>/python-automation-practice.git

# 2. Перейти в папку проекта
cd python-automation-practice

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить тесты
pytest tests/ -v --html=reports/report.html

🎯 Цели проекта
Цель	Статус
✅ Создать структурированный тестовый фреймворк	В процессе
✅ Освоить паттерны (POM, API Clients)	В процессе
✅ Настроить CI/CD (GitHub Actions)	Готово
🔄 Интегрировать Docker	Запланировано
🔄 Подготовить портфолио для собеседований	Запланировано

📁 Архитектура проекта

python-automation-practice/
├── docs/                    # 📚 Документация и справочники
│   ├── framework_guide.py   # 🔗 Главный справочник (см. разделы ниже)
│   └── learning_roadmap.md  # 🗺️  Персональный план развития
├── src/                     # 💻 Исходный код фреймворка
│   ├── pages/              # 🖥️  Page Objects
│   ├── api/                # 🔌 API клиенты
│   ├── utils/              # 🛠️  Вспомогательные функции
│   └── config/             # ⚙️  Конфигурация
├── tests/                   # 🧪 Тесты
│   ├── ui/                 # 🌐 UI-тесты (Selenium)
│   └── api/                # 📡 API-тесты (Requests)
├── data/                   # 📊 Тестовые данные
├── reports/                # 📈 Отчёты (генерируются)
└── .github/workflows/      # ⚡ CI/CD (GitHub Actions)
Подробное описание структуры: docs/framework_guide.py#L7-архитектура-проекта

📚 Ключевые разделы справочника
Основные паттерны и решения собраны в едином файле-справочнике:

```
#### 🏗️ Framework Guide - Оглавление

- [1. Базовые импорты](docs/framework_guide.py#section-imports#L25)
- [1.2. Фикстуры Pytest](docs/framework_guide.py#section-fixtures#L53)  
- [1.3. Page Object Pattern](docs/framework_guide.py#section-pom#L68)
- [2. Типичные конструкции PYTHON в автотестах](docs/framework_guide.py#section-patterns#L98)
- [3. Архитектура проекта](docs/framework_guide.py#section-architecture#L208)
- [4. Conventional Commits](docs/framework_guide.py#section-commits#L361)
- [5. Решения распространеных проблем](docs/framework_guide.py#section-troubleshooting#L376)

```

🛠️ Технологический стек

Технология	Назначение	Версия
Python	Основной язык	3.9+
Pytest	Фреймворк для тестов	7.0+
Selenium	Автоматизация браузера	4.0+
Requests	HTTP-запросы (API)	2.28+
Allure	Генерация отчётов	2.9+
Docker	Контейнеризация	20.10+
GitHub Actions	CI/CD	-

📖 Как пользоваться справочником

При создании нового файла → откройте раздел "Структура проекта", чтобы понять, куда его поместить.
При написании теста → используйте "Page Object Pattern" для UI или "Базовые конструкции" для API.
При коммите изменений → сверьтесь с "Conventional Commits" для правильного сообщения.
При возникновении вопроса → поищите ответ в соответствующем разделе framework_guide.py.

📈 Прогресс обучения

✅ Завершено
Создана базовая структура репозитория
Написан главный справочник (framework_guide.py)

🔄 В процессе
Реализованы базовые фикстуры Pytest
Добавлен Page Object Pattern
API-тестирование с Requests
Параметризация тестов
Генерация Allure-отчётов

📅 Запланировано
Настройка GitHub Actions
Docker-контейнеризация тестов
Интеграция с реальным API


🔗 Полезные ресурсы
Ресурс	Описание
Test Automation University	Бесплатные курсы по автоматизации
Selenium Python Docs	Официальная документация
Pytest Documentation	Руководство по Pytest
Conventional Commits	Спецификация коммитов
Real Python	Уроки и статьи по Python
