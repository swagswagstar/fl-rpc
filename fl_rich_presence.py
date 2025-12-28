import time
import psutil
from pypresence import Presence
import win32gui
import win32process

CLIENT_ID = "1344373188293034066"
rpc = Presence(CLIENT_ID)
rpc.connect()

start_time = int(time.time())
missing_since = None
last_status = None

def get_fl_status():
    fl_names = ["fl.exe", "fl64.exe", "fl studio.exe", "flengine.exe"]

    for proc in psutil.process_iter(['pid', 'name']):
        name = proc.info['name']
        if name and any(x in name.lower() for x in fl_names):
            pid = proc.info['pid']

            def callback(hwnd, titles):
                if win32gui.IsWindowVisible(hwnd):
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if found_pid == pid:
                        title = win32gui.GetWindowText(hwnd)
                        if "FL Studio" in title or title == "Welcome to FL Studio":
                            titles.append(title)
                return True

            titles = []
            win32gui.EnumWindows(callback, titles)

            if not titles:
                return None

            title = titles[0].strip()

            if title == "Welcome to FL Studio":
                return ("no_project", None)

            if title == "FL Studio 25":
                return ("unsaved", None)

            if " - FL Studio" in title:
                project = title.rsplit(" - FL Studio", 1)[0].strip()
                return ("project", project)

            return ("unsaved", None)

    return None

try:
    while True:
        status = get_fl_status()

        if status:
            missing_since = None

            if status != last_status:
                start_time = int(time.time())
                last_status = status

            mode, project = status

            if mode == "project":
                rpc.update(
                    details=f"Working on {project}",
                    state="wallahi im finished 😭😭",
                    large_image="fl-icon",
                    large_text="FL Studio 2025",
                    start=start_time
                )
            elif mode == "unsaved":
                rpc.update(
                    details="Unsaved project",
                    state="surely i wont close without saving right??",
                    large_image="fl-icon",
                    large_text="FL Studio 2025",
                    start=start_time
                )
            else:
                rpc.update(
                    details="Unsaved project",
                    state="don't mind me... 💤",
                    large_image="fl-icon",
                    large_text="FL Studio 2025",
                    start=start_time
                )
        else:
            if missing_since is None:
                missing_since = time.time()

            rpc.update(
                details="Browsing FL Studio",
                state="No project open",
                large_image="fl-icon",
                large_text="FL Studio 2025",
                start=start_time
            )

            if time.time() - missing_since >= 10:
                break

        time.sleep(15)

except KeyboardInterrupt:
    pass

rpc.close()
