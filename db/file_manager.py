class FileManager:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = FileManager()
        return cls._instance

    def read(self, pg_id):
        with open(str(pg_id) + ".pg", "r") as f:
            return f.readlines()

    def scan(self, _):
        pass