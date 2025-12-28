import psutil
import win32gui
import win32process

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
                return ("project", title.rsplit(" - FL Studio", 1)[0].strip())

            return ("unsaved", None)

    return None
