# 8. Server Security

Категория: Web & Networks
Статус: Готово

## Hardened server (Защищенный сервер)

Процесс повышения надежности серверов снижает вероятность атак на ваш бизнес и помогает вам защититься от программ-вымогателей, вредоносных программ и других киберугроз. Вы можете следовать этому процессу, чтобы защитить все точки входа от кибератак, устранить слабые места в системе кибербезопасности и оптимизировать свою систему безопасности.

С помощью повышения безопасности ваш бизнес может устранить векторы киберпреступных атак и ненужные серверные процессы.

Например, ваша компания может "заблокировать" доступ к определенным системным приложениям, портам или учетным записям пользователей. Это устраняет потенциальные возможности, которые киберпреступник может использовать для атаки на вашу компанию. Защищайте себя от кибератак, устраняйте слабые места в системе кибербезопасности и оптимизируйте свою систему безопасности.

Зона атаки - это любые точки входа, которые киберпреступник может использовать для проникновения на серверы вашей компании. Она включает в себя сетевые интерфейсы, программное обеспечение и приложения. Зона атаки может увеличиваться или уменьшаться в зависимости от того, как вы управляете своими системами.

Если ваша компания добавляет новые системы, это увеличивает вероятность атаки и дает киберпреступникам больше потенциальных точек входа для атаки. Или вы можете ограничить количество используемых вами систем и свести к минимуму вероятность атаки.

Существует множество мер, которые вы можете использовать для защиты своих серверов, включая:

- Регулярное внесение исправлений и обновление операционных систем
- Обновление программного обеспечения сторонних производителей, необходимого для работы ваших серверов в соответствии с отраслевыми стандартами безопасности
- Требовать пользователей создавать и поддерживать сложные пароли, состоящие из букв, цифр и специальных символов, и часто обновлять эти пароли
- Блокировать учетную запись после определенного количества неудачных попыток входа в систему
- Отключение определенных USB-портов при загрузке сервера
- Использование многофакторной аутентификации (MFA)
- Использование шифрования AES или самошифрованных дисков для сокрытия и защиты критически важной для бизнеса информации
- Использование антивирусной защиты, брандмауэра и других передовых решений для обеспечения безопасности

### Server Hardering Checklist

Факторы, которые необходимо учитывать, чтобы защитить сервер:

- Учетные записи пользователей и логины для входа в систему
- Серверные компоненты и подсистемы
- Обновления программного обеспечения и приложений и уязвимости
- Часы работы сервера и временные метки
- Сети и брандмауэры
- Безопасность удаленного доступа
- Управление журналами

### Рекомендации по защите серверов

1. Зашифруйте свои данные
Используйте технологии шифрования для всех ваших данных. Защитите эту информацию с помощью паролей, ключей и сертификатов.
2. Сократите количество программного обеспечения и приложений до минимума
Подумайте, действительно ли вам нужно программное обеспечение или приложения, прежде чем загружать их. Если ответ положительный, загрузите программное обеспечение или приложение и поддерживайте его в актуальном состоянии.
3. Настройте серверы для различных сетевых служб
Запустите каждую сетевую службу на отдельном сервере. Таким образом, в случае взлома сервера будет затронута только одна сетевая служба.
4. Отслеживайте свои настройки
Создайте список конфигураций вашего сервера. В вашем списке должна быть документация о каждой конфигурации, а также о любых изменениях в ней. Кроме того, проводите тестирование конфигурации и отслеживайте его результаты. Регулярно просматривайте и обновляйте список конфигураций вашего сервера.
5. Проводите оценку рисков
Разработайте план управления рисками и проведите тестирование, чтобы понять текущее состояние безопасности вашего сервера. Проведите оценку рисков, чтобы выявить пробелы в безопасности и найти наилучшие способы их устранения. Эту оценку может выполнить ваша внутренняя команда ИТ-безопасности или вы можете сотрудничать со сторонним поставщиком средств безопасности.
6. Применяйте надежные пароли
Убедитесь, что ваши сотрудники соблюдают политику управления паролями вашей компании. Не разрешайте сотрудникам использовать общие пароли, которые киберпреступники могут легко угадать. Сотрудники должны устанавливать сложные пароли и никогда ни с кем ими не делиться. Им также следует избегать хранения паролей на рабочих местах или в любых общественных местах.
7. Расскажите своим сотрудникам об усилении защиты серверов
Расскажите своим сотрудникам о том, как это работает и почему это важно. Регулярно просматривайте свои учебные материалы по усилению защиты серверов и обновляйте их по мере необходимости.
8. Продолжайте искать пути улучшения
Встретьтесь с членами вашей команды ИТ-безопасности, руководителями высшего звена и другими бизнес-профессионалами, чтобы обсудить вопросы кибербезопасности. Вместе сотрудники вашего предприятия смогут найти способы защиты от всех типов кибератак и повысить уровень вашей безопасности.

## Алгоритмы шифрования

### MD5

MD5 (Message Digest Algorithm 5) — это **криптографический алгоритм, преобразующий данные любого размера в уникальный 128-битный «отпечаток» (хеш) фиксированной длины (32 шестнадцатеричных символа), используемый для проверки целостности файлов, но из-за обнаруженных критических уязвимостей (коллизий, когда разные данные дают одинаковый хеш) он больше не считается безопасным для криптографических задач, таких как хеширование паролей, и его следует заменить на более современные алгоритмы, такие как SHA-256**. 

**Как работает MD5 (упрощенно)**

1. **Подготовка данных**: Входные данные дополняются битами до размера, кратного 512 битам, и к ним добавляется их исходная длина.
2. **Инициализация**: Используется 128-битный буфер, который инициализируется четырьмя 32-битными значениями.
3. **Циклическая обработка**: Данные обрабатываются блоками по 512 бит в 4 раундах. Каждый раунд выполняет сложные математические операции (логические функции, сложение, вращение) над данными и буфером, используя константы.
4. **Результат**: После всех операций итеративно обрабатываются все блоки, и финальные значения буфера преобразуются в 128-битный хеш.

**Почему MD5 небезопасен**

- **Коллизии**: Главная проблема — возможность найти две разные входные строки, которые дают одинаковый MD5-хеш. Злоумышленники могут подменить файл или данные, сохраняя при этом старый хеш.
- **Неустойчивость к атакам**: Существуют практические методы быстрого поиска коллизий.
- **Уязвимость для паролей**: Легкость нахождения коллизий и возможность использования "радужных таблиц" (предварительно вычисленных хешей) делают его непригодным для хранения паролей, даже с солью (дополнительными данными).

**Применение сегодня**

- **Для безопасности**: Не рекомендуется для хеширования паролей, цифровых подписей, сертификатов. Следует использовать [**bcrypt**](https://www.google.com/url?sa=i&source=web&rct=j&url=https://www.dev-notes.ru/articles/php/security-tip-stop-using-md5-and-sha-1/&ved=2ahUKEwji1vH_6bWRAxWiTVUIHXbvOs0Qy_kOegQICRAB&opi=89978449&cd&psig=AOvVaw1ATvirc4aHkAGc65t3LeSf&ust=1765552571010000) или [**SHA-256/SHA-3**](https://www.google.com/url?sa=i&source=web&rct=j&url=https://mojoauth.com.en2ru.search.translate.goog/compare-hashing-algorithms/md5-vs-sha-256/&ved=2ahUKEwji1vH_6bWRAxWiTVUIHXbvOs0Qy_kOegQICRAC&opi=89978449&cd&psig=AOvVaw1ATvirc4aHkAGc65t3LeSf&ust=1765552571010000).
- **Для некриптографических задач**: Все еще используется для проверки целостности файлов (контрольных сумм), кэширования, распределения данных, где надежность криптографического уровня не является критичной, а важна скорость.

### SHA

SHA (Secure Hash Algorithm) — это **семейство криптографических хэш-функций, которое преобразует данные любого размера в уникальный «отпечаток» (хэш) фиксированной длины**; он работает путем необратимого математического преобразования, где даже минимальное изменение в исходном тексте полностью меняет хэш-значение, и используется для проверки целостности данных, цифровых подписей и в блокчейне (например, Bitcoin), а также для безопасного хранения паролей. 

**Как это работает**

1. **Ввод данных**: SHA-алгоритм принимает на вход данные любого размера (текст, файл и т.д.).
2. **Хэширование (Преобразование)**: Данные проходят через серию сложных математических операций (сжатие, перемешивание), которые необратимо их меняют.
3. **Вывод хэша (Отпечатка)**: На выходе получается строка символов фиксированной длины (например, 256 бит для SHA-256), которая и является хэшем.
4. **Ключевые свойства**:
    - **Однонаправленность**: По хэшу невозможно восстановить исходные данные.
    - **Уникальность**: Разные данные дают разные хэши, а изменение одного символа в исходнике полностью меняет хэш (эффект лавины).
    - **Устойчивость к коллизиям**: Крайне сложно найти два разных файла, которые дадут один и тот же хэш.

**Где используется**

- **Проверка целостности**: Для подтверждения, что файл не был поврежден или подделан после скачивания.
- **Блокчейн и криптовалюты**: Bitcoin использует двойной [SHA-256](https://www.google.com/search?q=SHA-256&client=opera&sca_esv=b338e4d9bf6df8e5&sxsrf=AE3TifOuJ9zSUcDo0tI2ntD8s2YtlXepyQ%3A1765466433482&ei=QeE6aZaSHY2twPAP_dPt4As&ved=2ahUKEwikmeb-6rWRAxV3U1UIHWI_DPIQgK4QegQIBhAC&uact=5&oq=%D0%A7%D1%82%D0%BE+%D1%82%D0%B0%D0%BA%D0%BE%D0%B5+SHA%2C+%D0%BA%D0%B0%D0%BA+%D0%BE%D0%BD+%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82+%D0%B8+%D0%B3%D0%B4%D0%B5+%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D0%B5%D1%82%D1%81%D1%8F&gs_lp=Egxnd3Mtd2l6LXNlcnAiVtCn0YLQviDRgtCw0LrQvtC1IFNIQSwg0LrQsNC6INC-0L0g0YDQsNCx0L7RgtCw0LXRgiDQuCDQs9C00LUg0LjRgdC_0L7Qu9GM0LfRg9C10YLRgdGPMgUQABjvBTIFEAAY7wUyCBAAGIAEGKIESNAGUABYzAFwAHgBkAEAmAFqoAG-AaoBAzEuMbgBA8gBAPgBAZgCAqACxgHCAgYQIRgKGCqYAwCSBwMxLjGgB-EHsgcDMS4xuAfGAcIHAzAuMsgHBIAIAA&sclient=gws-wiz-serp&mstk=AUtExfAw9lM3H3-sVsmXUPpGmpDD2tmisjpLrBsVaupaDJPmD2dgQeVfuIk3D3kW7WVwiY5-sOaAZJe8QxZp-es7I571FasqARfsbG2XSoBwykbkZy5zKfVTF9mjw9CKkFtFO8iyFkFA5ytCIGQl_6jJiAEfWLLUQC7i8-6n3DiCf-C2sm59szq8116yG6uU3t_GY336s2N2w6V9dT2a1fU_yQ1izfvZCv0AVz15Pqn5kFx823aOECwI9cUkwXipOTCdS7ZrkB90eBaD7NbWlbSitNp9nNyTpIMj7pbSC6rtKBH0Zw&csui=3) для подтверждения транзакций и создания блоков.
- **Цифровые подписи**: Для подтверждения подлинности и целостности документов и программного обеспечения.
- **Хэширование паролей**: Вместо хранения паролей в открытом виде, хранят их хэши, что защищает их при утечке.
- **SSL/TLS сертификаты**: Для аутентификации веб-сайтов.

**Примеры версий**

- **SHA-1**: Более старая, менее безопасная версия (160 бит).
- **SHA-2 (SHA-256, SHA-512)**: Семейство более современных и надежных функций, где цифра – это длина хэша в битах (256 или 512), [**SHA-256**](https://www.google.com/url?sa=i&source=web&rct=j&url=https://www.ssldragon.com/ru/blog/sha-256-algorithm/&ved=2ahUKEwikmeb-6rWRAxV3U1UIHWI_DPIQy_kOegQICBAC&opi=89978449&cd&psig=AOvVaw0t5oBwlBir5mkSgqZBhAGj&ust=1765552837160000) особенно популярно.
- **SHA-3**: Последний стандарт с другой архитектурой ("губка"), предлагающий еще более высокий уровень безопасности.

### scrypt

Scrypt — это криптографический алгоритм создания ключей из паролей, который требует много памяти (RAM) и времени для вычислений, делая его устойчивым к атакам перебора и ASIC-майнерам, используемый для хеширования паролей и в майнинге криптовалют (Litecoin, Dogecoin) для защиты сети и поддержки децентрализации. Он работает, выполняя ресурсоёмкие и последовательные преобразования данных, которые сложно ускорить специализированным железом, что защищает от атак «грубой силой».

**Как работает Scrypt**

- [**Ресурсоёмкость**](https://www.google.com/search?q=%D0%A0%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%BE%D1%91%D0%BC%D0%BA%D0%BE%D1%81%D1%82%D1%8C&client=opera&sca_esv=b338e4d9bf6df8e5&sxsrf=AE3TifOAOle193Lp-p1lwbAggfU1mHC9ZA%3A1765466436908&ei=ROE6aeOcN4GRwPAPmMSH6Qc&ved=2ahUKEwjs9NK467WRAxXeFxAIHeT7GBEQgK4QegQIAxAB&uact=5&oq=%D0%A7%D1%82%D0%BE+%D1%82%D0%B0%D0%BA%D0%BE%D0%B5+scrypt%2C+%D0%BA%D0%B0%D0%BA+%D0%BE%D0%BD+%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82+%D0%B8+%D0%B3%D0%B4%D0%B5+%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D0%B5%D1%82%D1%81%D1%8F&gs_lp=Egxnd3Mtd2l6LXNlcnAiWdCn0YLQviDRgtCw0LrQvtC1IHNjcnlwdCwg0LrQsNC6INC-0L0g0YDQsNCx0L7RgtCw0LXRgiDQuCDQs9C00LUg0LjRgdC_0L7Qu9GM0LfRg9C10YLRgdGPMggQABiABBiiBDIFEAAY7wUyBRAAGO8FMgUQABjvBUiGCVDgA1jgA3ABeAGQAQCYAWCgAWCqAQExuAEDyAEA-AEC-AEBmAICoAJowgIKEAAYsAMY1gQYR5gDAIgGAZAGCJIHATKgB_UCsgcBMbgHY8IHBTAuMS4xyAcGgAgA&sclient=gws-wiz-serp&mstk=AUtExfAfgBMxfS1ipAnjfA8LKw0Omwd1X5h1I9WCEM-F68o6sCQKLOIpkWrGXvOE2qR2Mdy3wM5fgNJT1QkdNXvtwic3LSE0S8PJDGVj61EKXz2mZkW8Fcim_rp-JZZMYIP5JY8qDlzWYjkXfD5K_UrYCxoCiR50dVTiLGC_HnpA_h2-LanYlJH4xonGOy7mHRd4JRGnmal0FJqDS7rpLSCIsNh1sQEwxulFM5MghPue3szbqlde-yFQH6MuhD9cI7H1Fb3ZV58yEjI1Gmgq3nFJ6s-JCeEQ2pjQDJ8CU7CXZpgYqg&csui=3): В отличие от SHA-256, Scrypt использует не только процессорное время, но и большой объём оперативной памяти (RAM).
- [**Параметры**](https://www.google.com/search?q=%D0%9F%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%D1%8B&client=opera&sca_esv=b338e4d9bf6df8e5&sxsrf=AE3TifOAOle193Lp-p1lwbAggfU1mHC9ZA%3A1765466436908&ei=ROE6aeOcN4GRwPAPmMSH6Qc&ved=2ahUKEwjs9NK467WRAxXeFxAIHeT7GBEQgK4QegQIAxAD&uact=5&oq=%D0%A7%D1%82%D0%BE+%D1%82%D0%B0%D0%BA%D0%BE%D0%B5+scrypt%2C+%D0%BA%D0%B0%D0%BA+%D0%BE%D0%BD+%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82+%D0%B8+%D0%B3%D0%B4%D0%B5+%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D0%B5%D1%82%D1%81%D1%8F&gs_lp=Egxnd3Mtd2l6LXNlcnAiWdCn0YLQviDRgtCw0LrQvtC1IHNjcnlwdCwg0LrQsNC6INC-0L0g0YDQsNCx0L7RgtCw0LXRgiDQuCDQs9C00LUg0LjRgdC_0L7Qu9GM0LfRg9C10YLRgdGPMggQABiABBiiBDIFEAAY7wUyBRAAGO8FMgUQABjvBUiGCVDgA1jgA3ABeAGQAQCYAWCgAWCqAQExuAEDyAEA-AEC-AEBmAICoAJowgIKEAAYsAMY1gQYR5gDAIgGAZAGCJIHATKgB_UCsgcBMbgHY8IHBTAuMS4xyAcGgAgA&sclient=gws-wiz-serp&mstk=AUtExfAfgBMxfS1ipAnjfA8LKw0Omwd1X5h1I9WCEM-F68o6sCQKLOIpkWrGXvOE2qR2Mdy3wM5fgNJT1QkdNXvtwic3LSE0S8PJDGVj61EKXz2mZkW8Fcim_rp-JZZMYIP5JY8qDlzWYjkXfD5K_UrYCxoCiR50dVTiLGC_HnpA_h2-LanYlJH4xonGOy7mHRd4JRGnmal0FJqDS7rpLSCIsNh1sQEwxulFM5MghPue3szbqlde-yFQH6MuhD9cI7H1Fb3ZV58yEjI1Gmgq3nFJ6s-JCeEQ2pjQDJ8CU7CXZpgYqg&csui=3): Имеет настраиваемые параметры (N, r, p), которые определяют уровень потребления памяти и вычислений, позволяя адаптировать сложность.
- [**Преобразования**](https://www.google.com/search?q=%D0%9F%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F&client=opera&sca_esv=b338e4d9bf6df8e5&sxsrf=AE3TifOAOle193Lp-p1lwbAggfU1mHC9ZA%3A1765466436908&ei=ROE6aeOcN4GRwPAPmMSH6Qc&ved=2ahUKEwjs9NK467WRAxXeFxAIHeT7GBEQgK4QegQIAxAF&uact=5&oq=%D0%A7%D1%82%D0%BE+%D1%82%D0%B0%D0%BA%D0%BE%D0%B5+scrypt%2C+%D0%BA%D0%B0%D0%BA+%D0%BE%D0%BD+%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82+%D0%B8+%D0%B3%D0%B4%D0%B5+%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D0%B5%D1%82%D1%81%D1%8F&gs_lp=Egxnd3Mtd2l6LXNlcnAiWdCn0YLQviDRgtCw0LrQvtC1IHNjcnlwdCwg0LrQsNC6INC-0L0g0YDQsNCx0L7RgtCw0LXRgiDQuCDQs9C00LUg0LjRgdC_0L7Qu9GM0LfRg9C10YLRgdGPMggQABiABBiiBDIFEAAY7wUyBRAAGO8FMgUQABjvBUiGCVDgA1jgA3ABeAGQAQCYAWCgAWCqAQExuAEDyAEA-AEC-AEBmAICoAJowgIKEAAYsAMY1gQYR5gDAIgGAZAGCJIHATKgB_UCsgcBMbgHY8IHBTAuMS4xyAcGgAgA&sclient=gws-wiz-serp&mstk=AUtExfAfgBMxfS1ipAnjfA8LKw0Omwd1X5h1I9WCEM-F68o6sCQKLOIpkWrGXvOE2qR2Mdy3wM5fgNJT1QkdNXvtwic3LSE0S8PJDGVj61EKXz2mZkW8Fcim_rp-JZZMYIP5JY8qDlzWYjkXfD5K_UrYCxoCiR50dVTiLGC_HnpA_h2-LanYlJH4xonGOy7mHRd4JRGnmal0FJqDS7rpLSCIsNh1sQEwxulFM5MghPue3szbqlde-yFQH6MuhD9cI7H1Fb3ZV58yEjI1Gmgq3nFJ6s-JCeEQ2pjQDJ8CU7CXZpgYqg&csui=3): Комбинирует соль (случайные данные), псевдослучайные преобразования и повторные вычисления для создания надежного хеша, который сложно взломать.
- [**Защита**](https://www.google.com/search?q=%D0%97%D0%B0%D1%89%D0%B8%D1%82%D0%B0&client=opera&sca_esv=b338e4d9bf6df8e5&sxsrf=AE3TifOAOle193Lp-p1lwbAggfU1mHC9ZA%3A1765466436908&ei=ROE6aeOcN4GRwPAPmMSH6Qc&ved=2ahUKEwjs9NK467WRAxXeFxAIHeT7GBEQgK4QegQIAxAH&uact=5&oq=%D0%A7%D1%82%D0%BE+%D1%82%D0%B0%D0%BA%D0%BE%D0%B5+scrypt%2C+%D0%BA%D0%B0%D0%BA+%D0%BE%D0%BD+%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82+%D0%B8+%D0%B3%D0%B4%D0%B5+%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D0%B5%D1%82%D1%81%D1%8F&gs_lp=Egxnd3Mtd2l6LXNlcnAiWdCn0YLQviDRgtCw0LrQvtC1IHNjcnlwdCwg0LrQsNC6INC-0L0g0YDQsNCx0L7RgtCw0LXRgiDQuCDQs9C00LUg0LjRgdC_0L7Qu9GM0LfRg9C10YLRgdGPMggQABiABBiiBDIFEAAY7wUyBRAAGO8FMgUQABjvBUiGCVDgA1jgA3ABeAGQAQCYAWCgAWCqAQExuAEDyAEA-AEC-AEBmAICoAJowgIKEAAYsAMY1gQYR5gDAIgGAZAGCJIHATKgB_UCsgcBMbgHY8IHBTAuMS4xyAcGgAgA&sclient=gws-wiz-serp&mstk=AUtExfAfgBMxfS1ipAnjfA8LKw0Omwd1X5h1I9WCEM-F68o6sCQKLOIpkWrGXvOE2qR2Mdy3wM5fgNJT1QkdNXvtwic3LSE0S8PJDGVj61EKXz2mZkW8Fcim_rp-JZZMYIP5JY8qDlzWYjkXfD5K_UrYCxoCiR50dVTiLGC_HnpA_h2-LanYlJH4xonGOy7mHRd4JRGnmal0FJqDS7rpLSCIsNh1sQEwxulFM5MghPue3szbqlde-yFQH6MuhD9cI7H1Fb3ZV58yEjI1Gmgq3nFJ6s-JCeEQ2pjQDJ8CU7CXZpgYqg&csui=3): Высокая потребность в памяти затрудняет создание эффективных ASIC-майнеров, которые оптимизированы для скорости и неэффективны в работе с памятью.

**Где используется Scrypt**

- [**Криптовалюты**](https://www.google.com/search?q=%D0%9A%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D0%B2%D0%B0%D0%BB%D1%8E%D1%82%D1%8B&client=opera&sca_esv=b338e4d9bf6df8e5&sxsrf=AE3TifOAOle193Lp-p1lwbAggfU1mHC9ZA%3A1765466436908&ei=ROE6aeOcN4GRwPAPmMSH6Qc&ved=2ahUKEwjs9NK467WRAxXeFxAIHeT7GBEQgK4QegQIBRAB&uact=5&oq=%D0%A7%D1%82%D0%BE+%D1%82%D0%B0%D0%BA%D0%BE%D0%B5+scrypt%2C+%D0%BA%D0%B0%D0%BA+%D0%BE%D0%BD+%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82+%D0%B8+%D0%B3%D0%B4%D0%B5+%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D0%B5%D1%82%D1%81%D1%8F&gs_lp=Egxnd3Mtd2l6LXNlcnAiWdCn0YLQviDRgtCw0LrQvtC1IHNjcnlwdCwg0LrQsNC6INC-0L0g0YDQsNCx0L7RgtCw0LXRgiDQuCDQs9C00LUg0LjRgdC_0L7Qu9GM0LfRg9C10YLRgdGPMggQABiABBiiBDIFEAAY7wUyBRAAGO8FMgUQABjvBUiGCVDgA1jgA3ABeAGQAQCYAWCgAWCqAQExuAEDyAEA-AEC-AEBmAICoAJowgIKEAAYsAMY1gQYR5gDAIgGAZAGCJIHATKgB_UCsgcBMbgHY8IHBTAuMS4xyAcGgAgA&sclient=gws-wiz-serp&mstk=AUtExfAfgBMxfS1ipAnjfA8LKw0Omwd1X5h1I9WCEM-F68o6sCQKLOIpkWrGXvOE2qR2Mdy3wM5fgNJT1QkdNXvtwic3LSE0S8PJDGVj61EKXz2mZkW8Fcim_rp-JZZMYIP5JY8qDlzWYjkXfD5K_UrYCxoCiR50dVTiLGC_HnpA_h2-LanYlJH4xonGOy7mHRd4JRGnmal0FJqDS7rpLSCIsNh1sQEwxulFM5MghPue3szbqlde-yFQH6MuhD9cI7H1Fb3ZV58yEjI1Gmgq3nFJ6s-JCeEQ2pjQDJ8CU7CXZpgYqg&csui=3): Самое известное применение — майнинг альткоинов, таких как [**Litecoin (LTC)**](https://www.google.com/url?sa=i&source=web&rct=j&url=https://www.bitget.com/ru/wiki/1152594&ved=2ahUKEwjs9NK467WRAxXeFxAIHeT7GBEQy_kOegQIBRAC&opi=89978449&cd&psig=AOvVaw2PjG2UN21q-hBg4sCa7zVl&ust=1765552958479000), Dogecoin (DOGE), а также других монет для поддержания децентрализации.
- [**Хеширование паролей**](https://www.google.com/search?q=%D0%A5%D0%B5%D1%88%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5+%D0%BF%D0%B0%D1%80%D0%BE%D0%BB%D0%B5%D0%B9&client=opera&sca_esv=b338e4d9bf6df8e5&sxsrf=AE3TifOAOle193Lp-p1lwbAggfU1mHC9ZA%3A1765466436908&ei=ROE6aeOcN4GRwPAPmMSH6Qc&ved=2ahUKEwjs9NK467WRAxXeFxAIHeT7GBEQgK4QegQIBRAE&uact=5&oq=%D0%A7%D1%82%D0%BE+%D1%82%D0%B0%D0%BA%D0%BE%D0%B5+scrypt%2C+%D0%BA%D0%B0%D0%BA+%D0%BE%D0%BD+%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82+%D0%B8+%D0%B3%D0%B4%D0%B5+%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D0%B5%D1%82%D1%81%D1%8F&gs_lp=Egxnd3Mtd2l6LXNlcnAiWdCn0YLQviDRgtCw0LrQvtC1IHNjcnlwdCwg0LrQsNC6INC-0L0g0YDQsNCx0L7RgtCw0LXRgiDQuCDQs9C00LUg0LjRgdC_0L7Qu9GM0LfRg9C10YLRgdGPMggQABiABBiiBDIFEAAY7wUyBRAAGO8FMgUQABjvBUiGCVDgA1jgA3ABeAGQAQCYAWCgAWCqAQExuAEDyAEA-AEC-AEBmAICoAJowgIKEAAYsAMY1gQYR5gDAIgGAZAGCJIHATKgB_UCsgcBMbgHY8IHBTAuMS4xyAcGgAgA&sclient=gws-wiz-serp&mstk=AUtExfAfgBMxfS1ipAnjfA8LKw0Omwd1X5h1I9WCEM-F68o6sCQKLOIpkWrGXvOE2qR2Mdy3wM5fgNJT1QkdNXvtwic3LSE0S8PJDGVj61EKXz2mZkW8Fcim_rp-JZZMYIP5JY8qDlzWYjkXfD5K_UrYCxoCiR50dVTiLGC_HnpA_h2-LanYlJH4xonGOy7mHRd4JRGnmal0FJqDS7rpLSCIsNh1sQEwxulFM5MghPue3szbqlde-yFQH6MuhD9cI7H1Fb3ZV58yEjI1Gmgq3nFJ6s-JCeEQ2pjQDJ8CU7CXZpgYqg&csui=3): Используется для безопасного хранения паролей в системах резервного копирования (например, Tarsnap) и других приложениях, где требуется защита от атак перебора.

### bcrypt

Bcrypt — это **адаптивная функция хеширования паролей, основанная на алгоритме шифра Blowfish, которая медленно и ресурсоемко преобразует пароли в нечитаемые строки (хеши), защищая их от атак перебора (Brute-force) и радужных таблиц, используя «соль» (случайные данные) для уникальности, и широко применяется в веб-разработке для безопасного хранения паролей в системах аутентификации**.

**Как работает Bcrypt**

1. **Соль (Salt)**: К паролю добавляется уникальная, случайная строка (соль). Это гарантирует, что даже одинаковые пароли разных пользователей будут иметь разные хеши, что предотвращает использование радужных таблиц.
2. **Итерации (Work Factor/Cost Factor)**: Процесс хеширования повторяется многократно (сотни или тысячи раз), используя коэффициент сложности (`cost`). Это намеренно замедляет процесс, делая его дорогим для злоумышленников, даже если у них есть мощные GPU.
3. **Хеширование на основе Blowfish**: Используется криптографически стойкий алгоритм Blowfish для выполнения самих хеширований.
4. **Встроенная соль**: Соль "встраивается" в итоговый хеш, что упрощает проверку, так как библиотеке не нужно хранить соль отдельно.
5. **Проверка**: При входе пользователя его пароль с уже встроенной солью хешируется и сравнивается с сохраненным хешем; если совпадают, доступ разрешен.

**Где используется**

- **Аутентификация пользователей**: Основное применение – хранение паролей в базах данных веб-приложений, форумов, социальных сетей.
- **Системы управления доступом**: В Spring Security, OpenBSD и других системах, где важна надежная защита учетных данных.
- **Различные языки программирования**: Доступны реализации для C, C++, C#, Java, JavaScript (Node.js), Python, PHP и других.

Bcrypt является лучшей, чем устаревшие методы (MD5, SHA-1), и рекомендован для безопасной реализации систем входа и регистрации.

**Радужная таблица** — это особый вид предварительно вычисленной таблицы, созданной для быстрого **взлома хэшей** (преобразования зашифрованного пароля обратно в исходный текст). Это компромисс между скоростью и объемом памяти, более эффективный, чем простые таблицы перебора.