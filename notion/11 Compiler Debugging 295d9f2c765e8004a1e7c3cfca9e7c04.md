# 11. Compiler Debugging

Категория: Python Core
Статус: В процессе

В  Python есть встроенный отладчик PDB (Python Debugger)

**PDB** — это интерактивный отладчик командной строки, встроенный в Python.

![image.png](image%2054.png)

![image.png](image%2055.png)

Альтернатива c Python 2.7+ - breakpoint()

![image.png](image%2056.png)

Можно ставить условия на breakpoints.

![image.png](image%2057.png)

Запуск с PDB в командной строке:

![image.png](image%2058.png)

Можно в PDB выполнять произвольный код Python

![image.png](image%2059.png)

## Debugging Multithreading Applications

### Проблемы отладки многопоточных приложений

**Основные сложности:**

- Race conditions (состояние гонки)
- Deadlocks (взаимоблокировки)
- Сложно отследить порядок выполнения
- PDB плохо работает с потоками

![image.png](image%2060.png)

Отладка deallock

![image.png](image%2061.png)

![image.png](image%2062.png)

PDB-отладка через сеть

![image.png](image%2063.png)

![image.png](image%2064.png)

Отладка Docker контейнеров

![image.png](image%2065.png)

## GDB для Python (отладка на уровне C)

### Когда использовать GDB

- Сегфолты (Segmentation Fault)
- Зависания интерпретатора
- Проблемы с C-расширениями
- Глубокая диагностика

![image.png](image%2066.png)

## SQL Debugging

### Отладка SQL запросов в Python

### SQLAlchemy с логированием

![image.png](image%2067.png)

Django SQL debugging

![image.png](image%2068.png)

![image.png](image%2069.png)