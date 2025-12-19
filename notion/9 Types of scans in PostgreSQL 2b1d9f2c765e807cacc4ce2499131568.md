# 9. Types of scans in PostgreSQL

Категория: SQL Databases
Статус: Готово

В реляционных БД данные хранятся в страницах, и страница представляет собой блок памяти фиксированного размера. В Postgres размер страницы обычно составляет 8 КБ.
В реляционных базах данных индексы обычно хранятся в структуре данных B-дерево, а фактические строки данных таблицы хранятся в куче (heap) в виде страниц.
B-дерево является структурированной и упорядоченной структурой, поэтому поиск в индексах выполняется намного-намного быстрее. Когда база данных находит совпадение в индексе и ей требуются какие-то данные из соответствующей строки, база данных перейдёт в кучу и получит необходимые данные.

![image.png](image%20723.png)

Сканирование в PostgreSQL — это процесс, который база данных использует для чтения данных из таблицы.
Давайте посмотрим, какие типы сканирования существуют и какое сканирование используется в каких условиях в Postgres.

### Типы сканирования

1. Index Scan (Сканирование по индексу)

Когда вам нужно выбрать очень избирательные строки, или если вы выбираете много строк через диапазонный запрос на индексе первичного ключа, и индекс присутствует для параметра поиска, тогда выполняется сканирование по индексу.

![image.png](image%20724.png)

![image.png](image%20725.png)

1. Index Only Scan (Сканирование только по индексу)

Postgres выполнит сканирование только по индексу, когда базе данных не нужно обращаться в кучу, так как все необходимые данные присутствуют в самом индексе.

![image.png](image%20726.png)

![image.png](image%20727.png)

Здесь базе данных не нужно обращаться в кучу. Поэтому это сканирование только по индексу.

1. Sequential Scan (Последовательное сканирование)

Postgres выберет последовательный поиск в наихудшем случае. Потому что здесь ему приходится обходить кучу, что очень медленно. Это может произойти в нескольких сценариях:

- Когда вы выбираете слишком много строк
- Когда индексирование отсутствует для параметра поиска

![image.png](image%20728.png)

![image.png](image%20729.png)

Как видите, я выбираю более полумиллиона строк — около 60% от общего количества строк.

Таким образом, даже если для `id` есть индекс, он не сканирует индекс, потому что частое переключение между B-деревом и кучей очень затратно по времени.

1. Bitmap Scan (Битовое сканирование)

Bitmap Index Sca[n](https://www.google.com/search?q=Bitmap+Index+Scan&client=opera&hs=ciq&sca_esv=a660b44055a2f0e3&sxsrf=AE3TifPHjmtJQwA8sMMQsMA6Eyyq5-Ruxg%3A1763652141103&ei=LTIfaZqBBo28xc8P1vXR0Ag&ved=2ahUKEwj9gJCehIGRAxUJBNsEHd5rCZ0QgK4QegQIARAB&uact=5&oq=bitmap+index+scan+vs+bitmap+heap+scan+%D0%BE%D0%B1%D1%8A%D1%8F%D1%81%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5&gs_lp=Egxnd3Mtd2l6LXNlcnAiOmJpdG1hcCBpbmRleCBzY2FuIHZzIGJpdG1hcCBoZWFwIHNjYW4g0L7QsdGK0Y_RgdC90LXQvdC40LUyCBAAGIAEGKIEMggQABiABBiiBDIFEAAY7wUyBRAAGO8FSJUUUAxYphJwAXgBkAEBmAHcAaABswyqAQYwLjEwLjG4AQPIAQD4AQGYAgugAsoLwgIKEAAYsAMY1gQYR8ICBhAAGBYYHsICBBAhGBXCAgkQIRigARgKGCqYAwCIBgGQBgiSBwUxLjkuMaAH0ByyBwUwLjkuMbgHxQvCBwYwLjEwLjHIBxc&sclient=gws-wiz-serp&mstk=AUtExfCsXw2jpaF_zqEIvHLSrfuXjPFKTpqtOZyN6klXa0CD58H49duev3Cs97De9nm3v7dVFpg8fWnaLx-bPO0RrE6eMdnvyvrVSLCVH5ZHJvVrYwG1Of5vPq3ggi_5GOXNzW41R35FYIPlF_ist40oN9kSp2x94ta9PdopTwSlCbXqR4pz-AYevFqIDWJQE0jiH5TlnRSDsLYhtAUPSiP6yDsqotj-9I7vOFQ8qjYp_xBNL0-VCOTP8N3_zWtS50PPd_9WLEsLWZ3Q9FiXBO2QdBNs&csui=3) и Bitmap Heap Scan — это два этапа в плане выполнения запроса, которые работают вместе, чтобы найти данные. 

1. Bitmap Index Scan сначала создает битовую карту, отмечая страницы данных, которые могут содержать искомые значения, используя один или несколько индексов. 
2. Затем, Bitmap Heap Scan использует эту битовую карту для фактического извлечения строк из кучи (таблицы), читая страницы в том порядке, в котором они расположены на диске, чтобы уменьшить количество случайных операций ввода-вывода. 

![image.png](image%20730.png)