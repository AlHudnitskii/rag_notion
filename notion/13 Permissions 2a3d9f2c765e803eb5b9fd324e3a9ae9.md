# 13. Permissions

Категория: SQL Databases
Статус: Готово

На уровне таблиц можно определить политики защиты строк, которые могут быть возвращены обычными запросами, изменены и удалены командами, изменяющими данные. Это называется также *защитой на уровне строк* (RLS, Row-Level Security). 

Когда для таблицы включается защита строк (с помощью команды [ALTER TABLE ... ENABLE ROW LEVEL SECURITY](https://postgrespro.ru/docs/postgrespro/current/sql-altertable.html)), все обычные запросы к таблице на выборку или модификацию строк должны разрешаться политикой защиты строк. (Однако на владельца таблицы такие политики обычно не действуют.) Если политика для таблицы не определена, применяется политика запрета по умолчанию, так что никакие строки в этой таблице нельзя увидеть или модифицировать. На операции с таблицей в целом, такие как `TRUNCATE` и `REFERENCES`, защита строк не распространяется.

Неотъемлемое право включать или отключать защиту строк, а также определять политики для таблицы, имеет только её владелец.

Для создания политик предназначена команда [CREATE POLICY](https://postgrespro.ru/docs/postgrespro/current/sql-createpolicy.html), для изменения — [ALTER POLICY](https://postgrespro.ru/docs/postgrespro/current/sql-alterpolicy.html), а для удаления — [DROP POLICY](https://postgrespro.ru/docs/postgrespro/current/sql-droppolicy.html). Чтобы включить или отключить защиту строк для определённой таблицы, воспользуйтесь командой [ALTER TABLE](https://postgrespro.ru/docs/postgrespro/current/sql-altertable.html).

![image.png](image%20382.png)

### Пример работы RLS

![image.png](image%20383.png)

![image.png](image%20384.png)