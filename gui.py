import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from win10toast import ToastNotifier
import json
import os
import webbrowser
import pystray
from PIL import Image

CONFIG_FILE = "config.json"
ICON_FILE = "icon.ico"

class AppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("zekkie's fun fl studio rpc tool for discord")
        self.root.geometry("520x520")
        self.root.resizable(False, False)
        self.root.iconbitmap(ICON_FILE)

        self.running = True
        self.tray = None
        self.notifier = ToastNotifier()

        self._load_config()
        self._build_menu()
        self._build_ui()

        self.root.protocol("WM_DELETE_WINDOW", self._hide_to_tray)
        self.root.after(200, self.sync_values)

    def _load_config(self):
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "w") as f:
                json.dump({
                    "project_details": "Working on {project}",
                    "project_state": "Producing",
                    "unsaved_details": "Unsaved project",
                    "unsaved_state": "CTRL+S?",
                    "no_project_details": "No project open",
                    "no_project_state": "Idle",
                    "start_paused": False
                }, f, indent=4)

        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)

        self.project_details_value = cfg["project_details"]
        self.project_state_value = cfg["project_state"]
        self.unsaved_details_value = cfg["unsaved_details"]
        self.unsaved_state_value = cfg["unsaved_state"]
        self.no_project_details_value = cfg["no_project_details"]
        self.no_project_state_value = cfg["no_project_state"]

        self.running = not cfg.get("start_paused", False)

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_config)
        file_menu.add_command(label="Restore", command=self.restore_config)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Credits", command=lambda: messagebox.showinfo("Credits", "zekkie's fun fl studio rich presence tool for discord\nby zekkie\nbecause fl doesn't have native discord rpc support\nversion 1.0.0\nbuilt for FL Studio 2025"))
        help_menu.add_command(label="GitHub Repo", command=lambda: webbrowser.open("https://github.com/yourusername/fl-rpc"))
        help_menu.add_command(label="Documentation", command=lambda: webbrowser.open("https://github.com/yourusername/fl-rpc/wiki"))
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        self.project_details_var = tk.StringVar(value=self.project_details_value)
        self.project_state_var = tk.StringVar(value=self.project_state_value)
        self.unsaved_details_var = tk.StringVar(value=self.unsaved_details_value)
        self.unsaved_state_var = tk.StringVar(value=self.unsaved_state_value)
        self.no_project_details_var = tk.StringVar(value=self.no_project_details_value)
        self.no_project_state_var = tk.StringVar(value=self.no_project_state_value)

        for label, var in [
            ("Project - Details", self.project_details_var),
            ("Project - State", self.project_state_var),
            ("Unsaved - Details", self.unsaved_details_var),
            ("Unsaved - State", self.unsaved_state_var),
            ("No project - Details", self.no_project_details_var),
            ("No project - State", self.no_project_state_var),
        ]:
            ttk.Label(container, text=label).pack(anchor="w", pady=(8, 2))
            ttk.Entry(container, textvariable=var).pack(fill="x", ipady=4)

        ttk.Separator(container).pack(fill="x", pady=20)

        self.toggle_btn = ttk.Button(container, command=self.toggle)
        self.toggle_btn.pack(fill="x", ipady=6)
        self._update_toggle()

    def sync_values(self):
        self.project_details_value = self.project_details_var.get()
        self.project_state_value = self.project_state_var.get()
        self.unsaved_details_value = self.unsaved_details_var.get()
        self.unsaved_state_value = self.unsaved_state_var.get()
        self.no_project_details_value = self.no_project_details_var.get()
        self.no_project_state_value = self.no_project_state_var.get()
        self.root.after(200, self.sync_values)

    def save_config(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save Configuration"
        )
        if not path:
            return 

        with open(path, "w") as f:
            json.dump({
                "project_details": self.project_details_value,
                "project_state": self.project_state_value,
                "unsaved_details": self.unsaved_details_value,
                "unsaved_state": self.unsaved_state_value,
                "no_project_details": self.no_project_details_value,
                "no_project_state": self.no_project_state_value,
                "start_paused": not self.running
            }, f, indent=4)
        messagebox.showinfo("Saved", f"Configuration saved to:\n{path}")

    def restore_config(self):
        path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Open Configuration"
        )
        if not path:
            return 

        with open(path, "r") as f:
            cfg = json.load(f)

        self.project_details_value = cfg.get("project_details", self.project_details_value)
        self.project_state_value = cfg.get("project_state", self.project_state_value)
        self.unsaved_details_value = cfg.get("unsaved_details", self.unsaved_details_value)
        self.unsaved_state_value = cfg.get("unsaved_state", self.unsaved_state_value)
        self.no_project_details_value = cfg.get("no_project_details", self.no_project_details_value)
        self.no_project_state_value = cfg.get("no_project_state", self.no_project_state_value)
        self.running = not cfg.get("start_paused", not self.running)

        self.project_details_var.set(self.project_details_value)
        self.project_state_var.set(self.project_state_value)
        self.unsaved_details_var.set(self.unsaved_details_value)
        self.unsaved_state_var.set(self.unsaved_state_value)
        self.no_project_details_var.set(self.no_project_details_value)
        self.no_project_state_var.set(self.no_project_state_value)
        self._update_toggle()

    def toggle(self):
        self.running = not self.running
        self._update_toggle()

    def _update_toggle(self):
        self.toggle_btn.config(
            text="Pause Rich Presence" if self.running else "Resume Rich Presence"
        )

    def _hide_to_tray(self):
        self.root.withdraw()

        try:
            self.notifier.show_toast(
                "zekkie's fun fl rpc tool",
                "The app has been minimized to the tray.",
                icon_path=ICON_FILE,
                duration=5,
                threaded=True
            )
        except Exception:
            pass

        if not self.tray:
            image = Image.open(ICON_FILE)
            self.tray = pystray.Icon(
                "fl-rpc",
                image,
                "zekkie's fun fl rpc tool",
                menu=pystray.Menu(
                    pystray.MenuItem("Show", self._show_from_tray),
                    pystray.MenuItem("Quit", self._quit)
                )
            )
            import threading
            threading.Thread(target=self.tray.run, daemon=True).start()

    def _show_from_tray(self):
        self.root.after(0, self.root.deiconify)
        if self.tray:
            tray_ref = self.tray
            self.tray = None
            tray_ref.stop()

    def _quit(self):
        if self.tray:
            tray_ref = self.tray
            self.tray = None
            tray_ref.stop()

        self.root.after(0, self.root.destroy)

    def loop(self):
        self.root.update()

    def close(self):
        self._quit()
