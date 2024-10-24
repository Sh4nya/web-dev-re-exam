Для запуска нужно создать app/config.py со структурой:

```python
import os

SECRET_KEY = "yourSecretKey"

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://user:password@host/db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "media", "images"
)

```
