# 9. Monitoring & Logging

Категория: Infr as code & CI/CD & General Theory
Статус: Проверено

**Логирование** — это процесс записи событий, происходящих в системе. Логи содержат информацию о действиях программного обеспечения, пользователях и возникающих ошибках. Они помогают анализировать работу системы и выявлять причины проблем.

**Мониторинг** — это непрерывное наблюдение за состоянием системы и ее компонентов. Он позволяет отслеживать производительность, доступность и безопасность приложений и серверов.

## **Зачем нужны логирование и мониторинг**

1. **Обнаружение и устранение проблем**
    - Логирование помогает идентифицировать ошибки и понять их причины.
    - Мониторинг позволяет оперативно реагировать на сбои и предупреждать о потенциальных проблемах.
2. **Оптимизация производительности**
    - Анализ логов позволяет выявить узкие места в работе приложений.
    - Мониторинг ресурсов (например, использование CPU и памяти) помогает оптимизировать их распределение.
3. **Аудит и безопасность**
    - Логирование записывает действия пользователей и изменения в системе, что важно для соблюдения нормативных требований.
    - Мониторинг помогает обнаруживать подозрительную активность и предотвращать атаки.

## **Типы логов**

Логи могут быть разделены на несколько типов в зависимости от их назначения:

- **Системные логи**: фиксируют события, происходящие на уровне операционной системы.
- **Серверные логи**: регистрируют обращения к серверу и возникающие ошибки.
- **Логи приложений**: содержат информацию о работе программного обеспечения.
- **Логи баз данных**: отслеживают запросы и изменения в базе данных.

## **Процесс логирования**

1. **Запись событий**: Система фиксирует события и ошибки, происходящие в процессе работы.
2. **Сохранение данных**: Логи сохраняются в текстовых файлах или в базе данных для последующего анализа.
3. **Анализ**: IT-специалисты используют инструменты для анализа логов, чтобы выявить причины проблем и улучшить производительность.

## **Инструменты для мониторинга и логирования**

Существует множество инструментов, которые помогают в логировании и мониторинге:

- **ELK Stack**: набор инструментов для сбора, хранения и визуализации логов (Elasticsearch, Logstash, Kibana).
- **Prometheus**: система мониторинга и оповещения, предназначенная для сбора метрик с различных источников.
- **Grafana**: платформа для визуализации данных, часто используется в паре с Prometheus.

### Prometeus & Grafana

Prometheus — это система мониторинга и оповещения с открытым исходным кодом, написанная на Go, которая в реальном времени собирает, хранит и анализирует данные временных рядов (метрики) о состоянии серверов, приложений и инфраструктуры , позволяя отслеживать производительность, обнаруживать проблемы и автоматизировать реакции, используя сбор данных по принципу «скрейпинга» (pull) через HTTP-запросы и мощный язык запросов PromQL.

Что он делает:

- Сбор метрик: Периодически опрашивает настроенные «цели» (приложения, серверы) по HTTP-эндпойнтам (например, `/metrics`) и извлекает числовые данные.
- Хранение данных: Сохраняет метрики как временные ряды (значение + метка времени + метки/теги), эффективно управляя большими объемами данных.
- Анализ и запросы: Позволяет писать запросы на языке [PromQL](https://www.google.com/search?client=opera&hs=MLq&sa=X&sca_esv=48308ae346848ecf&biw=2301&bih=1124&sxsrf=AE3TifMPoMQizCX4GVxVH0bnpZX_08u4fA%3A1765716139605&q=PromQL&ved=2ahUKEwjx2pmajb2RAxVOLBAIHSh3FCAQxccNegQIZxAB&mstk=AUtExfAl2yFf-PyrQa4VeW87aanOYwQD8w6KRIYUvnX6HQLxyCNUEzZZ2wPWAaJ2aulM_Bg7umwXnfbTEEZ3NoohOpaMjpR7xFyypRvspehafANZ4-VpYX52GiROSCxbQBOTkYQspoOT6blsvi6A_ImqEm3ktiA3xQklRpKV5qPnpptddWsDMxrFNyKFUA_9ZzvILld2j3isMCK7Gs72q-leawaPFa8voKUgAFGDQuPGo_wkrxPRf9Tnay61IfBtSv20n3HYPsFcRggwVIHezAbVvvZYYKgopjJ2Z9FKP1efs8_WLA&csui=3) для фильтрации, агрегирования и анализа метрик.

Оповещения (Alerting): С помощью Alertmanager генерирует и отправляет уведомления (Email, Slack) при срабатывании заданных правил.

- Оповещения (Alerting): С помощью Alertmanager генерирует и отправляет уведомления (Email, Slack) при срабатывании заданных правил.

![image.png](image%20701.png)

![image.png](image%20702.png)

Интерфейс Прометеуса повзоляет извлекать данные, используя PromQL.

![image.png](image%20703.png)

Для красивой визуализации уже используется непосредcтвенно Grafana. 

![image.png](image%20704.png)

Главное различие: [Elasticsearch](https://www.google.com/search?client=opera&q=Elasticsearch&sourceid=opera&ie=UTF-8&oe=UTF-8&mstk=AUtExfBd_VE7b-q7u9q53VMVzOx4TEFLfrQuTj5OEfOj7Msk4eyjzcFwE0S9I-z0TylwYRRghOBXbS_t9zyL0Azfebz09YL-JhAnGN-NVfZavAWo2THJGFyFAkCy8YYq6snsnm19pJFmx-OHQvF1HDUJSLhnMaZImcOefzoBQLk3XJ_5LxYK5wjlhsKiPef88Cu1c7D8dsbyJtn02EMLiMFPJHNZoTqGTcDSDeKjHwljqZ8L0dQTZVoP3dqFhefD1owRsmGUvHLtvwROgu3R5IPnPR7mFhsJSZQNmpDfK16TPHp3Gv4iwLWM8ZsS0lDLOQ3Sug&csui=3&ved=2ahUKEwj9_u7Vj72RAxWaDRAIHaw9AwAQgK4QegQIARAC) индексирует весь текст логов, что дает мощный поиск, но требует много ресурсов; [Loki](https://www.google.com/search?client=opera&q=Loki&sourceid=opera&ie=UTF-8&oe=UTF-8&mstk=AUtExfBd_VE7b-q7u9q53VMVzOx4TEFLfrQuTj5OEfOj7Msk4eyjzcFwE0S9I-z0TylwYRRghOBXbS_t9zyL0Azfebz09YL-JhAnGN-NVfZavAWo2THJGFyFAkCy8YYq6snsnm19pJFmx-OHQvF1HDUJSLhnMaZImcOefzoBQLk3XJ_5LxYK5wjlhsKiPef88Cu1c7D8dsbyJtn02EMLiMFPJHNZoTqGTcDSDeKjHwljqZ8L0dQTZVoP3dqFhefD1owRsmGUvHLtvwROgu3R5IPnPR7mFhsJSZQNmpDfK16TPHp3Gv4iwLWM8ZsS0lDLOQ3Sug&csui=3&ved=2ahUKEwj9_u7Vj72RAxWaDRAIHaw9AwAQgK4QegQIARAD) индексирует только [метки](https://www.google.com/search?client=opera&q=%D0%BC%D0%B5%D1%82%D0%BA%D0%B8&sourceid=opera&ie=UTF-8&oe=UTF-8&mstk=AUtExfBd_VE7b-q7u9q53VMVzOx4TEFLfrQuTj5OEfOj7Msk4eyjzcFwE0S9I-z0TylwYRRghOBXbS_t9zyL0Azfebz09YL-JhAnGN-NVfZavAWo2THJGFyFAkCy8YYq6snsnm19pJFmx-OHQvF1HDUJSLhnMaZImcOefzoBQLk3XJ_5LxYK5wjlhsKiPef88Cu1c7D8dsbyJtn02EMLiMFPJHNZoTqGTcDSDeKjHwljqZ8L0dQTZVoP3dqFhefD1owRsmGUvHLtvwROgu3R5IPnPR7mFhsJSZQNmpDfK16TPHp3Gv4iwLWM8ZsS0lDLOQ3Sug&csui=3&ved=2ahUKEwj9_u7Vj72RAxWaDRAIHaw9AwAQgK4QegQIARAE) (метаданные), что дешевле и эффективнее для простого поиска и сопоставления логов с метриками (как Prometheus), но менее гибкий в полнотекстовом анализе.

Рассмотрим схему взаимодействия компонентов системы мониторинга на основе Prometheus. Базовая конфигурация состоит из трех компонентов [экосистемы](https://github.com/orgs/prometheus/repositories?type=all):

- [Экспортеры](https://prometheus.io/docs/instrumenting/exporters/) (exporters)
    
    Экспортер собирает данные и возвращает их в виде набора метрик. Экспортеры делятся на официальные (написанные командой Prometheus) и неофициальные (написанные разработчиками различного программного обеспечения для интеграции с Prometheus). При необходимости есть возможность писать свои экспортеры и расширять существующие дополнительными метриками
    
- [Prometheus](https://prometheus.io/docs/concepts/data_model/)
    
    Получает метрики от экспортеров и сохраняет их в БД временных рядов. Поддерживает мощный язык запросов [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/) (Prometheus Query Language) для выборки и аггрегации метрик. Позволяет строить простые  графики и формировать [правила уведомлений](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/) (alerts) на основе выражений PromQL для отправки через Alertmanager
    
- [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)
    
    Обрабатывает уведомления от Prometheus и рассылает их. С помощью механизма [приемников](https://prometheus.io/docs/alerting/latest/configuration/#receiver) (receivers) реализована интеграция с почтой (SMTP), Telegram, Slack и др. системами, а также отправка сообщений в собственный API посредством [вебхуков](https://prometheus.io/docs/alerting/latest/configuration/#webhook_config) (webhook)
    

Таким образом, базовая конфигурация позволяет собирать данные, писать сложные запросы и отправлять уведомления на их основе. Однако по-настоящему потенциал Prometheus раскрывается при добавлении двух дополнительных компонентов (или как минимум одного – Grafana):

- [VictoriaMetrics](https://victoriametrics.com/products/open-source/)
    
    Получает метрики из Prometheus посредством [remote write](https://docs.victoriametrics.com/#prometheus-setup). Поддерживает язык запросов [MetricsQL](https://docs.victoriametrics.com/MetricsQL.html), синтаксис которого совместим с PromQL. Предоставляет оптимизированное по потреблению ресурсов хранение данных и высокопроизводительное выполнение запросов. Идеально подходит для долговременного хранения большого количества метрик
    
    - Примечание
- [Grafana](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/)
    
    Предоставляет средства визуализации и дополнительного анализа информации из Prometheus и VictoriaMetrics. Есть [примеры дашбордов](https://grafana.com/grafana/dashboards/?dataSource=prometheus) практически под любые задачи, которые при необходимости можно легко  доработать. Создание собственных дашбордов также интуитивно (разумеется, за исключением некоторых тонкостей) – достаточно знать основы PromQL / MetricsQL
    
    ![image.png](image%20705.png)
    

Итак, система мониторинга на основе Prometheus – **PAVG** (Prometheus, Alertmanager, VictoriaMetrics, Grafana) – предоставляет широкий спектр возможностей. Рассмотрим ее практическое применение.

### **OpenTelemetry**

OpenTelemetry (OTel) — это открытый стандарт и набор инструментов для сбора и экспорта телеметрических данных ([метрик](https://www.google.com/search?client=opera&q=%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%BA&sourceid=opera&ie=UTF-8&oe=UTF-8&mstk=AUtExfDQtqWOBJ1es91rxVlZXhz98ouKORgyboiNLomjaVszI4ZnBldPZnYeyvnDTk0fYODEsLop0b6fOD3VJtvQCaMz_gOzrd3jk6SJ2R1QHR9jLl4idXKG8u2GwlFd29tDsyUvssqWoYTUaI6qfCs1UIq84CXb6nyYUTOgtR9q-InqCMHWMkvjGmLs0BKqppjZ7u3ah50ITXQIVNekgWDBWt00Yj2LWFLFcZUTTZ7aHhc43GO0m-95Lr4CVccaDrcFhhVgiJ68r4aggMDKr19QQ2Vdebe0viOiuVye-bZzBal87s7YFqxoc1orTxXKqoAODA&csui=3&ved=2ahUKEwjxwaP4kb2RAxWhGRAIHdDsF-gQgK4QegQIARAC), [трассировок](https://www.google.com/search?client=opera&q=%D1%82%D1%80%D0%B0%D1%81%D1%81%D0%B8%D1%80%D0%BE%D0%B2%D0%BE%D0%BA&sourceid=opera&ie=UTF-8&oe=UTF-8&mstk=AUtExfDQtqWOBJ1es91rxVlZXhz98ouKORgyboiNLomjaVszI4ZnBldPZnYeyvnDTk0fYODEsLop0b6fOD3VJtvQCaMz_gOzrd3jk6SJ2R1QHR9jLl4idXKG8u2GwlFd29tDsyUvssqWoYTUaI6qfCs1UIq84CXb6nyYUTOgtR9q-InqCMHWMkvjGmLs0BKqppjZ7u3ah50ITXQIVNekgWDBWt00Yj2LWFLFcZUTTZ7aHhc43GO0m-95Lr4CVccaDrcFhhVgiJ68r4aggMDKr19QQ2Vdebe0viOiuVye-bZzBal87s7YFqxoc1orTxXKqoAODA&csui=3&ved=2ahUKEwjxwaP4kb2RAxWhGRAIHdDsF-gQgK4QegQIARAD), [логов](https://www.google.com/search?client=opera&q=%D0%BB%D0%BE%D0%B3%D0%BE%D0%B2&sourceid=opera&ie=UTF-8&oe=UTF-8&mstk=AUtExfDQtqWOBJ1es91rxVlZXhz98ouKORgyboiNLomjaVszI4ZnBldPZnYeyvnDTk0fYODEsLop0b6fOD3VJtvQCaMz_gOzrd3jk6SJ2R1QHR9jLl4idXKG8u2GwlFd29tDsyUvssqWoYTUaI6qfCs1UIq84CXb6nyYUTOgtR9q-InqCMHWMkvjGmLs0BKqppjZ7u3ah50ITXQIVNekgWDBWt00Yj2LWFLFcZUTTZ7aHhc43GO0m-95Lr4CVccaDrcFhhVgiJ68r4aggMDKr19QQ2Vdebe0viOiuVye-bZzBal87s7YFqxoc1orTxXKqoAODA&csui=3&ved=2ahUKEwjxwaP4kb2RAxWhGRAIHdDsF-gQgK4QegQIARAE)) из распределенных приложений, который помогает разработчикам наблюдать за их поведением и производительностью без привязки к конкретному поставщику мониторинга. Он предоставляет унифицированный способ инструментирования кода, сбора данных и отправки их в разные системы (например, [Prometheus](https://www.google.com/search?client=opera&q=Prometheus&sourceid=opera&ie=UTF-8&oe=UTF-8&mstk=AUtExfDQtqWOBJ1es91rxVlZXhz98ouKORgyboiNLomjaVszI4ZnBldPZnYeyvnDTk0fYODEsLop0b6fOD3VJtvQCaMz_gOzrd3jk6SJ2R1QHR9jLl4idXKG8u2GwlFd29tDsyUvssqWoYTUaI6qfCs1UIq84CXb6nyYUTOgtR9q-InqCMHWMkvjGmLs0BKqppjZ7u3ah50ITXQIVNekgWDBWt00Yj2LWFLFcZUTTZ7aHhc43GO0m-95Lr4CVccaDrcFhhVgiJ68r4aggMDKr19QQ2Vdebe0viOiuVye-bZzBal87s7YFqxoc1orTxXKqoAODA&csui=3&ved=2ahUKEwjxwaP4kb2RAxWhGRAIHdDsF-gQgK4QegQIARAF), [Jaeger](https://www.google.com/search?client=opera&q=Jaeger&sourceid=opera&ie=UTF-8&oe=UTF-8&mstk=AUtExfDQtqWOBJ1es91rxVlZXhz98ouKORgyboiNLomjaVszI4ZnBldPZnYeyvnDTk0fYODEsLop0b6fOD3VJtvQCaMz_gOzrd3jk6SJ2R1QHR9jLl4idXKG8u2GwlFd29tDsyUvssqWoYTUaI6qfCs1UIq84CXb6nyYUTOgtR9q-InqCMHWMkvjGmLs0BKqppjZ7u3ah50ITXQIVNekgWDBWt00Yj2LWFLFcZUTTZ7aHhc43GO0m-95Lr4CVccaDrcFhhVgiJ68r4aggMDKr19QQ2Vdebe0viOiuVye-bZzBal87s7YFqxoc1orTxXKqoAODA&csui=3&ved=2ahUKEwjxwaP4kb2RAxWhGRAIHdDsF-gQgK4QegQIARAG), [Datadog](https://www.google.com/search?client=opera&q=Datadog&sourceid=opera&ie=UTF-8&oe=UTF-8&mstk=AUtExfDQtqWOBJ1es91rxVlZXhz98ouKORgyboiNLomjaVszI4ZnBldPZnYeyvnDTk0fYODEsLop0b6fOD3VJtvQCaMz_gOzrd3jk6SJ2R1QHR9jLl4idXKG8u2GwlFd29tDsyUvssqWoYTUaI6qfCs1UIq84CXb6nyYUTOgtR9q-InqCMHWMkvjGmLs0BKqppjZ7u3ah50ITXQIVNekgWDBWt00Yj2LWFLFcZUTTZ7aHhc43GO0m-95Lr4CVccaDrcFhhVgiJ68r4aggMDKr19QQ2Vdebe0viOiuVye-bZzBal87s7YFqxoc1orTxXKqoAODA&csui=3&ved=2ahUKEwjxwaP4kb2RAxWhGRAIHdDsF-gQgK4QegQIARAH)) через единый протокол (OTLP), что облегчает переход и обеспечивает прозрачность в сложных микросервисных архитектурах. 

![image.png](image%20706.png)

OpenTelemetry состоит из трёх основных компонентов:

1. **API и SDK** — библиотеки для различных языков (Go, Python, Node.js, Java и др.), через которые приложения отправляют данные.
2. **Collector** — агент или сервис, который принимает данные от приложений, обрабатывает их и экспортирует в нужную систему (например, Prometheus, Jaeger, Grafana, Zipkin).
3. **Протокол OTLP (OpenTelemetry Protocol)** — формат передачи данных между SDK и Collector.