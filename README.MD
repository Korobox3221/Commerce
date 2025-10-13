
### Commerce
### Автор: Константин Коробейников



Платформа для онлайн-аукционов. Реализована система ставок, закрытия лотов, добавления товаров и категорий. Использованы Django Models для хранения данных о пользователях, лотах и ставках.

**Ключевые технологии:** Django, Python, SQLite, HTML/CSS.

### **Как запустить данное приложение**

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Korobox3221/Commerce.git
    cd commerce
    ```
2.  **Установите зависимости:**
    ```bashcd
    pip install -r requirements.txt
    ```
3.  **Примените миграцию базы данных:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4.  **Создайте суперпользователя (необязательно):**
    ```bash
    python manage.py createsuperuser
    ```
5.  **Запустите сервер для разработки:**
    ```bash
    python manage.py runserver
    ```

Приложение будет запущено на `http://127.0.0.1:8000/`.
