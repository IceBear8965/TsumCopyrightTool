import json

class Saver:
    def save(self, data, file_name):
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False)
        except Exception:
            pass

    def load(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data
        except Exception:
            return False