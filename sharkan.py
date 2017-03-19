#!/usr/bin/env python3.5

import argparse
import os.path
import py_compile
import re
import subprocess
import sys
from tkinter import BOTH
from tkinter import BOTTOM
from tkinter import END
from tkinter import Frame
from tkinter import INSERT
from tkinter import Label
from tkinter import LEFT
from tkinter import Menu
from tkinter import Menubutton
from tkinter import NONE
from tkinter import PanedWindow
from tkinter import SEL_FIRST
from tkinter import SEL_LAST
from tkinter import RIGHT
from tkinter import Text
from tkinter import Tk
from tkinter import TOP
from tkinter import VERTICAL
from tkinter import X
from tkinter import YES
from tkinter.filedialog import asksaveasfilename
	
class PyEd(Frame):

  def __init__(self, file=None, parent=None):
    Frame.__init__(self, parent, name="base")
    self.file = file
    self.make_menu()

    self.pw = PanedWindow(self, orient=VERTICAL)
    self.pw.pack(side=TOP, expand=YES)
    self.text = Text(self.pw)
    self.pw.add(self.text)
    self.output = Text(self.pw)
    self.pw.add(self.output)

    if self.file:
      self.master.title(self.file)
      self.settext()
    else:
      self.master.title("Untitled")
    self.text.focus()

    self.makestatus()
    self.update_status_msg("Welcome")

    self.bind_all("<Control-n>", self.new)
    self.bind_all("<Control-s>", self.save)
    self.bind_all("<Control-q>", self.quit)
    self.text.bind("<KeyPress>", self.update_pos)

  def make_menu(self):
    self.menubar = Frame(self)
    self.menubar.pack(side=TOP)

    filebtn = Menubutton(self.menubar, text='File')
    filebtn.pack(side=LEFT)
    file = Menu(filebtn, tearoff=0)
    file.add_command(label='New', command=self.new, accelerator="Ctrl+N")
    file.add_command(label='Save', command=self.save, accelerator="Ctrl+S")
    file.add_command(label='Quit', command=self.quit, accelerator="Ctrl+Q")
    filebtn.config(menu=file)

    editbtn = Menubutton(self.menubar, text='Edit')
    editbtn.pack(side=LEFT)
    edit = Menu(editbtn, tearoff=0)
    edit.add_command(label='Cut', command=self.cut)
    edit.add_command(label='Copy', command=self.copy)
    edit.add_command(label='Paste', command=self.paste)
    editbtn.config(menu=edit)

    if self.file:
      self.make_file_type_menu(self.menubar)

  def make_file_type_menu(self, menubar):
    _, e = os.path.splitext(self.file)
    ext = e[1:]
    if ext == "py":
      pybtn = Menubutton(menubar, text='Python', name=ext)
      pybtn.pack(side=LEFT)
      py = Menu(pybtn, tearoff=0)
      py.add_command(label='Compile', command=self.compile_python, accelerator="Ctrl+F5")
      py.add_command(label='Run', command=self.run_python, accelerator="F5")
      pybtn.config(menu=py)
      self.bind_all("<Control-F5>", self.compile_python)
      self.bind_all("<F5>", self.run_python)
    elif ext == "tcl":
      tclbtn = Menubutton(menubar, text='TCL', name=ext)
      tclbtn.pack(side=LEFT)
      tcl = Menu(tclbtn, tearoff=0)
      tcl.add_command(label='Run', command=self.run_tcl, accelerator="F5")
      tclbtn.config(menu=tcl)
      self.bind_all("<F5>", self.run_tcl)

  def makestatus(self):
    statusbar = Frame(self, name="status")
    statusbar.pack(side=BOTTOM)
    msg = Label(statusbar, name="msg")
    msg.pack(side=LEFT)
    pos = Label(statusbar, name="pos")
    pos.pack(side=RIGHT)

  def update_pos(self, event):
    index = self.text.index(INSERT)
    l = self.nametowidget("status.pos")
    l.config(text=index)

  def update_status_msg(self, message):
    l = self.nametowidget("status.msg")
    l.config(text=message)
    self.after(5000, self.clear_status_msg)

  def clear_status_msg(self):
    l = self.nametowidget("status.msg")
    l.config(text="")

  def settext(self):
    if os.path.exists(self.file):
      txt = self.read_file(self.file)
      self.text.insert('1.0', txt)

  def quit(self, event=None):
    Frame.quit(self)

  def save(self, event=None):
    txt = self.text.get('1.0', END+'-1c')
    if not self.file:
      self.file = asksaveasfilename()
      self.master.title(self.file)
      self.make_file_type_menu(self.menubar)
    self.write_to_file(self.file, txt)
    self.update_status_msg("Saved")

  def new(self, event=None):
    _, e = os.path.splitext(self.file)
    ext = e[1:]
    b = self.menubar.children.get(ext)
    if b:
      b.destroy()
    self.file = None
    self.master.title("Untitled")
    self.text.delete('1.0', END)

  def write_to_file(self, file, txt):
    with open(file, 'w') as f:
      f.write(txt)

  def read_file(self, file):
    with open(file, 'r+') as f:
      txt = f.read()
      return txt

  def cut(self):
    txt = self.text.get(SEL_FIRST, SEL_LAST)
    self.text.delete(SEL_FIRST, SEL_LAST)
    self.clipboard_clear()
    self.clipboard_append(txt)

  def copy(self):
    txt = self.text.get(SEL_FIRST, SEL_LAST)
    self.clipboard_clear()
    self.clipboard_append(txt)

  def paste(self):
    txt = self.selection_get(selection='CLIPBOARD')
    self.text.insert(INSERT, txt)

  def run_python(self, event=None):
    p = subprocess.run([sys.executable, self.file], 
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE) 
    self.output.insert('end', p.stdout)
    self.output.insert('end', p.stderr)
    self.output.see(END)

  def compile_python(self, event=None):
    try:
      py_compile.compile(self.file, doraise=True)
      self.output.insert('end', "%s compiled successfully\n" % self.file)
    except py_compile.PyCompileError as pyce:
      lere = re.compile('\s*File \".*\", line(\d*)')
      r = lere.match(pyce.msg)
      lineno = r.group(1)
      print(lineno)

  def run_tcl(self, event=None):
    p = subprocess.run(["tclsh8.7", self.file],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    self.output.insert('end', p.stdout)
    self.output.insert('end', p.stderr)
    self.output.see(END)

def main():
  parser = argparse.ArgumentParser(description="Text Editor")
  parser.add_argument("file",
                      help="File to open",
                      nargs="?",
                      default=None)
  args = parser.parse_args()
  root = Tk()
  pyed = PyEd(parent=root, file=args.file)
  pyed.pack()
  root.mainloop() 

if __name__ == '__main__':
  main()
