import time
import threading
from fl import get_fl_status
from rpc import FLRPC
from gui import AppGUI

CLIENT_ID = "1344373188293034066"

gui = AppGUI()
rpc = FLRPC(CLIENT_ID)

def rpc_worker():
    missing_since = None
    last_status = None

    while True:
        if not gui.running:
            rpc.pause()
            time.sleep(0.2)
            continue
        else:
            rpc.resume()

        status = get_fl_status()

        if status:
            missing_since = None
            mode, project = status

            if status != last_status:
                rpc.start_time = int(time.time())
                last_status = status

            if mode == "project":
                rpc.update(
                    gui.project_details_value.format(project=project),
                    gui.project_state_value
                )
            elif mode == "unsaved":
                rpc.update(
                    gui.unsaved_details_value,
                    gui.unsaved_state_value
                )
            else:
                rpc.update(
                    gui.no_project_details_value,
                    gui.no_project_state_value
                )
        else:
            if missing_since is None:
                missing_since = time.time()

            rpc.update(
                gui.no_project_details_value,
                gui.no_project_state_value
            )

            if time.time() - missing_since >= 10:
                rpc.pause()
                break

        time.sleep(10)

threading.Thread(target=rpc_worker, daemon=True).start()

try:
    while True:
        gui.loop()
        time.sleep(0.01)
except KeyboardInterrupt:
    pass

rpc.close()
gui.close()
