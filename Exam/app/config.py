import os

SECRET_KEY = "91c7126afb5e5fc8e38adb2e5ea39b7c"

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://std_2380_exam:password@std-mysql.ist.mospolytech.ru/std_2380_exam"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "media", "images"
)
