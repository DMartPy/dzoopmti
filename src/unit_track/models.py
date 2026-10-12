from abc import ABC, abstractmethod
from datetime import datetime


class AbstractEntity(ABC):    
    @abstractmethod
    def get_id(self) -> int:
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass


class Pair:
    def __init__(self, k, v):
        self.key = k
        self.val = v

    def __eq__(self, other):
        if isinstance(other, Pair):
            return self.key == other.key
        return False


class MyMap:
    def __init__(self):
        self.data = [] 

    def set_item(self, key, value):
        for item in self.data:
            if item.key == key:
                item.val = value
                return
        self.data.append(Pair(key, value))

    def get_item(self, key):
        for item in self.data:
            if item.key == key:
                return item.val
        return None

    def delete_item(self, key):
        for i, item in enumerate(self.data):
            if item.key == key:
                del self.data[i]
                return True
        return False
    
    def get_values(self):
        return [item.val for item in self.data]

    def __len__(self):
        return len(self.data)
    
    def __contains__(self, key):
        for item in self.data:
            if item.key == key:
                return True
        return False


class Task(AbstractEntity):
    def __init__(self, t_id, name, prio):
        self._id = t_id
        self._name = name
        self._prio = prio
        self.done = False

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, val):
        if not val:
            raise ValueError("Имя не может быть пустым")
        self._name = val

    @property
    def priority(self):
        return self._prio
    
    @priority.setter
    def priority(self, val):
        if not (1 <= val <= 10):
            raise ValueError("Приоритет должен быть 1-10")
        self._prio = val

    def get_id(self):
        return self._id

    def __eq__(self, other):
        if isinstance(other, Task):
            return self._id == other._id
        return False

    def __lt__(self, other):
        if self._prio != other._prio:
            return self._prio > other._prio 
        return self._id < other._id

    def __hash__(self):
        return hash(self._id)

    def __str__(self):
        status = "[Готово]" if self.done else "[Активна]"
        return f"{status} {self._name} (P:{self._prio})"

    def __repr__(self):
        return f"Task({self._id}, '{self._name}', P={self._prio})"


class User(AbstractEntity):
    def __init__(self, u_id, login):
        self._id = u_id
        self._login = login

    @property
    def id(self):
        return self._id
    
    @property
    def login(self):
        return self._login

    def get_id(self):
        return self._id

    def __str__(self):
        return f"User({self._login})"
    
    def __eq__(self, other):
        if isinstance(other, User):
            return self._id == other._id
        return False
        
    def __hash__(self):
        return hash(self._id)


class SessionManager:    
    def __init__(self):
        self.user_login = "Guest"
        self.time_start = datetime.now()
        self.time_end = None

    def set_user(self, login: str):
        self.user_login = login

    def finish_session(self):
        self.time_end = datetime.now()

    def generate_report_text(self) -> str:
        fmt = "%d.%m.%Y %H:%M:%S"
        t_in = self.time_start.strftime(fmt)
        t_out = self.time_end.strftime(fmt) if self.time_end else "N/A"
        
        table = "+------------------------+---------------------+---------------------+\n"
        table += "|       LOGIN            |      TIME IN        |      TIME OUT       |\n"
        table += "+------------------------+---------------------+---------------------+\n"
        
        log_cell = f"| {self.user_login:<22}|"
        tin_cell = f"| {t_in:<19}|"
        tout_cell = f"| {t_out:<19}|\n"
        
        table += log_cell + tin_cell + tout_cell
        table += "+------------------------+---------------------+---------------------+"
        return table

    def save_to_file(self, filename: str = "report.txt"):
        self.finish_session()
        text = self.generate_report_text()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)