# **ОБЛАЧНОЕ ХРАНИЛИЩЕ MyCloud**
## Серверная часть приложения (Backend) <br>(разработан с использованием Django)

### 1. *Структура проекта*

`d_backend` - корневая папка бэкенда<br>
&nbsp;&nbsp;&nbsp;&nbsp;`backend/` - папка с основной конфигурацией Django<br> 
&nbsp;&nbsp;&nbsp;&nbsp;`my_server/` - папка с кодом приложения<br> 
&nbsp;&nbsp;&nbsp;&nbsp;`media/` – папка с загруженными файлами пользователей приложения<br> 

`manage.py` - файл с точкой входа управления Django-приложением<br>
`requirements.txt` – файл со списком зависимостей Django<br> 
`README.md` - файл с инструкцией по установке и развертыванию<br>
`information.log` – log-файл (появится в после начала работы приложения)<br> 

### 2. *Развертывание проекта на локальном компьютере*

1. Если на компьютере не установлен PostgreSQL, установить его согласно [инструкции](https://embed.new.video/uyjUq9B3qYo6BbbkzG71Ny). 

2. Клонировать репозиторий:\
   `git clone https://github.com/ART20230129/d_backend`

3. Открыть папку `d_backend` в любой IDE и запустить встроенный терминал

4. Перейти в папку `backend/`   
   ```bash
   cd backend
   ```
5. Создать виртуальное окружение
   ```bash
   python -m venv venv
   ```
6. Активировать виртуальное окружение   
   ```bash
   venv/Scripts/activate.bat
   ```
7. Установить зависимости
   ```bash
   pip install -r requirements.txt 
   ```
8. Сгенерировать в терминале секретный ключ для Django   
   ```bash
   python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   скопировать сгенерированный секретный ключ

9. В папке `backend/` создать файл `.env` в соответствии с шаблоном:  
   ```plaintext
   SECRET_KEY=вставить сгенерированный в п. 7 секретный ключ
   DB_USER=имя пользователя базы данных PostgreSQL
   DB_PASSWORD=пароль пользователя данных PostgreSQL
   DB_NAME=имя планируемой к использованию базы данных
   ```

10. Создаем базу данных (DB_USER и DB_NAME взять из файла `.env` (см. п. 9))    
    ```bash
    createdb -U DB_USER DB_NAME
    ```

11. Выполнить миграции    
    ```bash
    python manage.py migrate
    ```

12. Создать Суперпользователя (на Административной странице он не отражается)    
    ```bash
    python manage.py createsuperuser
    ```

13. Запустить сервер    
    ```
    python manage.py runserver
    ```

По адресу `http://127.0.0.1:8000/admin/` будет доступно страница: Django administration (админка Django).<br> 
Суперпользователь мовжет входить как в Django administration, так и в Административный интерфейс после входа (на Административной странице он не отражается).
   
### 3. *Развертывание проекта на серверу*

1. Генерируем (при необходимости) ssh-ключ   
   ```bash
   ssh-keygen
   ```
2. Скопировать публичный ssh-ключ, вызываемый командой   
   ```bash
   cat ~/.ssh/id_rsa.pub
   ```
3. На сайте провайдера создать облачный сервер (на примере [reg.ru](https://cloud.reg.ru)):
   * создать сервер
   * образ Ubuntu
   * выбрать необходимый тарифный план
   * вставить ранее (см. п. 2) публичный ключ (начинается с ssh-rsa и до конца текста)
   * указать название используемого ssh-ключа (как правило, название компьютера)
   * нажать кнопку "Добавить ssh-ключ"
   * нажать кнопку "Заказать сервер"
   * на электронную почту придет письмо с информацией по доступу к серверу
*** 
  
4. Запустить терминал и перейти в домашнюю директорию   
   ```bash
   cd ~
   ```
5. Подключаемся к серверу
   ```bash
   ssh root@<ip_адрес_сервера>
   ```
   Вводим пароль для доступа к серверу из письма, полученного на электронную почту

6. Создать нового пользователя   
   ```bash
   adduser <ИМЯ_ПОЛЬЗВАТЕЛЯ>
   ```
7. Добавляем созданного пользователя в группу sudo (для получения расширенных прав)   
   ```bash
   usermod <ИМЯ_ПОЛЬЗОВАТЕЛЯ> -aG sudo
   ```
8. Переключаемся на созданного пользователя   
   ```bash
   su <ИМЯ_ПОЛЬЗОВАТЕЛЯ>
   ```
9. Переходим в домашнюю директорию созданного пользователя
   ```bash
   cd ~
   ```
   **Примечание**
   В случае, если "выбросило" из сервера вернуться с помощью команды
   ```bash
   ssh <ИМЯ_ПОЛЬЗОВАТЕЛЯ>@<ip  адрес сервера>
---  
10. Проверяем наличие python
    ```bash
    python3 --version
    ```
    и Git
    ```bash
    git --version
    ```
11. Обновляем пакетный менеджер
    ```bash
    sudo apt update
    ```
12. Устанавливаем необходимые пакеты на сервере
    ```bash
    sudo apt install  python3-pip python3-venv postgresql nginx
    ```
13. Создаем базу данных (приводится пример для пользователя postgres)
   * зайти в postgres
      ```bash
      sudo su postgres
      ```
   * Через postgres зайти в psql
      ```bash
      psql
      ```
   * Задать пароль для пользователя postgres
      ```bash
      ALTER USER postgres WITH PASSWORD '<ПАРОЛЬ_ПОЛЬЗОВАТЕЛЯ>';
      ```
   * Создать базу данных для проекта
      ```bash
      CREATE DATABASE <ИМЯ_БАЗЫ_ДАННЫХ>;
      ```
   * Выйти из панели psql:
      ```bash
      \q
      ```
   * Выйти из postgres
      ```bash
      exit
      ```
---
14. Клонируем репозиторий с проектом
    ```bash
    git clone https://github.com/ART20230129/d_backend.git
    ```
15. Переходим в папку проекта
    ```bash
    cd backend
    ```
16. Создаем виртуальное окружение 
    ```bash
    python3 -m venv env
    ```
17. Активируем виртуальное окружение
    ```bash
    source env/bin/activate
    ```
18. Устанавливаем необходиме пакеты
    ```bash
    pip install -r requirements.txt
    ```
19. Создать файл .env с переменным окружением
    ```bash
    nano .env
    ```
20. Заполнить шаблон
    ```bash
    # можно сгенерировать на сайте https://djecrety.ir
    SECRET_KEY=*****************
    DEBUG=False
    # ALLOWED_HOSTS например через запятую: localhost,127.0.0.1,<ИМЯ ДОМЕНА ИЛИ IP АДРЕС СЕРВЕРА> или оставить `*` для всех
    ALLOWED_HOSTS=*
    DB_NAME=<ИМЯ_БАЗЫ_ДАННЫХ>
    DB_USER=postgres
    DB_PASSWORD=<ПАРОЛЬ_ПОЛЬЗОВАТЕЛЯ>
    DB_HOST=localhost
    DB_PORT=5432
    ```
    Внимание! Файл .env должен быть на одном уровне с файлом manage.py
21. Проверить, подключно ли виртуальное окружение и провести миграции
    ```bash
    python manage.py migrate
    ```
22. Запускаем сервер
    ```bash
    python manage.py runserver
    ```
23. Проверяем рабтоспособность в браузере, прописав в поисковой строке
    ```bash
    <ip_адрес_сервера>:8000
    ```
---   
24. Запускаем nginx
    ```bash
    sudo systemctl start nginx
    ```
24. Проверяем рабтоспособность nginx
    ```bash
    sudo systemctl status nginx
    ```
    В терминале должна появиться запись зеленым цветом Active: active (running)
    Если в браузере ввсести <ip_адрес_сервера>, то должен пояиться текст <strong>Welcome to nginx</strong>
25. Проверить, что включено виртуальное окружение, нахождение в папке проекта (где файл manage.py),
    проверить работу gunicorn
    ```bash
    gunicorn backend.wsgi --bind 0.0.0.0:8000
    ```
    Проверяем работоспособность в браузере (без стилей)
    ```bash
    <ip адрес сервера>:8000
    ```
26. Собираем весь статичный контент в папке (static) на сервере
    ```bash
    python manage.py collectstatic
    ```
27. Настраиваем gunicorn
    ```bash
    sudo nano /etc/systemd/system/gunicorn.service
    ```
    Описываем настройки gunicorn.service
    ```bash
    [Unit]
    Description=service for wsgi
    After=network.target

    [Service]
    User=<ИМЯ_ПОЛЬЗОВАТЕЛЯ>
    Group=www-data
    WorkingDirectory=/home/<ИМЯ_ПОЛЬЗОВАТЕЛЯ>/d_backend
    ExecStart=/home/<ИМЯ_ПОЛЬЗОВАТЕЛЯ>/d_backend/env/bin/gunicorn --access-logfile - --workers=3 \
                                 --bind unix:/home/stu<ИМЯ_ПОЛЬЗОВАТЕЛЯ>dent/d_backend/backend/project.sock \
                                 backend.wsgi:application

    [Install]
    WantedBy=multi-user.target
    ``` 
28. Меняем пользователя в файле nginx.conf
    ```bash
    sudo nano /etc/nginx/nginx.conf
    ```
    ```bash
    user <ИМЯ_ПОЛЬЗОВАТЕЛЯ>;  
    ```
29. Запускаем gunicorn
    ```bash
    sudo systemctl start gunicorn
    ```
    ```bash
    sudo systemctl status gunicorn
    ```
30. Проверяем работоспособность gunicorn
    ```bash
    sudo systemctl status gunicorn
    ```
    В терминале должна появиться запись зеленым цветом Active: active (running).
    В папке backend должен появиться файл project.sock
31. Создаем модуль для nginx
    ```bash
    sudo nano /etc/nginx/sites-available/project
    ```
    ```bash
    server{

    listen 80;
    server_name 195.208.119.35;

    location /static/ {
      root /home/<ИМЯ_ПОЛЬЗОВАТЕЛЯ>/d_backend;
    }

    location / {
      include proxy_params;
      proxy_pass http://unix:/home/<ИМЯ_ПОЛЬЗОВАТЕЛЯ>/d_backend/backend/project.sock;
    }
    }
    ```
32. Создаем символическую ссылку для запуска сайта
    ```bash
    sudo ln -s /etc/nginx/sites-available/project /etc/nginx/sites-enabled/
    ```
33. Проверяем nginx на ошибки в синтаксисе
    ```bash
    sudo nginx -t
    ```
34. Перезапускаем веб-сервер
    ```bash
    sudo systemctl restart nginx
    ```
35. Проверяем работоспособность nginx
    ```bash
    sudo systemctl status nginx
    ```
    В терминале должна появиться запись зеленым цветом Active: active (running).
36. С помощью файрвола разрешаем полные права ngins для подключений
    ```bash
    sudo ufw allow 'Nginx Full'
    ```
37. Проверяем доступность приложения в брузере
    ```bash
    <ip_адрес_сервера>
    ```
38. Проверить, что включено виртуальное окружение, нахождение в папке проекта (где файл manage.py),
    создать администратора (суперпользователя), имеющего право входить как в "Django administration", 
    так и в "Административный интерфейс" сайта. С целью безусловности прав владельца он не отображается
    в "Администртивном интерфейсе" сайта.
    ```bash
    python manage.py createsuperuser
    ```



