from typing import List, Dict
from parent_model import ParentModel


class TeleHealth(ParentModel):
    """Class represents a telehealth session"""
    def __init__(self, patient_id: str, staff_id: str, session_date: str,
                 session_time: str, session_length: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_id = patient_id
        self.staff_id = staff_id
        self.session_date = session_date
        self.session_time = session_time
        self.session_length = session_length

    def to_dict(self) -> Dict:
        """Returns dictionary representation of object"""
        attr = super().to_dict()
        attr.update({
            "patient_id": self.patient_id,
            "staff_id": self.staff_id,
            "session_date": self.session_date,
            "session_time": self.session_time,
            "session_length": self.session_length
        })
        return attr

    def __str__(self):
        """Returns string representation of object"""
        return f"[[{self.__class__.__name__}] ({self.id}) {self.to_dict()}]"


class TeleHealthSchedule(ParentModel):
    """Class represents a scheduled telehealth session"""
    def __init__(self, patient_id: str, staff_id: str, session_date: str,
                 session_time: str, session_length: int, status: str = "pending",
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_id = patient_id
        self.staff_id = staff_id
        self.session_date = session_date
        self.session_time = session_time
        self.session_length = session_length
        self.status = status

    def to_dict(self) -> Dict:
        """Returns dictionary representation of object"""
        attr = super().to_dict()
        attr.update({
            "patient_id": self.patient_id,
            "staff_id": self.staff_id,
            "session_date": self.session_date,
            "session_time": self.session_time,
            "session_length": self.session_length,
            "status": self.status
        })
        return attr

    def __str__(self):
        """Returns string representation of object"""
        return f"[[{self.__class__.__name__}] ({self.id}) {self.to_dict()}]"


class TeleHealthLog(ParentModel):
    """Class represents a log of telehealth sessions"""
    def __init__(self, patient_id: str, staff_id: str, session_date: str,
                 session_time: str, session_length: int, duration: int,
                 call_quality: int, comments: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_id = patient_id
        self.staff_id = staff_id
        self.session_date = session_date
        self.session_time = session_time
        self.session_length = session_length
        self.duration = duration
        self.call_quality = call_quality
        self.comments = comments

    def to_dict(self) -> Dict:
        """Returns dictionary representation of object"""
        attr = super().to_dict()
        attr.update({
            "patient_id": self.patient_id,
            "staff_id": self.staff_id,
            "session_date": self.session_date,
            "session_time": self.session_time,
            "session_length": self.session_length,
            "duration": self.duration,
            "call_quality": self.call_quality,
            "comments": self.comments
        })
        return attr

    def __str__(self):
        """Returns string"""
