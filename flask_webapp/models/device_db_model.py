import __init__
from flask_sqlalchemy import SQLAlchemy

DB_RETURN_STATUS = {
        "HTTP_512_DOUBLE_ENTRY_DB_ERROR": 512,
        "HTTP_514_WRONG_DEVICE_CONNECTED_DB_ERROR": 514,
        "HTTP_515_NO_DEVICE_RETURNED": 515,
        "HTTP_200_OK": 200,
    }

db = SQLAlchemy()

class Device_Model(db.Model):
    __tablename__ = 'devices'
    name = db.Column(db.String(80), primary_key=True)
    status = db.Column(db.String(80), nullable=False)

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def json(self):
        return {'name': self.name, 'status': self.status}

    def save_to_db(self):
        print(f"Changing entry: {self.name} to {self.status}")
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        device_search_result = cls.query.filter_by(name=name) # SELECT * FROM devices WHERE name=name
        return cls.get_single_entry_or_error_list(device_search_result)

    @classmethod
    def find_by_status(cls, status):
        device_search_result = cls.query.filter_by(status=status)  # SELECT * FROM device WHERE status=status
        return cls.get_single_entry_or_error_list(device_search_result)

    @classmethod
    def get_single_entry_or_error_list(cls, queryObj):
        status = None
        return_entry = None
        if queryObj.first() is not None:
            entry_list = queryObj.all()
            if len(entry_list) == 1:   # only a single entry is allowed for our use-case.
                status = DB_RETURN_STATUS["HTTP_200_OK"]
                return_entry = entry_list[0]
            else:   # If more than one entry, return error code with list
                status = DB_RETURN_STATUS["HTTP_512_DOUBLE_ENTRY_DB_ERROR"]
                return_entry = entry_list
        else:
            status = DB_RETURN_STATUS["HTTP_515_NO_DEVICE_RETURNED"]   # None is a valid state if empty
            return_entry = None

        return status, return_entry

    @classmethod
    def disconnect_all_devices(cls):
        print("Disconnecting connected device before closing application!")
        db_status, connected_dev_from_db = cls.find_by_status("connected")
        if db_status == DB_RETURN_STATUS["HTTP_200_OK"]:
            connected_dev_from_db.status = "disconnected"  # Update db to disconnected status
            connected_dev_from_db.save_to_db()
        elif db_status == DB_RETURN_STATUS["HTTP_512_DOUBLE_ENTRY_DB_ERROR"]:
            for device in connected_dev_from_db:
                device.status = "disconnected"  # Update db to disconnected status
                device.save_to_db()