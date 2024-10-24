import hashlib
import os
from flask import current_app
from models import db, Cover


class CoverSaver:
    def __init__(self, file):
        self.file = file

    def save(self):
        self.img = self.__find_by_md5_hash()
        if self.img is not None:
            return self.img

        filename = self.md5_hash + "." + self.file.filename.rsplit(".", 1)[1]
        self.img = Cover(
            filename=filename, mime_type=self.file.mimetype, md5_hash=self.md5_hash
        )
        self.file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        db.session.add(self.img)
        db.session.commit()
        return self.img

    def __find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return db.session.execute(
            db.select(Cover).filter(Cover.md5_hash == self.md5_hash)
        ).scalar()


class CoverRemover:
    def __init__(self, coverName):
        self.coverName = coverName

    def remove(self):
        try:
            os.remove(os.path.join(current_app.config["UPLOAD_FOLDER"], self.coverName))
            return True
        except FileNotFoundError:
            return False
