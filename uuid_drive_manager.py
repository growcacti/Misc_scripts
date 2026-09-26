#!/usr/bin/env python3
import tkinter as tk, uuid, csv, secrets, json, subprocess, shutil
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timezone

def u7():
 m=int(datetime.now(timezone.utc).timestamp()*1000)&((1<<48)-1); return uuid.UUID(int=(m<<80)|(7<<76)|(secrets.randbits(12)<<64)|(2<<62)|secrets.randbits(62))
def u8():
 v=secrets.randbits(128); v=(v&~(15<<76))|(8<<76); v=(v&~(3<<62))|(2<<62); return uuid.UUID(int=v)
def u6():
 u=uuid.uuid1();t=u.time;v=((t>>28)<<96)|(((t>>12)&65535)<<80)|(6<<76)|((t&4095)<<64)|(2<<62)|((u.clock_seq&16383)<<48)|u.node;return uuid.UUID(int=v)

class App(tk.Tk):
 def __init__(self):
  super().__init__();self.title('UUID Toolbox');self.geometry('1000x700');self.minsize(820,580);self.hist=[]
  self.status=tk.StringVar(value='Ready');self.upper=tk.BooleanVar();self.hyph=tk.BooleanVar(value=True)
  try: ttk.Style(self).theme_use('clam')
  except: pass
  self.columnconfigure(0,weight=1);self.rowconfigure(1,weight=1)
  h=ttk.Frame(self,padding=10);h.grid(sticky='ew');ttk.Label(h,text='UUID Toolbox',font=('TkDefaultFont',16,'bold')).pack(anchor='w');ttk.Label(h,text='Generate • Validate • Edit • Convert • Compare • Export').pack(anchor='w')
  self.nb=ttk.Notebook(self);self.nb.grid(row=1,column=0,sticky='nsew',padx=10,pady=5)
  self.gen_tab();self.val_tab();self.edit_tab();self.conv_tab();self.cmp_tab();self.usb_tab();self.history_tab();self.help_tab()
  ttk.Label(self,textvariable=self.status,relief='sunken',anchor='w',padding=5).grid(row=2,column=0,sticky='ew')
 def tab(self,n):
  f=ttk.Frame(self.nb,padding=12);self.nb.add(f,text=n);f.columnconfigure(0,weight=1);return f
 def cp(self,s): self.clipboard_clear();self.clipboard_append(s);self.status.set('Copied to clipboard')
 def add(self,a,u):
  r=(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),a,str(u));self.hist.append(r)
  if hasattr(self,'tree'):self.tree.insert('',0,values=r)
 def settext(self,w,s):w.config(state='normal');w.delete('1.0','end');w.insert('1.0',s);w.config(state='disabled')
 def ns(self):
  d={'DNS':uuid.NAMESPACE_DNS,'URL':uuid.NAMESPACE_URL,'OID':uuid.NAMESPACE_OID,'X500':uuid.NAMESPACE_X500};return uuid.UUID(self.custom.get()) if self.nsv.get()=='Custom' else d[self.nsv.get()]
 def make(self,v):
  if v=='v1':return uuid.uuid1()
  if v=='v3':return uuid.uuid3(self.ns(),self.name.get())
  if v=='v4':return uuid.uuid4()
  if v=='v5':return uuid.uuid5(self.ns(),self.name.get())
  return {'v6':u6,'v7':u7,'v8':u8}[v]()
 def form(self,u):
  s=str(u) if self.hyph.get() else u.hex;return s.upper() if self.upper.get() else s
 def gen_tab(self):
  f=self.tab('Generator');c=ttk.LabelFrame(f,text='Generation',padding=8);c.grid(sticky='ew')
  ttk.Label(c,text='Version').grid(row=0,column=0);self.ver=ttk.Combobox(c,values=['v1','v3','v4','v5','v6','v7','v8'],state='readonly',width=7);self.ver.set('v4');self.ver.grid(row=0,column=1,padx=5)
  ttk.Label(c,text='Count').grid(row=0,column=2);self.count=tk.Spinbox(c,from_=1,to=10000,width=7);self.count.delete(0,'end');self.count.insert(0,'1');self.count.grid(row=0,column=3,padx=5);ttk.Button(c,text='Generate',command=self.generate).grid(row=0,column=4)
  n=ttk.LabelFrame(f,text='v3/v5 name-based options',padding=8);n.grid(row=1,column=0,sticky='ew',pady=6);n.columnconfigure(3,weight=1);self.nsv=ttk.Combobox(n,values=['DNS','URL','OID','X500','Custom'],state='readonly',width=9);self.nsv.set('DNS');self.nsv.grid(row=0,column=1);ttk.Label(n,text='Namespace').grid(row=0,column=0);ttk.Label(n,text='Name').grid(row=0,column=2);self.name=ttk.Entry(n);self.name.insert(0,'example.com');self.name.grid(row=0,column=3,sticky='ew');ttk.Label(n,text='Custom namespace UUID').grid(row=1,column=0,columnspan=2,sticky='w');self.custom=ttk.Entry(n);self.custom.grid(row=1,column=2,columnspan=2,sticky='ew')
  o=ttk.Frame(f);o.grid(row=2,column=0,sticky='w');ttk.Checkbutton(o,text='Uppercase',variable=self.upper).pack(side='left');ttk.Checkbutton(o,text='Hyphens',variable=self.hyph).pack(side='left',padx=10)
  self.out=tk.Text(f,font=('TkFixedFont',10),wrap='none');self.out.grid(row=3,column=0,sticky='nsew',pady=6);f.rowconfigure(3,weight=1)
  b=ttk.Frame(f);b.grid(row=4,column=0,sticky='w');ttk.Button(b,text='Copy All',command=lambda:self.cp(self.out.get('1.0','end-1c'))).pack(side='left');ttk.Button(b,text='Save TXT',command=self.save_txt).pack(side='left',padx=5);ttk.Button(b,text='Save CSV',command=self.save_csv).pack(side='left')
 def generate(self):
  try:
   n=int(self.count.get());assert 1<=n<=10000;z=[]
   for _ in range(n):u=self.make(self.ver.get());z.append(self.form(u));self.add('Generated '+self.ver.get(),u)
   self.out.delete('1.0','end');self.out.insert('1.0','\n'.join(z));self.status.set(f'Generated {n} UUID(s)')
  except Exception as e:messagebox.showerror('UUID Toolbox',str(e))
 def val_tab(self):
  f=self.tab('Validate / Inspect');self.val=ttk.Entry(f,font=('TkFixedFont',11));self.val.grid(sticky='ew');ttk.Button(f,text='Validate & Inspect',command=self.validate).grid(row=1,column=0,sticky='w',pady=6);self.info=tk.Text(f,font=('TkFixedFont',10),state='disabled');self.info.grid(row=2,column=0,sticky='nsew');f.rowconfigure(2,weight=1)
 def validate(self):
  try:
   u=uuid.UUID(self.val.get().strip());s=f'VALID UUID\n\nCanonical : {u}\nHex       : {u.hex}\nURN       : {u.urn}\nVersion   : {u.version}\nVariant   : {u.variant}\nInteger   : {u.int}\nBytes     : {u.bytes!r}\nFields    : {u.fields}';self.settext(self.info,s);self.add('Validated',u);self.status.set('UUID is valid')
  except Exception as e:self.settext(self.info,'INVALID UUID\n\n'+str(e));self.status.set('Invalid UUID')
 def edit_tab(self):
  f=self.tab('Editor');ttk.Label(f,text='Editing any digit creates a NEW UUID.').grid(sticky='w');self.src=ttk.Entry(f,font=('TkFixedFont',11));self.src.grid(row=1,column=0,sticky='ew',pady=5);ttk.Button(f,text='Load UUID',command=self.loadedit).grid(row=2,column=0,sticky='w');g=ttk.Frame(f);g.grid(row=3,column=0,pady=12);self.groups=[]
  for i,w in enumerate([8,4,4,4,12]):
   e=ttk.Entry(g,width=w+2,font=('TkFixedFont',12),justify='center');e.grid(row=0,column=i*2);self.groups.append(e)
   if i<4:ttk.Label(g,text='-').grid(row=0,column=i*2+1)
  ttk.Button(f,text='Build New UUID',command=self.buildedit).grid(row=4,column=0,sticky='w');self.edres=tk.StringVar();ttk.Entry(f,textvariable=self.edres,state='readonly',font=('TkFixedFont',12)).grid(row=5,column=0,sticky='ew',pady=8);ttk.Button(f,text='Copy Result',command=lambda:self.cp(self.edres.get())).grid(row=6,column=0,sticky='w')
 def loadedit(self):
  try:
   u=uuid.UUID(self.src.get().strip())
   for e,p in zip(self.groups,str(u).split('-')):e.delete(0,'end');e.insert(0,p)
   self.edres.set(str(u))
  except Exception as e:messagebox.showerror('UUID Toolbox',str(e))
 def buildedit(self):
  try:
   ps=[]
   for e,n in zip(self.groups,[8,4,4,4,12]):
    p=e.get().strip()
    if len(p)!=n or any(c not in '0123456789abcdefABCDEF' for c in p):raise ValueError('Groups must contain exactly 8-4-4-4-12 hex digits.')
    ps.append(p)
   u=uuid.UUID('-'.join(ps));self.edres.set(self.form(u));self.add('Edited/new',u);self.status.set('New UUID built')
  except Exception as e:messagebox.showerror('UUID Toolbox',str(e))
 def conv_tab(self):
  f=self.tab('Converter');ttk.Label(f,text='UUID / 32-digit hex / decimal 128-bit integer').grid(sticky='w');self.cv=ttk.Entry(f,font=('TkFixedFont',11));self.cv.grid(row=1,column=0,sticky='ew',pady=5);ttk.Button(f,text='Convert',command=self.convert).grid(row=2,column=0,sticky='w');self.cvo=tk.Text(f,state='disabled',font=('TkFixedFont',10));self.cvo.grid(row=3,column=0,sticky='nsew',pady=6);f.rowconfigure(3,weight=1)
 def convert(self):
  try:
   s=self.cv.get().strip();u=uuid.UUID(int=int(s)) if s.isdigit() else uuid.UUID(s);self.settext(self.cvo,f'Canonical : {u}\nHex       : {u.hex}\nInteger   : {u.int}\nBytes     : {u.bytes!r}\nURN       : {u.urn}\nVersion   : {u.version}\nVariant   : {u.variant}');self.add('Converted',u)
  except Exception as e:messagebox.showerror('UUID Toolbox',str(e))
 def cmp_tab(self):
  f=self.tab('Compare');self.a=ttk.Entry(f,font=('TkFixedFont',11));self.b=ttk.Entry(f,font=('TkFixedFont',11));ttk.Label(f,text='UUID A').grid(sticky='w');self.a.grid(row=1,column=0,sticky='ew');ttk.Label(f,text='UUID B').grid(row=2,column=0,sticky='w');self.b.grid(row=3,column=0,sticky='ew');ttk.Button(f,text='Compare',command=self.compare).grid(row=4,column=0,sticky='w',pady=6);self.co=tk.Text(f,state='disabled',font=('TkFixedFont',10));self.co.grid(row=5,column=0,sticky='nsew');f.rowconfigure(5,weight=1)
 def compare(self):
  try:
   a,b=uuid.UUID(self.a.get().strip()),uuid.UUID(self.b.get().strip());d=[str(i+1) for i,(x,y) in enumerate(zip(a.hex,b.hex)) if x!=y];self.settext(self.co,f'A: {a}\nB: {b}\n\nEqual: {a==b}\nDifferent hex digits: {len(d)} of 32\nPositions: {", ".join(d) if d else "none"}\n\nA version: {a.version}\nB version: {b.version}')
  except Exception as e:messagebox.showerror('UUID Toolbox',str(e))
 def usb_tab(self):
  f=self.tab('USB / Drives');f.rowconfigure(1,weight=1)
  ttk.Label(f,text='Inspect USB/removable storage identifiers (read-only inspection).').grid(row=0,column=0,sticky='w')
  cols=('device','type','size','fstype','label','uuid','partuuid','serial','model','mount','editable');self.usbtree=ttk.Treeview(f,columns=cols,show='headings')
  heads=['Device','Type','Size','FS','Label','Filesystem UUID','PARTUUID','Serial','Model','Mount','Editable?'];widths=[100,60,75,70,110,235,190,130,160,180,160]
  for c,h,w in zip(cols,heads,widths):self.usbtree.heading(c,text=h);self.usbtree.column(c,width=w,minwidth=55)
  self.usbtree.grid(row=1,column=0,sticky='nsew',pady=6);xs=ttk.Scrollbar(f,orient='horizontal',command=self.usbtree.xview);xs.grid(row=2,column=0,sticky='ew');self.usbtree.configure(xscrollcommand=xs.set)
  b=ttk.Frame(f);b.grid(row=3,column=0,sticky='w');ttk.Button(b,text='Refresh Drives',command=self.scan_usb).pack(side='left');ttk.Button(b,text='Copy Filesystem UUID',command=lambda:self.copy_usb_col(5)).pack(side='left',padx=4);ttk.Button(b,text='Copy PARTUUID',command=lambda:self.copy_usb_col(6)).pack(side='left');ttk.Button(b,text='Copy Serial',command=lambda:self.copy_usb_col(7)).pack(side='left',padx=4);ttk.Button(b,text='Export CSV',command=self.export_usb).pack(side='left');ttk.Button(b,text='Advanced Editor',command=self.advanced_drive_editor).pack(side='left',padx=4)
  self.usbinfo=tk.Text(f,height=9,wrap='word',state='disabled');self.usbinfo.grid(row=4,column=0,sticky='ew',pady=6);self.usbtree.bind('<<TreeviewSelect>>',self.usb_details);self.scan_usb()
 def scan_usb(self):
  self.usbtree.delete(*self.usbtree.get_children())
  if not shutil.which('lsblk'):self.settext(self.usbinfo,'USB drive inspection currently requires Linux lsblk. The Advanced Editor targets Linux filesystem tools.');return
  try:
   data=json.loads(subprocess.check_output(['lsblk','-J','-o','NAME,PATH,TYPE,SIZE,FSTYPE,LABEL,UUID,PARTUUID,SERIAL,MODEL,MOUNTPOINTS,RM,TRAN'],text=True,stderr=subprocess.STDOUT))
   def walk(x,parent=False,serial='',model=''):
    isusb=parent or x.get('tran')=='usb' or bool(x.get('rm'));serial=x.get('serial') or serial or '';model=x.get('model') or model or ''
    if isusb:
     fs=x.get('fstype') or '';mount=', '.join(str(m) for m in (x.get('mountpoints') or []) if m);vals=(x.get('path') or '',x.get('type') or '',x.get('size') or '',fs,x.get('label') or '',x.get('uuid') or '',x.get('partuuid') or '',serial,model.strip(),mount,self.drive_editability(fs,x.get('type') or ''));self.usbtree.insert('', 'end',values=vals)
    for ch in x.get('children') or []:walk(ch,isusb,serial,model)
   for d in data.get('blockdevices',[]):walk(d)
   self.status.set('USB/removable drive scan complete')
  except Exception as e:self.settext(self.usbinfo,'Unable to inspect drives:\n'+str(e))
 def drive_editability(self,fs,typ):
  if typ=='disk':return 'Hardware IDs: usually no'
  return {'ext2':'UUID/label: yes','ext3':'UUID/label: yes','ext4':'UUID/label: yes','vfat':'Label; ID tool-specific','fat':'Label; ID tool-specific','exfat':'Label; serial tool-specific','ntfs':'Label; UUID tool-specific','xfs':'UUID/label: yes','btrfs':'UUID/label: advanced'}.get(fs.lower(),'Inspect filesystem tools') if fs else 'Partition metadata only'
 def usb_selected(self):
  s=self.usbtree.selection();return self.usbtree.item(s[0])['values'] if s else None
 def copy_usb_col(self,i):
  v=self.usb_selected();self.cp(str(v[i])) if v and str(v[i]) else messagebox.showinfo('UUID Toolbox','Select a row containing that identifier first.')
 def usb_details(self,event=None):
  v=self.usb_selected()
  if not v:return
  text='DEVICE EVALUATION\n\nDevice: {}\nType: {}    Size: {}    Filesystem: {}\nLabel: {}\nFilesystem UUID: {}\nPARTUUID: {}\nHardware serial: {}\nModel: {}\nMounted at: {}\n\nEditability: {}\n\nFilesystem UUID/label changes require filesystem-specific utilities and normally an unmounted filesystem. PARTUUID is partition-table metadata. Hardware USB serial/model identifiers are device/controller information and are not treated as normal editable fields. Back up important data before changing on-disk identifiers.'.format(*v)
  self.settext(self.usbinfo,text)
 def advanced_drive_editor(self):
  v=self.usb_selected()
  if not v:
   messagebox.showinfo('UUID Toolbox','Select a filesystem/partition row first.');return
  dev,typ,size,fs,label,fsuuid,partuuid,serial,model,mount,editable=v
  if typ=='disk' or not fs:
   messagebox.showinfo('UUID Toolbox','Select a partition containing a recognized filesystem. Hardware serial/model fields are inspection-only.');return
  w=tk.Toplevel(self);w.title('Advanced Drive Metadata Editor');w.geometry('760x520');w.transient(self)
  w.columnconfigure(1,weight=1)
  fields=[('Device',dev),('Filesystem',fs),('Current label',label),('Current filesystem UUID/ID',fsuuid),('PARTUUID',partuuid),('Hardware serial',serial)]
  for r,(a,b) in enumerate(fields):ttk.Label(w,text=a+':').grid(row=r,column=0,sticky='w',padx=10,pady=4);ttk.Label(w,text=b or '(none)',font=('TkFixedFont',10)).grid(row=r,column=1,sticky='w',padx=10)
  ttk.Separator(w).grid(row=6,column=0,columnspan=2,sticky='ew',pady=8)
  ttk.Label(w,text='New volume label:').grid(row=7,column=0,sticky='w',padx=10);lab=ttk.Entry(w);lab.insert(0,label);lab.grid(row=7,column=1,sticky='ew',padx=10)
  ttk.Label(w,text='New filesystem UUID/ID:').grid(row=8,column=0,sticky='w',padx=10);uid=ttk.Entry(w);uid.insert(0,fsuuid);uid.grid(row=8,column=1,sticky='ew',padx=10)
  preview=tk.Text(w,height=9,font=('TkFixedFont',9),state='disabled',wrap='word');preview.grid(row=10,column=0,columnspan=2,sticky='nsew',padx=10,pady=8);w.rowconfigure(10,weight=1)
  def plan():
   cmds=[];f=fs.lower();nl=lab.get().strip();nu=uid.get().strip()
   if mount: cmds.append('# UNMOUNT REQUIRED before metadata changes: '+dev)
   if nl!=label:
    if f in ('ext2','ext3','ext4'):cmds.append('e2label '+dev+' '+repr(nl))
    elif f=='xfs':cmds.append('xfs_admin -L '+repr(nl)+' '+dev)
    elif f=='exfat':cmds.append('exfatlabel '+dev+' '+repr(nl))
    elif f in ('vfat','fat','fat32'):cmds.append('fatlabel '+dev+' '+repr(nl))
    elif f=='ntfs':cmds.append('ntfslabel '+dev+' '+repr(nl))
    else:cmds.append('# Label editing not configured for '+fs)
   if nu!=fsuuid:
    if f in ('ext2','ext3','ext4'):cmds.append('tune2fs -U '+nu+' '+dev)
    elif f=='xfs':cmds.append('xfs_admin -U '+nu+' '+dev)
    else:cmds.append('# UUID/volume-ID writing is not enabled for '+fs+' in this safety-focused version.')
   if not cmds:cmds=['# No metadata changes entered.']
   self.settext(preview,'COMMAND PREVIEW — NOT EXECUTED\n\n'+'\n'.join(cmds)+'\n\nThis preview is intentionally non-destructive. Hardware serial/model identifiers are not modified.')
  def randomid():
   f=fs.lower()
   if f in ('ext2','ext3','ext4','xfs'):uid.delete(0,'end');uid.insert(0,str(uuid.uuid4()))
   else:messagebox.showinfo('UUID Toolbox','Automatic random UUID generation is enabled here for ext-family and XFS filesystems. Other filesystems use different volume-ID formats/tools.')
  buttons=ttk.Frame(w);buttons.grid(row=9,column=0,columnspan=2,sticky='w',padx=10,pady=8)
  ttk.Button(buttons,text='Generate Random UUID',command=randomid).pack(side='left');ttk.Button(buttons,text='Preview Changes',command=plan).pack(side='left',padx=5);ttk.Button(buttons,text='Close',command=w.destroy).pack(side='left')
  self.settext(preview,'Select changes above and click Preview Changes.\n\nFor safety, this editor does not automatically run privileged disk-modification commands. It identifies the appropriate operation so you can evaluate the drive first.')

 def export_usb(self):
  p=filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV','*.csv')])
  if not p:return
  with open(p,'w',newline='',encoding='utf-8') as q:
   w=csv.writer(q);w.writerow(['Device','Type','Size','Filesystem','Label','Filesystem UUID','PARTUUID','Serial','Model','Mount','Editable?']);[w.writerow(self.usbtree.item(i)['values']) for i in self.usbtree.get_children()]
  self.status.set('Drive report exported')
 def history_tab(self):
  f=self.tab('History');self.tree=ttk.Treeview(f,columns=('time','action','uuid'),show='headings');self.tree.heading('time',text='Time');self.tree.heading('action',text='Action');self.tree.heading('uuid',text='UUID');self.tree.column('time',width=150);self.tree.column('action',width=120);self.tree.column('uuid',width=420);self.tree.grid(sticky='nsew');f.rowconfigure(0,weight=1);b=ttk.Frame(f);b.grid(row=1,column=0,sticky='w',pady=5);ttk.Button(b,text='Copy Selected',command=self.copyhist).pack(side='left');ttk.Button(b,text='Export CSV',command=self.exporthist).pack(side='left',padx=5);ttk.Button(b,text='Clear History',command=self.clearhist).pack(side='left')
 def copyhist(self):
  s=self.tree.selection()
  if s:self.cp(self.tree.item(s[0])['values'][2])
 def clearhist(self):self.hist.clear();self.tree.delete(*self.tree.get_children());self.status.set('History cleared')
 def exporthist(self):
  p=filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV','*.csv')])
  if p:
   with open(p,'w',newline='',encoding='utf-8') as q:csv.writer(q).writerows([('Time','Action','UUID'),*self.hist])
   self.status.set('History exported')
 def save_txt(self):
  p=filedialog.asksaveasfilename(defaultextension='.txt',filetypes=[('Text','*.txt')])
  if p:open(p,'w',encoding='utf-8').write(self.out.get('1.0','end-1c'));self.status.set('TXT saved')
 def save_csv(self):
  p=filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV','*.csv')])
  if p:
   with open(p,'w',newline='',encoding='utf-8') as q:
    w=csv.writer(q);w.writerow(['UUID']);w.writerows([[x] for x in self.out.get('1.0','end-1c').splitlines() if x.strip()])
   self.status.set('CSV saved')
 def help_tab(self):
  f=self.tab('Help / About');t=tk.Text(f,wrap='word');t.grid(sticky='nsew');f.rowconfigure(0,weight=1);t.insert('1.0','''UUID TOOLBOX\n\nGenerator\nCreates one or many UUIDs. v1 is time/node based; v3 uses MD5 plus a namespace/name; v4 is random; v5 uses SHA-1 plus a namespace/name; v6 is reordered time-based; v7 is Unix-time ordered plus random data; v8 is application-defined.\n\nValidate / Inspect\nChecks UUID syntax and displays canonical form, version, variant, hex, integer, bytes and fields.\n\nEditor\nLoads the five standard UUID groups. Changing any hexadecimal digit creates a different UUID. This tab intentionally calls the result a NEW UUID.\n\nConverter\nConverts UUID text, 32-digit hexadecimal UUIDs and decimal 128-bit integers into common representations.\n\nCompare\nCompares two UUIDs and reports differing hexadecimal positions.\n\nHistory\nRecords generated, validated, edited and converted UUIDs during the current program session and can export them to CSV.\n\nPortability\nThis application uses only the Python standard library (Tkinter, uuid, csv, secrets and datetime). v6/v7/v8 generation is implemented internally for compatibility with Python versions whose uuid module does not yet provide those helpers.\n\nSafety note\nUUIDs are identifiers, not passwords or encryption keys. Do not assume a UUID is secret merely because it is difficult to guess.\n''');t.config(state='disabled')

if __name__=='__main__':App().mainloop()
