from pathlib import Path
import json

SESSION_DIR = Path.home() / ".cloudhopper" / "sessions"
SESSION_FilE = SESSION_DIR / "session.json"


class SessionManager:
    def __init__(self):
        self.session_file = SESSION_FilE
        self.session_data = {}


    @staticmethod
    def load_session(self):
        if self.session_file.exists():
            with open(self.session_file, "r") as f:
                self.session_data = json.load(f)
        else:
            self.session_data = {}

    @staticmethod
    def save_session(self):
        SESSION_DIR.mkdir(parents=True, exist_ok=True)
        with open(self.session_file, "w") as f:
            json.dump(self.session_data, f)

    @staticmethod
    def get_session_data(self):
        return self.session_data

    @staticmethod
    def set_session_data(self, data):
        self.session_data = data
        self.save_session()

    @staticmethod
    def clear_session(self):
        self.session_data = {}
        if self.session_file.exists():
            self.session_file.unlink()
        

    