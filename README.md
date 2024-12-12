# СЕРВЕР



## Установка
1. Откройте директорию, в ней запустите командную строку и введите:

   ```bash
   git clone https://github.com/Summer20100/manya_server.git
   ```
2. Перейдите в папку проекта:
   ```bash
   cd manya_server
   ```
3. Cоздайте виртуальную среду Python введя команду:  
   ```bash
   python -m venv env
   ```
4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
1. Запустите  сервер:
   ```bash
   uvicorn main:app --reload
   ```
1. Сервер по умолчанию запускается по адресу:
    ```bash
    http://127.0.0.1:8000/
    ```

## REST API маршруты
1. Приветствие:
    ```bash
    http://127.0.0.1:8000/
    ```
1. Добавить пользователя:
   * метод POST;
    ```bash
    http://127.0.0.1:8000/users/
    ```
   * тело запроса:
    ```bash
    { 
            user: str,
            email: str
    }
    ```
2. Получить всех пользователей:  
   * метод GET;
    ```bash
    http://127.0.0.1:8000/users
    ```
3. Получить пользователя по ID:  
   * метод GET;
   * id: int;
    ```bash
    http://127.0.0.1:8000/users/id
    ```
4. Обновить данные пользователя:
   * метод PUT;
   * id: int;
    ```bash
    http://127.0.0.1:8000/users/id
    ```
   * тело запроса:
    ```bash
    { 
            user: str,
            email: str
    }
    ```
   * email _**не должен повторяться**_ с другими пользователями
5. Удалить пользователя:  
   * метод DELETE;
   * id: int;
    ```bash
    http://127.0.0.1:8000/users/id
    ```
   

