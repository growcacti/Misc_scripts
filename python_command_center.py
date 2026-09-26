#!/usr/bin/env python3
"""
Python Command Center
A Tkinter GUI for common Python / pip tasks on MX Linux / Debian.

Features:
- Select a Python interpreter (system Python, Python 3.14, or custom)
- Generate requirements.txt using pip freeze
- Install requirements.txt
- Install / upgrade / uninstall individual packages
- Use --break-system-packages when needed on Debian/MX Linux
- List installed packages
- List outdated packages
- Run pip check
- Show package information
- Create a virtual environment
- Upgrade pip
- Show Python / pip versions
- Command preview and output console

Uses only Python standard-library modules.
"""

import os
import queue
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


APP_TITLE = "Python Command Center"


def find_python_executables():
    """Return a unique list of likely Python executables."""
    candidates = []

    # Current interpreter first.
    if sys.executable:
        candidates.append(sys.executable)

    # Common Linux names.
    names = [
        "python3",
        "python3.14",
        "python3.13",
        "python3.12",
        "python3.11",
        "python",
    ]

    for name in names:
        found = shutil.which(name)
        if found:
            candidates.append(found)

    # Common absolute locations.
    for path in [
        "/usr/bin/python3",
        "/usr/bin/python3.14",
        "/usr/local/bin/python3.14",
        "/usr/local/bin/python3",
    ]:
        if Path(path).exists():
            candidates.append(path)

    # Preserve order, remove duplicates.
    seen = set()
    unique = []
    for item in candidates:
        try:
            resolved = str(Path(item).resolve())
        except OSError:
            resolved = item
        if resolved not in seen:
            seen.add(resolved)
            unique.append(item)

    return unique


class PythonCommandCenter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1050x760")
        self.minsize(900, 650)

        self.output_queue = queue.Queue()
        self.current_process = None

        self.project_dir = tk.StringVar(value=str(Path.cwd()))
        self.python_exe = tk.StringVar()
        self.requirements_file = tk.StringVar(value=str(Path.cwd() / "requirements.txt"))
        self.package_name = tk.StringVar()
        self.break_system = tk.BooleanVar(value=False)
        self.user_install = tk.BooleanVar(value=False)
        self.upgrade_package = tk.BooleanVar(value=False)
        self.status_text = tk.StringVar(value="Ready")

        self.python_choices = find_python_executables()
        if self.python_choices:
            self.python_exe.set(self.python_choices[0])
        else:
            self.python_exe.set(sys.executable or "python3")

        self._build_ui()
        self._update_command_preview()
        self.after(100, self._poll_output_queue)

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        # --- Interpreter frame ---
        interp = ttk.LabelFrame(self, text="Python Interpreter")
        interp.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        interp.columnconfigure(1, weight=1)

        ttk.Label(interp, text="Python:").grid(
            row=0, column=0, padx=8, pady=8, sticky="w"
        )

        self.python_combo = ttk.Combobox(
            interp,
            textvariable=self.python_exe,
            values=self.python_choices,
        )
        self.python_combo.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        self.python_combo.bind("<<ComboboxSelected>>", lambda e: self._update_command_preview())
        self.python_combo.bind("<KeyRelease>", lambda e: self._update_command_preview())

        ttk.Button(
            interp, text="Browse...", command=self._browse_python
        ).grid(row=0, column=2, padx=5, pady=8)

        ttk.Button(
            interp, text="Refresh", command=self._refresh_python_list
        ).grid(row=0, column=3, padx=5, pady=8)

        ttk.Button(
            interp, text="Versions", command=self._show_versions
        ).grid(row=0, column=4, padx=5, pady=8)

        # --- Project / requirements frame ---
        project = ttk.LabelFrame(self, text="Project and Requirements")
        project.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        project.columnconfigure(1, weight=1)

        ttk.Label(project, text="Project folder:").grid(
            row=0, column=0, padx=8, pady=5, sticky="w"
        )
        ttk.Entry(project, textvariable=self.project_dir).grid(
            row=0, column=1, padx=8, pady=5, sticky="ew"
        )
        ttk.Button(project, text="Browse...", command=self._browse_project).grid(
            row=0, column=2, padx=5, pady=5
        )

        ttk.Label(project, text="requirements.txt:").grid(
            row=1, column=0, padx=8, pady=5, sticky="w"
        )
        ttk.Entry(project, textvariable=self.requirements_file).grid(
            row=1, column=1, padx=8, pady=5, sticky="ew"
        )
        ttk.Button(project, text="Choose...", command=self._browse_requirements).grid(
            row=1, column=2, padx=5, pady=5
        )

        req_buttons = ttk.Frame(project)
        req_buttons.grid(row=2, column=0, columnspan=3, padx=8, pady=8, sticky="ew")

        ttk.Button(
            req_buttons,
            text="Generate requirements.txt",
            command=self._generate_requirements,
        ).grid(row=0, column=0, padx=4, pady=2)

        ttk.Button(
            req_buttons,
            text="Install requirements.txt",
            command=self._install_requirements,
        ).grid(row=0, column=1, padx=4, pady=2)

        ttk.Button(
            req_buttons,
            text="Open requirements.txt",
            command=self._open_requirements,
        ).grid(row=0, column=2, padx=4, pady=2)

        # --- Package frame ---
        packages = ttk.LabelFrame(self, text="Package Management")
        packages.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        packages.columnconfigure(1, weight=1)

        ttk.Label(packages, text="Package name(s):").grid(
            row=0, column=0, padx=8, pady=7, sticky="w"
        )
        package_entry = ttk.Entry(packages, textvariable=self.package_name)
        package_entry.grid(row=0, column=1, padx=8, pady=7, sticky="ew")
        package_entry.bind("<KeyRelease>", lambda e: self._update_command_preview())

        ttk.Checkbutton(
            packages,
            text="--break-system-packages",
            variable=self.break_system,
            command=self._update_command_preview,
        ).grid(row=1, column=0, padx=8, pady=4, sticky="w")

        ttk.Checkbutton(
            packages,
            text="--user",
            variable=self.user_install,
            command=self._update_command_preview,
        ).grid(row=1, column=1, padx=8, pady=4, sticky="w")

        ttk.Checkbutton(
            packages,
            text="Upgrade package",
            variable=self.upgrade_package,
            command=self._update_command_preview,
        ).grid(row=1, column=2, padx=8, pady=4, sticky="w")

        pkg_buttons = ttk.Frame(packages)
        pkg_buttons.grid(row=2, column=0, columnspan=3, padx=8, pady=8, sticky="ew")

        ttk.Button(pkg_buttons, text="Install", command=self._install_package).grid(
            row=0, column=0, padx=4, pady=2
        )
        ttk.Button(pkg_buttons, text="Uninstall", command=self._uninstall_package).grid(
            row=0, column=1, padx=4, pady=2
        )
        ttk.Button(pkg_buttons, text="Show Info", command=self._show_package).grid(
            row=0, column=2, padx=4, pady=2
        )
        ttk.Button(pkg_buttons, text="List Installed", command=self._pip_list).grid(
            row=0, column=3, padx=4, pady=2
        )
        ttk.Button(pkg_buttons, text="List Outdated", command=self._pip_outdated).grid(
            row=0, column=4, padx=4, pady=2
        )
        ttk.Button(pkg_buttons, text="pip check", command=self._pip_check).grid(
            row=0, column=5, padx=4, pady=2
        )
        ttk.Button(pkg_buttons, text="Upgrade pip", command=self._upgrade_pip).grid(
            row=0, column=6, padx=4, pady=2
        )

        # --- Utilities frame ---
        utilities = ttk.LabelFrame(self, text="Utilities")
        utilities.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        utilities.columnconfigure(1, weight=1)

        ttk.Button(
            utilities, text="Create .venv", command=self._create_venv
        ).grid(row=0, column=0, padx=6, pady=7)

        ttk.Button(
            utilities, text="Activate Command", command=self._show_activate_command
        ).grid(row=0, column=1, padx=6, pady=7, sticky="w")

        ttk.Button(
            utilities, text="Clear Output", command=self._clear_output
        ).grid(row=0, column=2, padx=6, pady=7)

        ttk.Button(
            utilities, text="Stop Running Command", command=self._stop_process
        ).grid(row=0, column=3, padx=6, pady=7)

        # --- Output frame ---
        output_frame = ttk.LabelFrame(self, text="Command Preview and Output")
        output_frame.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(2, weight=1)

        ttk.Label(output_frame, text="Command preview:").grid(
            row=0, column=0, padx=8, pady=(6, 2), sticky="w"
        )

        self.command_preview = tk.Text(output_frame, height=2, wrap="word")
        self.command_preview.grid(
            row=1, column=0, padx=8, pady=(0, 6), sticky="ew"
        )

        console_frame = ttk.Frame(output_frame)
        console_frame.grid(row=2, column=0, padx=8, pady=5, sticky="nsew")
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)

        self.output = tk.Text(console_frame, wrap="word")
        self.output.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            console_frame, orient="vertical", command=self.output.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output.configure(yscrollcommand=scrollbar.set)

        status = ttk.Label(self, textvariable=self.status_text, relief="sunken", anchor="w")
        status.grid(row=5, column=0, padx=10, pady=(3, 10), sticky="ew")

    # ---------- Browsing ----------

    def _browse_python(self):
        filename = filedialog.askopenfilename(
            title="Select Python executable",
            initialdir="/usr/bin" if Path("/usr/bin").exists() else str(Path.home()),
        )
        if filename:
            self.python_exe.set(filename)
            self._update_command_preview()

    def _browse_project(self):
        folder = filedialog.askdirectory(
            title="Select project folder",
            initialdir=self.project_dir.get() or str(Path.home()),
        )
        if folder:
            self.project_dir.set(folder)
            self.requirements_file.set(str(Path(folder) / "requirements.txt"))

    def _browse_requirements(self):
        filename = filedialog.askopenfilename(
            title="Select requirements file",
            initialdir=self.project_dir.get() or str(Path.home()),
            filetypes=[
                ("Requirements files", "requirements*.txt"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.requirements_file.set(filename)

    def _refresh_python_list(self):
        self.python_choices = find_python_executables()
        self.python_combo["values"] = self.python_choices
        self._write_output("\nDetected Python interpreters:\n")
        for item in self.python_choices:
            self._write_output(f"  {item}\n")

    # ---------- Command helpers ----------

    def _python(self):
        value = self.python_exe.get().strip()
        return value or "python3"

    def _pip_base(self):
        return [self._python(), "-m", "pip"]

    def _install_flags(self):
        flags = []
        if self.break_system.get():
            flags.append("--break-system-packages")
        if self.user_install.get():
            flags.append("--user")
        return flags

    def _display_command(self, command):
        # Basic readable quoting for preview.
        pieces = []
        for part in command:
            part = str(part)
            if any(c.isspace() for c in part):
                pieces.append(f'"{part}"')
            else:
                pieces.append(part)
        return " ".join(pieces)

    def _set_preview(self, command):
        self.command_preview.delete("1.0", "end")
        self.command_preview.insert("1.0", self._display_command(command))

    def _update_command_preview(self):
        package = self.package_name.get().strip() or "PACKAGE_NAME"
        command = self._pip_base() + ["install"]
        if self.upgrade_package.get():
            command.append("--upgrade")
        command += self._install_flags()
        command += package.split()
        self._set_preview(command)

    def _validate_python(self):
        exe = self._python()
        if os.path.sep in exe and not Path(exe).exists():
            messagebox.showerror("Python not found", f"Python executable not found:\n{exe}")
            return False
        return True

    # ---------- Process running ----------

    def _run_command(self, command, cwd=None):
        if not self._validate_python():
            return

        if self.current_process is not None:
            messagebox.showwarning(
                "Command running",
                "Another command is still running. Stop it or wait for it to finish.",
            )
            return

        self._set_preview(command)
        self._write_output("\n$ " + self._display_command(command) + "\n")
        self.status_text.set("Running...")

        def worker():
            try:
                self.current_process = subprocess.Popen(
                    command,
                    cwd=cwd or self.project_dir.get() or None,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )

                if self.current_process.stdout:
                    for line in self.current_process.stdout:
                        self.output_queue.put(("text", line))

                rc = self.current_process.wait()
                self.output_queue.put(("done", rc))

            except FileNotFoundError as exc:
                self.output_queue.put(("text", f"\nERROR: {exc}\n"))
                self.output_queue.put(("done", 1))
            except Exception as exc:
                self.output_queue.put(("text", f"\nERROR: {exc}\n"))
                self.output_queue.put(("done", 1))

        threading.Thread(target=worker, daemon=True).start()

    def _poll_output_queue(self):
        try:
            while True:
                item_type, value = self.output_queue.get_nowait()
                if item_type == "text":
                    self._write_output(value)
                elif item_type == "done":
                    self.current_process = None
                    if value == 0:
                        self.status_text.set("Finished successfully")
                        self._write_output("\n[Finished successfully]\n")
                    else:
                        self.status_text.set(f"Command finished with error code {value}")
                        self._write_output(f"\n[Finished with exit code {value}]\n")
        except queue.Empty:
            pass

        self.after(100, self._poll_output_queue)

    def _write_output(self, text):
        self.output.insert("end", text)
        self.output.see("end")

    def _clear_output(self):
        self.output.delete("1.0", "end")
        self.status_text.set("Ready")

    def _stop_process(self):
        if self.current_process is None:
            self.status_text.set("No command is running")
            return

        try:
            self.current_process.terminate()
            self._write_output("\n[Stop requested]\n")
            self.status_text.set("Stopping...")
        except Exception as exc:
            messagebox.showerror("Stop failed", str(exc))

    # ---------- Requirements ----------

    def _generate_requirements(self):
        req = Path(self.requirements_file.get()).expanduser()
        req.parent.mkdir(parents=True, exist_ok=True)

        if req.exists():
            if not messagebox.askyesno(
                "Overwrite requirements.txt",
                f"This file already exists:\n\n{req}\n\nOverwrite it?",
            ):
                return

        command = self._pip_base() + ["freeze"]

        self._set_preview(command + [">", str(req)])
        self._write_output(
            "\n$ " + self._display_command(command) + f" > {req}\n"
        )
        self.status_text.set("Generating requirements.txt...")

        def worker():
            try:
                result = subprocess.run(
                    command,
                    cwd=self.project_dir.get() or None,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                if result.returncode == 0:
                    req.write_text(result.stdout, encoding="utf-8")
                    self.output_queue.put(
                        ("text", f"Saved requirements to:\n{req}\n")
                    )
                else:
                    self.output_queue.put(("text", result.stderr))
                self.output_queue.put(("done", result.returncode))
            except Exception as exc:
                self.output_queue.put(("text", f"\nERROR: {exc}\n"))
                self.output_queue.put(("done", 1))

        if self.current_process is not None:
            messagebox.showwarning("Busy", "Another command is already running.")
            return

        threading.Thread(target=worker, daemon=True).start()

    def _install_requirements(self):
        req = Path(self.requirements_file.get()).expanduser()
        if not req.exists():
            messagebox.showerror(
                "File not found",
                f"Requirements file not found:\n{req}",
            )
            return

        command = self._pip_base() + ["install"]
        command += self._install_flags()
        command += ["-r", str(req)]
        self._run_command(command)

    def _open_requirements(self):
        req = Path(self.requirements_file.get()).expanduser()
        if not req.exists():
            messagebox.showerror("File not found", f"Not found:\n{req}")
            return

        try:
            if shutil.which("xdg-open"):
                subprocess.Popen(["xdg-open", str(req)])
            else:
                messagebox.showinfo(
                    "Requirements file",
                    req.read_text(encoding="utf-8", errors="replace"),
                )
        except Exception as exc:
            messagebox.showerror("Open failed", str(exc))

    # ---------- Package actions ----------

    def _get_packages(self):
        text = self.package_name.get().strip()
        if not text:
            messagebox.showwarning(
                "Package required",
                "Enter one or more package names first.",
            )
            return None
        return text.split()

    def _install_package(self):
        packages = self._get_packages()
        if not packages:
            return

        command = self._pip_base() + ["install"]
        if self.upgrade_package.get():
            command.append("--upgrade")
        command += self._install_flags()
        command += packages
        self._run_command(command)

    def _uninstall_package(self):
        packages = self._get_packages()
        if not packages:
            return

        if not messagebox.askyesno(
            "Confirm uninstall",
            "Uninstall:\n\n" + "\n".join(packages) + "?",
        ):
            return

        command = self._pip_base() + ["uninstall", "-y"] + packages
        self._run_command(command)

    def _show_package(self):
        packages = self._get_packages()
        if not packages:
            return
        self._run_command(self._pip_base() + ["show"] + packages)

    def _pip_list(self):
        self._run_command(self._pip_base() + ["list"])

    def _pip_outdated(self):
        self._run_command(self._pip_base() + ["list", "--outdated"])

    def _pip_check(self):
        self._run_command(self._pip_base() + ["check"])

    def _upgrade_pip(self):
        command = self._pip_base() + ["install", "--upgrade"]
        command += self._install_flags()
        command += ["pip"]
        self._run_command(command)

    # ---------- Utilities ----------

    def _show_versions(self):
        self._run_command([self._python(), "--version"])

        # Queue pip version after Python version with a tiny GUI-side delay.
        def later():
            if self.current_process is None:
                self._run_command(self._pip_base() + ["--version"])
            else:
                self.after(250, later)

        self.after(250, later)

    def _create_venv(self):
        folder = Path(self.project_dir.get()).expanduser()
        if not folder.exists():
            messagebox.showerror("Folder not found", f"Project folder not found:\n{folder}")
            return

        venv_dir = folder / ".venv"

        if venv_dir.exists():
            if not messagebox.askyesno(
                ".venv already exists",
                f"{venv_dir} already exists.\n\nCreate it again?",
            ):
                return

        self._run_command([self._python(), "-m", "venv", str(venv_dir)], cwd=str(folder))

    def _show_activate_command(self):
        folder = Path(self.project_dir.get()).expanduser()
        command = f"source {folder / '.venv' / 'bin' / 'activate'}"
        self._write_output(
            "\nVirtual environment activation command:\n"
            + command
            + "\n\n"
            "Note: activation changes the shell you run it in, so the GUI shows "
            "the command for you to paste into a terminal.\n"
        )
        self._set_preview(["source", str(folder / ".venv" / "bin" / "activate")])
        self.status_text.set("Activation command shown")

if __name__ == "__main__":
    app = PythonCommandCenter()
    app.mainloop()
