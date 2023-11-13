import tkinter as tk
from subprocess import Popen, PIPE

def execute_command():
    cmd = ["wget"]
    if timestamping_var.get():
        cmd += "--timestamping "
    if options["continue"]:
        cmd.append("-c")
    if options["no_directories"]:
        cmd.append("-nd")
    if options["recursive"]:
        cmd.append("-r")
    if options["level"]:
        cmd.extend(["-l", level_entry.get()])
    if options["robots_off"]:
        cmd.extend(["-e", "robots=off"])
    if options["random_wait"]:
        cmd.append("--random-wait")
    if options["page_requisites"]:
        cmd.append("-p")
    if options["user_agent"]:
        cmd.extend(["-U", user_agent_entry.get()])

    cmd.append(url_entry.get())

    process = Popen(cmd, stdout=PIPE, stderr=PIPE, text=True)
    output, error = process.communicate()
    output_text.insert(tk.END, output + error)

root = tk.Tk()

# Options Dictionary
options = {"no_directories": False, "recursive": False, "level": False, "robots_off": False, "random_wait": False, "page_requisites": False, "user_agent": False,}

# URL Entry
url_entry = tk.Entry(root)
url_entry.pack()

# Checkboxes and Entries for Options
options = {"continue": False}
continue_var = tk.BooleanVar()
continue_cb = tk.Checkbutton(root, text="Continue Partial Downloads", variable=continue_var, command=lambda: options.update({"continue": continue_var.get()}))
continue_cb.pack()
timestamping_var = tk.BooleanVar()
timestamping_cb = tk.Checkbutton(root, text="Timestamping", variable=timestamping_var)
timestamping_cb.pack()
# Execute Button
execute_button = tk.Button(root, text="Download", command=execute_command)
execute_button.pack()

# Output Text Box
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

no_directories_var = tk.BooleanVar()
no_directories_cb = tk.Checkbutton(root, text="No Directories (-nd)", variable=no_directories_var, command=lambda: options.update({"no_directories": no_directories_var.get()}))
no_directories_cb.pack()

recursive_var = tk.BooleanVar()
recursive_cb = tk.Checkbutton(root, text="Recursive (-r)", variable=recursive_var, command=lambda: options.update({"recursive": recursive_var.get()}))
recursive_cb.pack()

level_var = tk.BooleanVar()
level_cb = tk.Checkbutton(root, text="Level (-l)", variable=level_var, command=lambda: options.update({"level": level_var.get()}))
level_cb.pack()
level_entry = tk.Entry(root)
level_entry.pack()

robots_off_var = tk.BooleanVar()
robots_off_cb = tk.Checkbutton(root, text="Ignore Robots.txt (-e robots=off)", variable=robots_off_var, command=lambda: options.update({"robots_off": robots_off_var.get()}))
robots_off_cb.pack()

random_wait_var = tk.BooleanVar()
random_wait_cb = tk.Checkbutton(root, text="Random Wait (--random-wait)", variable=random_wait_var, command=lambda: options.update({"random_wait": random_wait_var.get()}))
random_wait_cb.pack()

page_requisites_var = tk.BooleanVar()
page_requisites_cb = tk.Checkbutton(root, text="Page Requisites (-p)", variable=page_requisites_var, command=lambda: options.update({"page_requisites": page_requisites_var.get()}))
page_requisites_cb.pack()

user_agent_var = tk.BooleanVar()
user_agent_cb = tk.Checkbutton(root, text="User Agent (-U)", variable=user_agent_var, command=lambda: options.update({"user_agent": user_agent_var.get()}))
user_agent_cb.pack()
user_agent_entry = tk.Entry(root)
user_agent_entry.pack()

# Execute Button
execute_button = tk.Button(root, text="Download", command=execute_command)
execute_button.pack()

# Output Text Box
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

root.mainloop()
