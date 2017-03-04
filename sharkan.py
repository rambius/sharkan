#!/usr/bin/env python3.5

import argparse
import os.path
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
    self.makemenu()

    self.pw = PanedWindow(self, orient=VERTICAL)
    self.pw.pack(side=TOP, expand=YES)
    self.text = Text(self.pw)
    self.pw.add(self.text)
    self.output = Text(self.pw)
    self.pw.add(self.output)

    if file:
      if not os.path.exists(file):
        with open(file, 'w') as f:
          pass
      self.master.title(file)
      self.file = file
      self.settext()
    else:
      self.master.title("Untitled")
      self.file = None
    self.text.focus()

    self.makestatus()
    self.update_status_msg("Welcome")

    self.bind_all("<Control-s>", self.save)
    self.bind_all("<Control-q>", self.quit)
    self.bind_all("<F5>", self.run)

  def makemenu(self):
    menubar = Frame(self)
    menubar.pack(side=TOP)

    filebtn = Menubutton(menubar, text='File')
    filebtn.pack(side=LEFT)
    file = Menu(filebtn, tearoff=0)
    file.add_command(label='Save', command=self.save, accelerator="Ctrl+S")
    file.add_command(label='Quit', command=self.quit, accelerator="Ctrl+Q")
    filebtn.config(menu=file)

    editbtn = Menubutton(menubar, text='Edit')
    editbtn.pack(side=LEFT)
    edit = Menu(editbtn, tearoff=0)
    edit.add_command(label='Cut', command=self.cut)
    edit.add_command(label='Copy', command=self.copy)
    edit.add_command(label='Paste', command=self.paste)
    editbtn.config(menu=edit)

    runbtn = Menubutton(menubar, text='Run')
    runbtn.pack(side=LEFT)
    run = Menu(runbtn, tearoff=0)
    run.add_command(label='Run', command=self.run, accelerator="F5")
    runbtn.config(menu=run)

  def makestatus(self):
    statusbar = Frame(self, name="status")
    statusbar.pack(side=BOTTOM)
    msg = Label(statusbar, name="msg")
    msg.pack(side=LEFT)
    pos = Label(statusbar)
    pos.pack(side=RIGHT)

  def update_status_msg(self, message):
    l = self.nametowidget("status.msg")
    l.config(text=message)
    self.after(5000, self.clear_status_msg)

  def clear_status_msg(self):
    l = self.nametowidget("status.msg")
    l.config(text="")

  def settext(self):
    with open(self.file, 'r+') as f:
      txt = f.read()
      self.text.insert('1.0', txt)

  def quit(self, event=None):
    Frame.quit(self)

  def save(self, event=None):
    txt = self.text.get('1.0', END+'-1c')
    if self.file:
      with open(self.file, 'w') as f:
        f.write(txt)
    else:
      self.file = asksaveasfilename()
      with open(self.file, 'w') as f:
        f.write(txt)
      self.master.title(self.file)
    self.update_status_msg("Saved")

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

  def run(self, event=None):
    p = subprocess.run([sys.executable, self.file], 
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
  if args.file:
    pyed = PyEd(parent=root, file=args.file)
  else:
    pyed = PyEd(parent=root)
  pyed.pack()
  root.mainloop() 

if __name__ == '__main__':
  main()
