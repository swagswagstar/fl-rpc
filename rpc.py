import time
from pypresence import Presence

class FLRPC:
    def __init__(self, client_id):
        self.rpc = Presence(client_id)
        self.rpc.connect()
        self.start_time = int(time.time())
        self.enabled = True

    def pause(self):
        self.enabled = False
        self.rpc.clear()

    def resume(self):
        self.enabled = True
        self.start_time = int(time.time())

    def update(self, details, state):
        if not self.enabled:
            return

        self.rpc.update(
            details=details,
            state=state,
            large_image="fl-icon",
            large_text="FL Studio 2025",
            start=self.start_time
        )

    def close(self):
        self.rpc.close()
