# **ОБЛАЧНОЕ ХРАНИЛИЩЕ MyCloud**
## Серверная часть приложения (Backend) <br>(разработан с использованием Django)

### 1. *Структура проекта*

`d_back` - корневая папка бэкенда<br>
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
   `git clone https://github.com/ART20230129/d_back`

3. Открыть папку `d_back` в любой IDE и запустить встроенный терминал

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

10. Создаем базу данных (DB_USER и DB_NAME взять из файла `.env` (см. п. 9)
    
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
   