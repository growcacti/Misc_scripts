#!/usr/bin/env python3
import configparser, csv, json, os, shutil, subprocess, sys, threading
from dataclasses import dataclass, asdict
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

@dataclass
class Record:
    name: str
    version: str = ""
    kind: str = ""
    executable: str = ""
    location: str = ""
    description: str = ""

def run(args):
    try:
        return subprocess.run(args, text=True, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, timeout=45).stdout
    except (OSError, subprocess.SubprocessError):
        return ""

class App(tk.Tk):
    cols = ("name","version","kind","executable","location","description")
    def __init__(self):
        super().__init__()
        self.title("Linux Application Inventory")
        self.geometry("1250x720")
        self.minsize(900,500)
        self.records=[]; self.view=[]; self.rev={}; self.scanning=False
        s=ttk.Style(self)
        try: s.theme_use("clam")
        except tk.TclError: pass
        s.configure("Treeview", rowheight=25)
        s.configure("Treeview.Heading", font=("TkDefaultFont",10,"bold"))

        head=ttk.Frame(self,padding=10); head.pack(fill="x")
        ttk.Label(head,text="Linux Application Inventory",
                  font=("TkDefaultFont",16,"bold")).pack(side="left")

        bar=ttk.Frame(self,padding=(10,0,10,8)); bar.pack(fill="x")
        ttk.Label(bar,text="Search:").pack(side="left")
        self.q=tk.StringVar()
        ttk.Entry(bar,textvariable=self.q,width=32).pack(side="left",padx=(5,12))
        self.q.trace_add("write",lambda *_:self.filter())
        ttk.Label(bar,text="Type:").pack(side="left")
        self.kind=tk.StringVar(value="All")
        self.combo=ttk.Combobox(bar,textvariable=self.kind,state="readonly",
                                values=("All",),width=18)
        self.combo.pack(side="left",padx=(5,12))
        self.combo.bind("<<ComboboxSelected>>",lambda e:self.filter())
        ttk.Button(bar,text="Scan Again",command=self.scan).pack(side="left",padx=3)
        ttk.Button(bar,text="Export CSV",command=self.export_csv).pack(side="left",padx=3)
        ttk.Button(bar,text="Export JSON",command=self.export_json).pack(side="left",padx=3)
        ttk.Button(bar,text="Open Location",command=self.open_location).pack(side="left",padx=3)

        frame=ttk.Frame(self,padding=(10,0,10,5)); frame.pack(fill="both",expand=True)
        self.tree=ttk.Treeview(frame,columns=self.cols,show="headings")
        names={"name":"Name","version":"Version","kind":"Install Type",
               "executable":"Executable","location":"Location","description":"Description"}
        widths={"name":210,"version":100,"kind":120,"executable":220,"location":270,"description":330}
        for c in self.cols:
            self.tree.heading(c,text=names[c],command=lambda x=c:self.sort(x))
            self.tree.column(c,width=widths[c],minwidth=70)
        y=ttk.Scrollbar(frame,orient="vertical",command=self.tree.yview)
        x=ttk.Scrollbar(frame,orient="horizontal",command=self.tree.xview)
        self.tree.configure(yscrollcommand=y.set,xscrollcommand=x.set)
        self.tree.grid(row=0,column=0,sticky="nsew"); y.grid(row=0,column=1,sticky="ns")
        x.grid(row=1,column=0,sticky="ew")
        frame.rowconfigure(0,weight=1); frame.columnconfigure(0,weight=1)
        self.tree.bind("<Double-1>",lambda e:self.open_location())

        foot=ttk.Frame(self,padding=10); foot.pack(fill="x")
        self.status=tk.StringVar(value="Ready")
        ttk.Label(foot,textvariable=self.status).pack(side="left")
        self.progress=ttk.Progressbar(foot,mode="indeterminate",length=180)
        self.progress.pack(side="right")
        self.after(250,self.scan)

    def scan(self):
        if self.scanning:return
        self.scanning=True; self.progress.start(12); self.status.set("Scanning...")
        threading.Thread(target=self.worker,daemon=True).start()

    def worker(self):
        rows=[]
        for fn in (self.desktop,self.dpkg,self.flatpak,self.appimages,self.opt,self.localbin,self.pip):
            try: rows.extend(fn())
            except Exception: pass
        seen=set(); unique=[]
        for r in rows:
            k=tuple(str(getattr(r,c)).casefold() for c in self.cols)
            if k not in seen: seen.add(k); unique.append(r)
        unique.sort(key=lambda r:(r.name.casefold(),r.kind.casefold()))
        self.after(0,lambda:self.finish(unique))

    def finish(self,rows):
        self.records=rows
        self.combo["values"]=("All",*sorted({r.kind for r in rows}))
        self.scanning=False; self.progress.stop(); self.filter()

    def desktop(self):
        out=[]; seen=set()
        dirs=[Path("/usr/share/applications"),Path("/usr/local/share/applications"),
              Path.home()/".local/share/applications",
              Path("/var/lib/flatpak/exports/share/applications"),
              Path.home()/".local/share/flatpak/exports/share/applications"]
        for d in dirs:
            if not d.is_dir():continue
            for f in d.glob("*.desktop"):
                try:
                    cp=configparser.ConfigParser(interpolation=None,strict=False)
                    cp.optionxform=str; cp.read(f,encoding="utf-8")
                    s=cp["Desktop Entry"]
                    if s.get("Type","Application")!="Application" or s.get("NoDisplay","false").lower()=="true":continue
                    name=s.get("Name",f.stem); exe=s.get("Exec",""); key=(name.casefold(),exe)
                    if key in seen:continue
                    seen.add(key)
                    out.append(Record(name,"","Desktop App",exe,str(f),s.get("Comment","")))
                except Exception:pass
        return out

    def dpkg(self):
        if not shutil.which("dpkg-query"):return []
        fmt="${binary:Package}\\t${Version}\\t${db:Status-Abbrev}\\t${binary:Summary}\\n"
        rows=[]
        for line in run(["dpkg-query","-W",f"-f={fmt}"]).splitlines():
            p=line.split("\t",3)
            if len(p)>=3 and p[2].startswith("ii"):
                rows.append(Record(p[0],p[1],"APT/Debian","",
                                   "/var/lib/dpkg",p[3] if len(p)>3 else ""))
        return rows

    def flatpak(self):
        if not shutil.which("flatpak"):return []
        rows=[]
        text=run(["flatpak","list","--app","--columns=name,application,version,installation"])
        for line in text.splitlines():
            p=line.split("\t")+["","","",""]
            rows.append(Record(p[0] or p[1],p[2],"Flatpak",p[1],p[3],
                               ("Flatpak ID: "+p[1]) if p[1] else ""))
        return rows

    def appimages(self):
        rows=[]; seen=set(); checked=0
        roots=[Path.home(),Path("/opt"),Path("/mnt")]
        media=Path("/media")/os.environ.get("USER","")
        if media.exists():roots.append(media)
        for root in roots:
            if not root.exists():continue
            for cur,dirs,files in os.walk(root,onerror=lambda e:None):
                dirs[:]=[d for d in dirs if d not in {".cache",".git","node_modules",".Trash"}]
                for n in files:
                    checked+=1
                    if checked>150000:return rows
                    if n.lower().endswith(".appimage"):
                        p=str(Path(cur)/n)
                        if p not in seen:
                            seen.add(p); rows.append(Record(Path(n).stem,"","AppImage",p,cur,"Portable AppImage"))
        return rows

    def opt(self):
        root=Path("/opt"); rows=[]
        if root.is_dir():
            try:
                for p in root.iterdir():
                    rows.append(Record(p.name,"","/opt",str(p) if p.is_file() else "",str(p),
                                       "Manual/vendor installation under /opt"))
            except OSError:pass
        return rows

    def localbin(self):
        rows=[]
        for d in (Path("/usr/local/bin"),Path.home()/".local/bin"):
            if not d.is_dir():continue
            try:
                for p in d.iterdir():
                    if p.is_file() or p.is_symlink():
                        rows.append(Record(p.name,"","Local Executable",str(p),str(d),
                                           "Executable in a local bin directory"))
            except OSError:pass
        return rows

    def pip(self):
        text=run([sys.executable,"-m","pip","list","--format=json","--disable-pip-version-check"])
        try:data=json.loads(text)
        except Exception:return []
        return [Record(p.get("name",""),p.get("version",""),"Python/pip",
                       sys.executable,str(Path(sys.executable).parent),
                       "Python package") for p in data]

    def filter(self):
        q=self.q.get().casefold().strip(); k=self.kind.get()
        self.view=[r for r in self.records if (k=="All" or r.kind==k) and
                   (not q or q in " ".join(str(getattr(r,c)) for c in self.cols).casefold())]
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for r in self.view:self.tree.insert("", "end", values=tuple(getattr(r,c) for c in self.cols))
        self.status.set(f"Showing {len(self.view):,} of {len(self.records):,} entries")

    def sort(self,c):
        reverse=self.rev.get(c,False)
        self.view.sort(key=lambda r:str(getattr(r,c)).casefold(),reverse=reverse)
        self.rev[c]=not reverse; self.refresh()

    def selected(self):
        s=self.tree.selection()
        return self.tree.item(s[0],"values") if s else None

    def open_location(self):
        v=self.selected()
        if not v:return messagebox.showinfo("Open Location","Select an entry first.")
        for raw in (v[4],v[3]):
            if not raw:continue
            raw=str(raw).split()[0]
            p=Path(os.path.expanduser(raw))
            if p.exists():
                target=p if p.is_dir() else p.parent
                try:subprocess.Popen(["xdg-open",str(target)])
                except OSError as e:messagebox.showerror("Error",str(e))
                return
        messagebox.showinfo("Open Location","No filesystem location is available for this entry.")

    def export_csv(self):
        f=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV","*.csv")])
        if not f:return
        try:
            with open(f,"w",newline="",encoding="utf-8") as h:
                w=csv.writer(h); w.writerow(["Name","Version","Install Type","Executable","Location","Description"])
                for r in self.view:w.writerow(tuple(getattr(r,c) for c in self.cols))
            self.status.set(f"Exported {len(self.view):,} rows")
        except OSError as e:messagebox.showerror("Export",str(e))

    def export_json(self):
        f=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("JSON","*.json")])
        if not f:return
        try:
            with open(f,"w",encoding="utf-8") as h:json.dump([asdict(r) for r in self.view],h,indent=2)
            self.status.set(f"Exported {len(self.view):,} rows")
        except OSError as e:messagebox.showerror("Export",str(e))

if __name__=="__main__":
    App().mainloop()
