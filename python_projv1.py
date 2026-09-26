"""Cross-platform graphical tools for Python projects."""

import os
import queue
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


class PythonProjectManager(object):
    """Provide a graphical interface to selected Python project tools."""

    def __init__(self, root):
        self.root = root
        self.root.title("Python Project Manager")
        self.root.minsize(900, 650)
        self.events = queue.Queue()
        self.interpreters = {}
        self.active_process = None
        self.busy = False

        self.project_var = tk.StringVar(value=os.getcwd())
        self.script_var = tk.StringVar()
        self.venv_name_var = tk.StringVar(value=".venv")
        self.interpreter_var = tk.StringVar()
        self.package_var = tk.StringVar()
        self.remove_versions_var = tk.BooleanVar(value=True)
        self.onefile_var = tk.BooleanVar(value=True)

        self._create_widgets()
        self.refresh_interpreters()
        self._poll_events()

    def _create_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        target_frame = ttk.LabelFrame(self.root, text="Command Target")
        target_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        target_frame.columnconfigure(1, weight=1)
        ttk.Label(target_frame, text="Python interpreter:").grid(
            row=0, column=0, sticky="w", padx=(8, 5), pady=8)
        self.interpreter_box = ttk.Combobox(
            target_frame, textvariable=self.interpreter_var, state="readonly")
        self.interpreter_box.grid(row=0, column=1, sticky="ew", pady=8)
        ttk.Button(target_frame, text="Refresh", command=self.refresh_interpreters).grid(
            row=0, column=2, padx=8, pady=8)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self._create_project_tab()
        self._create_packages_tab()
        self._create_requirements_tab()
        self._create_build_tab()

        output_frame = ttk.LabelFrame(self.root, text="Command Output")
        output_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        output_frame.columnconfigure(0, weight=1)
        self.output = tk.Text(output_frame, height=12, wrap="word", state="disabled")
        self.output.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=8)
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 8), pady=8)
        self.output.configure(yscrollcommand=scrollbar.set)
        toolbar = ttk.Frame(output_frame)
        toolbar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8))
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(toolbar, textvariable=self.status_var).pack(side="left")
        ttk.Button(toolbar, text="Clear Output", command=self.clear_output).pack(side="right")
        self.stop_button = ttk.Button(toolbar, text="Stop Command", command=self.stop_command, state="disabled")
        self.stop_button.pack(side="right", padx=8)

    def _create_project_tab(self):
        frame = ttk.Frame(self.notebook, padding=12)
        frame.columnconfigure(1, weight=1)
        self.notebook.add(frame, text="Project and Environment")
        self._path_row(frame, 0, "Project folder:", self.project_var, self.choose_project)
        self._path_row(frame, 1, "Main script:", self.script_var, self.choose_script)
        ttk.Label(frame, text="Virtual environment folder:").grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(frame, textvariable=self.venv_name_var).grid(
            row=2, column=1, sticky="ew", pady=6)
        ttk.Button(frame, text="Create Project Folder", command=self.create_project).grid(
            row=3, column=0, sticky="w", pady=(12, 5))
        ttk.Button(frame, text="Create Virtual Environment", command=self.create_venv).grid(
            row=3, column=1, sticky="w", pady=(12, 5))
        ttk.Button(frame, text="Run Selected Script", command=self.run_selected_script).grid(
            row=4, column=0, sticky="w", pady=5)
        ttk.Button(frame, text="Activate in New Shell", command=self.open_activated_shell).grid(
            row=4, column=1, sticky="w", pady=5)
        ttk.Label(
            frame,
            text="Commands use .venv automatically when it exists. Activation only affects the new shell, not this program's parent terminal.",
            wraplength=760,
            justify="left"
        ).grid(row=5, column=0, columnspan=3, sticky="w", pady=(18, 0))

    def _create_packages_tab(self):
        frame = ttk.Frame(self.notebook, padding=12)
        frame.columnconfigure(0, weight=1)
        self.notebook.add(frame, text="Packages")
        ttk.Label(frame, text="Package names or pip arguments:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.package_var).grid(row=1, column=0, sticky="ew", pady=(4, 10))
        buttons = ttk.Frame(frame)
        buttons.grid(row=2, column=0, sticky="w")
        ttk.Button(buttons, text="Install", command=lambda: self.package_action("install")).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(buttons, text="Upgrade", command=lambda: self.package_action("install", "--upgrade")).grid(row=0, column=1, padx=5)
        ttk.Button(buttons, text="Uninstall", command=lambda: self.package_action("uninstall", "-y")).grid(row=0, column=2, padx=5)
        ttk.Button(buttons, text="Upgrade pip", command=self.upgrade_pip).grid(row=0, column=3, padx=5)
        ttk.Label(frame, text="Examples: requests Django>=5.0  or  -r requirements.txt", wraplength=760).grid(
            row=3, column=0, sticky="w", pady=(18, 0))

    def _create_requirements_tab(self):
        frame = ttk.Frame(self.notebook, padding=12)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)
        self.notebook.add(frame, text="Requirements")
        ttk.Checkbutton(frame, text="Remove version numbers from generated list", variable=self.remove_versions_var).grid(
            row=0, column=0, sticky="w")
        buttons = ttk.Frame(frame)
        buttons.grid(row=1, column=0, sticky="w", pady=8)
        ttk.Button(buttons, text="Freeze Target", command=self.freeze_requirements).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(buttons, text="Load requirements.txt", command=self.load_requirements).grid(row=0, column=1, padx=5)
        ttk.Button(buttons, text="Save requirements.txt", command=self.save_requirements).grid(row=0, column=2, padx=5)
        ttk.Button(buttons, text="Install Listed", command=self.install_listed).grid(row=0, column=3, padx=5)
        self.requirements = tk.Text(frame, wrap="none")
        self.requirements.grid(row=2, column=0, sticky="nsew")

    def _create_build_tab(self):
        frame = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(frame, text="Build and Compile")
        ttk.Button(frame, text="Compile Project to Bytecode", command=self.compile_bytecode).grid(row=0, column=0, sticky="w", pady=5)
        ttk.Checkbutton(frame, text="PyInstaller one-file executable", variable=self.onefile_var).grid(row=1, column=0, sticky="w", pady=5)
        ttk.Button(frame, text="Build with PyInstaller", command=self.pyinstaller).grid(row=2, column=0, sticky="w", pady=5)
        ttk.Button(frame, text="Create cx_Freeze setup.py", command=self.create_cx_freeze_setup).grid(row=3, column=0, sticky="w", pady=5)
        ttk.Button(frame, text="Build with cx_Freeze", command=self.cx_freeze).grid(row=4, column=0, sticky="w", pady=5)
        ttk.Button(frame, text="Compile with Nuitka", command=self.nuitka).grid(row=5, column=0, sticky="w", pady=5)
        ttk.Button(frame, text="Install Numba", command=lambda: self.package_action("install", "numba")).grid(row=6, column=0, sticky="w", pady=5)
        ttk.Label(
            frame,
            text="PyInstaller, cx_Freeze, Nuitka, and Numba must be installed in the selected target. Numba accelerates code only after its decorators are added to your program.",
            wraplength=760,
            justify="left"
        ).grid(row=7, column=0, sticky="w", pady=(18, 0))

    @staticmethod
    def _path_row(frame, row, label, variable, command):
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(frame, textvariable=variable).grid(row=row, column=1, sticky="ew", pady=6)
        ttk.Button(frame, text="Browse", command=command).grid(row=row, column=2, padx=(8, 0), pady=6)

    def refresh_interpreters(self):
        candidates = [sys.executable]
        if os.name == "nt" and shutil.which("py"):
            try:
                output = subprocess.check_output(["py", "-0p"], stderr=subprocess.STDOUT, universal_newlines=True)
                for line in output.splitlines():
                    match = re.search(r"([A-Za-z]:\\.+python\.exe)$", line.strip(), re.IGNORECASE)
                    if match:
                        candidates.append(match.group(1))
            except (OSError, subprocess.CalledProcessError):
                pass
        for executable in ("python", "python3", "python3.14", "python3.13", "python3.12", "python3.11", "python3.10"):
            path = shutil.which(executable)
            if path:
                candidates.append(path)

        self.interpreters = {}
        for path in candidates:
            path = os.path.realpath(path)
            if not os.path.isfile(path) or path in self.interpreters.values():
                continue
            try:
                version = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, universal_newlines=True).strip()
            except (OSError, subprocess.CalledProcessError):
                continue
            self.interpreters["{0} ({1})".format(version, path)] = path
        values = list(self.interpreters)
        self.interpreter_box["values"] = values
        if values and self.interpreter_var.get() not in self.interpreters:
            self.interpreter_var.set(values[0])
        self.log("Found {0} usable Python interpreter(s).".format(len(values)))

    def choose_project(self):
        path = filedialog.askdirectory(initialdir=self.project_var.get() or os.getcwd())
        if path:
            self.project_var.set(path)

    def choose_script(self):
        path = filedialog.askopenfilename(initialdir=self.project_var.get() or os.getcwd(), filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if path:
            self.script_var.set(path)
            self.project_var.set(os.path.dirname(path))

    def project_path(self):
        path = self.project_var.get().strip()
        return os.path.abspath(os.path.expanduser(path)) if path else os.getcwd()

    def venv_path(self):
        name = self.venv_name_var.get().strip() or ".venv"
        path = Path(name).expanduser()
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("Use a virtual environment folder within the project (no '..').")
        return os.path.join(self.project_path(), str(path))

    def target_python(self):
        executable = "python.exe" if os.name == "nt" else "python"
        try:
            venv = self.venv_path()
        except ValueError:
            return None
        venv_python = os.path.join(venv, "Scripts" if os.name == "nt" else "bin", executable)
        if os.path.isfile(venv_python):
            return venv_python
        return self.interpreters.get(self.interpreter_var.get())

    def create_project(self):
        path = self.project_path()
        try:
            os.makedirs(path, exist_ok=True)
            self.log("Project folder is ready: {0}".format(path))
        except OSError as error:
            messagebox.showerror("Project Folder", str(error))

    def create_venv(self):
        try:
            venv = self.venv_path()
        except ValueError as error:
            messagebox.showerror("Virtual Environment", str(error))
            return
        python = self.interpreters.get(self.interpreter_var.get())
        if not python:
            messagebox.showerror("No Python", "Select a usable Python interpreter first.")
            return
        if os.path.exists(venv):
            messagebox.showwarning("Virtual Environment", "The selected virtual environment folder already exists.")
            return
        try:
            os.makedirs(self.project_path(), exist_ok=True)
        except OSError as error:
            messagebox.showerror("Project Folder", str(error))
            return
        self.run_command([python, "-m", "venv", venv], "Create virtual environment")

    def open_activated_shell(self):
        try:
            venv = self.venv_path()
        except ValueError as error:
            messagebox.showerror("Virtual Environment", str(error))
            return
        if not os.path.isfile(os.path.join(venv, "Scripts" if os.name == "nt" else "bin", "python.exe" if os.name == "nt" else "python")):
            messagebox.showwarning("Virtual Environment", "Create the project's virtual environment first.")
            return
        try:
            if os.name == "nt":
                activate = os.path.join(venv, "Scripts", "activate.bat")
                subprocess.Popen(["cmd.exe", "/K", '"' + activate + '"'], cwd=self.project_path(), creationflags=subprocess.CREATE_NEW_CONSOLE)
            elif sys.platform == "darwin":
                activate = os.path.join(venv, "bin", "activate")
                script = 'cd {0}; . {1}; exec "${{SHELL:-/bin/sh}}"'.format(shlex.quote(self.project_path()), shlex.quote(activate))
                subprocess.Popen(["osascript", "-e", 'tell application "Terminal" to do script ' + self._applescript_quote(script)])
            else:
                activate = os.path.join(venv, "bin", "activate")
                shell = os.environ.get("SHELL", "/bin/sh")
                script = '. {0}; exec {1} -i'.format(shlex.quote(activate), shlex.quote(shell))
                terminals = (("x-terminal-emulator", ["-e", "sh", "-c", script]), ("gnome-terminal", ["--", "sh", "-c", script]), ("konsole", ["-e", "sh", "-c", script]), ("xfce4-terminal", ["--command", 'sh -c ' + shlex.quote(script)]))
                for terminal, args in terminals:
                    executable = shutil.which(terminal)
                    if executable:
                        subprocess.Popen([executable] + args, cwd=self.project_path())
                        break
                else:
                    raise OSError("No supported terminal emulator found. Run: . " + shlex.quote(activate))
        except OSError as error:
            messagebox.showerror("Open Shell", str(error))

    @staticmethod
    def _applescript_quote(value):
        return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'

    def package_action(self, action, option=None):
        package_text = self.package_var.get().strip()
        if not package_text:
            messagebox.showwarning("Package", "Enter one or more package names or pip arguments.")
            return
        command = [self.target_python(), "-m", "pip", action]
        if option:
            command.append(option)
        try:
            command.extend(shlex.split(package_text, posix=os.name != "nt"))
        except ValueError as error:
            messagebox.showerror("Package Arguments", str(error))
            return
        self.run_command(command, "pip {0}".format(action))

    def upgrade_pip(self):
        self.run_command([self.target_python(), "-m", "pip", "install", "--upgrade", "pip"], "Upgrade pip")

    def freeze_requirements(self):
        self.run_command([self.target_python(), "-m", "pip", "freeze"], "Freeze requirements", self._show_frozen_requirements)

    def _show_frozen_requirements(self, returncode, output):
        if returncode:
            return
        lines = output.splitlines()
        if self.remove_versions_var.get():
            lines = [self.remove_version_information(line) for line in lines]
        lines = sorted(set(line.strip() for line in lines if line.strip()))
        self.requirements.delete("1.0", tk.END)
        self.requirements.insert("1.0", "\n".join(lines))

    @staticmethod
    def remove_version_information(line):
        line = line.strip()
        if line.startswith("#"):
            return line
        if " @ " in line:
            return line.split(" @ ", 1)[0].strip()
        return re.split(r"(===|==|>=|<=|!=|~=|>|<)", line, 1)[0].strip()

    def load_requirements(self):
        path = filedialog.askopenfilename(initialdir=self.project_path(), filetypes=[("Requirements files", "*.txt *.in"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as source:
                content = source.read()
        except OSError as error:
            messagebox.showerror("Load Failed", str(error))
            return
        self.requirements.delete("1.0", tk.END)
        self.requirements.insert("1.0", content)

    def save_requirements(self):
        content = self.requirements.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Requirements", "There are no requirements to save.")
            return
        path = filedialog.asksaveasfilename(initialdir=self.project_path(), initialfile="requirements.txt", defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as target:
                target.write(content + "\n")
            self.log("Saved requirements: {0}".format(path))
        except OSError as error:
            messagebox.showerror("Save Failed", str(error))

    def install_listed(self):
        content = self.requirements.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Requirements", "There are no requirements to install.")
            return
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".txt", prefix="project-requirements-", delete=False) as target:
                target.write(content + "\n")
                path = target.name
        except OSError as error:
            messagebox.showerror("Requirements", str(error))
            return
        self.run_command([self.target_python(), "-m", "pip", "install", "-r", path], "Install listed requirements", cleanup=path)

    def script_or_warn(self):
        path = self.script_var.get().strip()
        if not path or not os.path.isfile(path):
            messagebox.showwarning("Main Script", "Choose an existing Python script in the Project and Environment tab.")
            return None
        return os.path.abspath(path)

    def run_selected_script(self):
        script = self.script_or_warn()
        if script:
            self.run_command([self.target_python(), script], "Run selected script")

    def compile_bytecode(self):
        self.run_command([self.target_python(), "-m", "compileall", self.project_path()], "Compile bytecode")

    def pyinstaller(self):
        script = self.script_or_warn()
        if script:
            command = [self.target_python(), "-m", "PyInstaller", "--noconfirm"]
            if self.onefile_var.get():
                command.append("--onefile")
            command.append(script)
            self.run_command(command, "Build with PyInstaller")

    def create_cx_freeze_setup(self):
        script = self.script_or_warn()
        if not script:
            return
        path = os.path.join(self.project_path(), "setup.py")
        if os.path.exists(path) and not messagebox.askyesno("Replace setup.py", "setup.py already exists. Replace it?"):
            return
        content = "from cx_Freeze import Executable, setup\n\nsetup(\n    name={0!r},\n    version='0.1',\n    description='',\n    executables=[Executable({1!r})],\n)\n".format(os.path.splitext(os.path.basename(script))[0], os.path.relpath(script, self.project_path()))
        try:
            with open(path, "w", encoding="utf-8") as target:
                target.write(content)
            self.log("Created cx_Freeze setup script: {0}".format(path))
        except OSError as error:
            messagebox.showerror("cx_Freeze", str(error))

    def cx_freeze(self):
        setup = os.path.join(self.project_path(), "setup.py")
        if not os.path.isfile(setup):
            messagebox.showwarning("cx_Freeze", "Create or provide setup.py first.")
            return
        self.run_command([self.target_python(), setup, "build"], "Build with cx_Freeze")

    def nuitka(self):
        script = self.script_or_warn()
        if script:
            self.run_command([self.target_python(), "-m", "nuitka", "--standalone", script], "Compile with Nuitka")

    def run_command(self, command, title, callback=None, cleanup=None):
        if self.busy:
            if cleanup:
                os.unlink(cleanup)
            messagebox.showinfo("Command Running", "Stop or finish the current command first.")
            return
        if not command[0]:
            if cleanup:
                os.unlink(cleanup)
            messagebox.showerror("No Python", "Select a usable Python interpreter first.")
            return
        if not os.path.isdir(self.project_path()):
            if cleanup:
                os.unlink(cleanup)
            messagebox.showerror("Project Folder", "Choose an existing project folder first.")
            return
        self.busy = True
        self.status_var.set("Running: " + title)
        self.stop_button.configure(state="normal")
        self.log("\n[{0}]\n{1}\n".format(title, subprocess.list2cmdline(command) if os.name == "nt" else shlex.join(command)))
        thread = threading.Thread(target=self._run_worker, args=(command, title, callback, cleanup), daemon=True)
        thread.start()

    def _run_worker(self, command, title, callback, cleanup):
        try:
            process = subprocess.Popen(command, cwd=self.project_path(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace", bufsize=1)
            self.active_process = process
            collected = [] if callback else None
            for line in process.stdout:
                self.events.put(("line", line))
                if collected is not None:
                    collected.append(line)
            process.wait()
            self.events.put(("complete", title, process.returncode, "".join(collected or []), callback))
        except (OSError, ValueError) as error:
            self.events.put(("complete", title, 1, str(error), callback))
        finally:
            self.active_process = None
            if cleanup:
                try:
                    os.unlink(cleanup)
                except OSError:
                    pass

    def _poll_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                if event[0] == "line":
                    self.log(event[1])
                    continue
                _, title, returncode, output, callback = event
                if returncode and output and callback:
                    self.log(output)
                self.log("[{0}: {1}]\n".format(title, "completed" if returncode == 0 else "failed"))
                self.busy = False
                self.status_var.set("Ready" if returncode == 0 else "Command failed")
                self.stop_button.configure(state="disabled")
                if callback:
                    callback(returncode, output)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_events)

    def stop_command(self):
        process = self.active_process
        if process and process.poll() is None:
            process.terminate()
            self.status_var.set("Stopping command…")

    def clear_output(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.configure(state="disabled")

    def log(self, text):
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + ("" if text.endswith("\n") else "\n"))
        self.output.see(tk.END)
        self.output.configure(state="disabled")


def main():
    root = tk.Tk()
    PythonProjectManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
