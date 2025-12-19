# 7. Migrations testing

Категория: Testing
Статус: В процессе

**Миграция** — это способ версионирования и управления изменениями схемы базы данных.

**Основные инструменты в Python:**

- **Alembic** — для SQLAlchemy (Flask, FastAPI)
- **Django Migrations** — встроено в Django

Зачем тестировать миграции?

1. Потеря данных
2. Долгие блокировки (Downtime)
3. Несовместимость кода и схемы
4. Невозможность отката
5. Баги в трансформации данных

## Структура Django-миграции

![image.png](image%20322.png)

### Основные типы операций

1. migrations.CreateModel
2.  migrations.AddField
3.  migrations.RemoveField
4. migrations.RenameField
5. migrations.AlterField
6. migrations.AddIndex
7. migrations.AddConstraint

![image.png](image%20323.png)

![image.png](image%20324.png)

![image.png](image%20325.png)

Тестирование django-миграций с помощью pytest

![image.png](image%20326.png)

![image.png](image%20327.png)

**Alembic** — инструмент миграций для SQLAlchemy (используется с Flask, FastAPI, чистым SQLAlchemy).

**Отличия от Django:**

- Не автогенерирует миграции (нужно писать руками или использовать `alembic revision --autogenerate`)
- Более низкоуровневый контроль
- Работает с любым фреймворком (не привязан к Django)

![image.png](image%20328.png)

 Структура миграции Alembic

![image.png](image%20329.png)

![image.png](image%20330.png)

### Тестирование Alembic Migrations

![image.png](image%20331.png)

![image.png](image%20332.png)

Пример теста в таком случае

![image.png](image%20333.png)

### pytest-alembic — специализированный плагин

![image.png](image%20334.png)