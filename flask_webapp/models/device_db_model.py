from db import db

class Device_Model(db.Model):
    __tablename__ = 'devices'
    name = db.Column(db.String(80), primary_key=True)
    status = db.Column(db.String(80))

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def json(self):
        return {'name': self.name, 'status': self.status}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name) # SELECT * FROM devices WHERE name=name

    @classmethod
    def find_by_status(cls, status):
        return cls.query.filter_by(status=status) # SELECT * FROM device WHERE status=status
