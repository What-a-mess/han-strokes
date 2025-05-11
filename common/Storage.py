import json
import threading


class Storage:
    
    storage_map = {}
    get_storage_lock = threading.Lock()
    
    def __init__(self, data_path: str = "data.json", flush_interval: int = 5):
        self.data_path = data_path
        self.data = {}
        self.dirty = False
        self.lock = threading.Lock()
        self.flush_interval = flush_interval
        self._stop_event = threading.Event()

        try:
            with open(self.data_path, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            with open(self.data_path, "w") as file:
                json.dump({}, file)

        # Start a background thread to flush data periodically
        self.flush_thread = threading.Thread(
            target=self._flush_periodically, daemon=True
        )
        self.flush_thread.start()
        
    @classmethod
    def get_storage(cls, data_path: str = "data.json", flush_interval: int = 5):
        """_summary_

        Args:
            data_path (str, optional): _description_. config location, Defaults to "data.json".
            flush_interval (int, optional): _description_. flush interval, Defaults to 5, if the storage exists, this parameter won't work.

        Returns:
            _type_: _description_ Storage instance
        """
        with cls.get_storage_lock:
            if data_path not in cls.storage_map:
                cls.storage_map[data_path] = Storage(data_path, flush_interval)
            return cls.storage_map[data_path]

    def set(self, key, value):
        with self.lock:
            self.data[key] = value
            self.dirty = True

    def get(self, key, default=None):
        with self.lock:
            return self.data.get(key, default)

    def update(self, kv: dict):
        with self.lock:
            self.data.update(kv)
            self.dirty = True

    def delete(self, key):
        with self.lock:
            if key in self.data:
                del self.data[key]
                self.dirty = True

    def _flush_periodically(self):
        while not self._stop_event.is_set():
            self._stop_event.wait(self.flush_interval)
            self.flush()

    def flush(self):
        with self.lock:
            if self.dirty:
                with open(self.data_path, "w") as file:
                    json.dump(self.data, file)
                self.dirty = False

    def close(self):
        self._stop_event.set()
        self.flush_thread.join()
        self.flush()

    def __del__(self):
        self.close()
