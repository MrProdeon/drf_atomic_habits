## Запуск проекта локально

1) Клонируйте репозиторий
``` git clone https://github.com/MrProdeon/drf_atomic_habits.git```
2) - Установите Poetry ```pip install poetry```
   - Установите зависимости ``` poetry install```
3) Создайте .env файл и заполните его по шаблону .env.template.
4) Запустите Docker Desktop
5) Выполните команду docker-compose up
6) После успешного запуска контейнеров проект будет развернут локально по адресу http://localhost:8000/

## Деплой проекта на сервер

1) Сделайте форк репозитория
2) Установите ваши секреты:  
ALLOWED_HOSTS  
DB_HOST  
DB_NAME  
DB_PASSWORD  
DB_PORT  
DB_USER  
DOCKER_HUB_ACCESS_TOKEN  
DOCKER_LOGIN  
POSTGRES_DB  
POSTGRES_PASSWORD  
POSTGRES_USER  
SECRET_KEY  
SERVER_IP  
SSH_KEY  
SSH_USER  
TELEGRAM_TOKEN  
3) Откройте файл ci.yml и на 163 строке укажите url вашего репозитория
для клонирования
4) Запушьте изменения
5) После успешного завершения пайплайна проект будет развернут на вашем сервере
