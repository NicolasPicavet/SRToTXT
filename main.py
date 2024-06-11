import os
import webbrowser
import re
import codecs

import tkinter as tk
from tkinter import filedialog


githubURL = "https://github.com/NicolasPicavet/SRToTXT"


def browseFilesClick(event):
  srtFileNames = filedialog.askopenfilenames(
    initialdir = os.getcwd(),
    title = "Select one or multiple file",
    filetypes = (
                  ("SRT files", "*.srt*"),
                  ("all files", "*.*")
                ))
  event.widget.after(0, lambda: event.widget.config(relief=tk.RAISED))
  for filename in srtFileNames:
    if filename != "":
      parse(filename, entryNumberVar.get(), timestampVar.get(), textVar.get())
      listOutputs.insert(srtFileNames.index(filename), filename + " ==> " + filename + ".txt")
    
def githubClick(event):
  webbrowser.open(githubURL, new=0, autoraise=True)

def parse(srtFileName, keepEntryNumber, keepTimestamp, keepText):
  try:
    srtFile = codecs.open(srtFileName, "r", "utf-8-sig")
  except FileNotFoundError:
    exit("[" + srtFile + "] : file not found")
  outputFile = codecs.open(srtFileName + ".txt", "w", "utf-8-sig")

  for line in srtFile:
    line = line.strip()
    if re.search("^[0-9]", line):
      if line.find(":") == -1:
        if not keepEntryNumber:
          continue
      else:
        if not keepTimestamp:
          continue
    elif not line:
      continue
    if not keepText:
      continue
    outputFile.write(line + "\n")

  srtFile.close()
  outputFile.close()


window = tk.Tk()
window.title("SRToTXT 1.1 - Nicolas Picavet")
window.resizable(0,0)


firstRowFrame = tk.Frame(window)
firstRowFrame.grid(column=0, row=0, sticky=tk.W)

oneLabel = tk.Label(firstRowFrame, text="1", font=(None, 28))
oneLabel.grid(column=0, row=0, padx=5, pady=2, rowspan=3)

entryNumberVar = tk.BooleanVar(value=False)
entryNumberCheckButton = tk.Checkbutton(firstRowFrame, text='Keep entry number',variable=entryNumberVar, onvalue=True, offvalue=False)
entryNumberCheckButton.grid(column=1, row=0, sticky=tk.W, padx=5, pady=2)
timestampVar = tk.BooleanVar(value=False)
timestampCheckButton = tk.Checkbutton(firstRowFrame, text='Keep timestamp',variable=timestampVar, onvalue=True, offvalue=False)
timestampCheckButton.grid(column=1, row=1, sticky=tk.W, padx=5, pady=2)
textVar = tk.BooleanVar(value=True)
textCheckButton = tk.Checkbutton(firstRowFrame, text='Keep text',variable=textVar, onvalue=True, offvalue=False)
textCheckButton.grid(column=1, row=2, sticky=tk.W, padx=5, pady=2)

twoLabel = tk.Label(firstRowFrame, text="2", font=(None, 28))
twoLabel.grid(column=2, row=0, padx=(25, 5), pady=2, rowspan=3)

browseButton = tk.Button(firstRowFrame, text="Browse SRT files")
browseButton.bind("<Button-1>", browseFilesClick)
browseButton.grid(column=3, row=0, padx=5, pady=5, rowspan=3)


secondRowFrame = tk.Frame(window)
secondRowFrame.grid(column=0, row=1, sticky=tk.W, padx=(0, 5), pady=(15, 0))

threeLabel = tk.Label(secondRowFrame, text="3", font=(None, 28))
threeLabel.grid(column=0, row=0, padx=5, pady=2)

listOutputsXScrollbar = tk.Scrollbar(secondRowFrame, orient=tk.HORIZONTAL)
listOutputsXScrollbar.grid(column=1, row=1, sticky=tk.W+tk.E)
listOutputsYScrollbar = tk.Scrollbar(secondRowFrame)
listOutputsYScrollbar.grid(column=2, row=0, sticky=tk.N+tk.S)
listOutputs = tk.Listbox(secondRowFrame, font=(None, 8), height=8, width=80, xscrollcommand = listOutputsXScrollbar.set, yscrollcommand = listOutputsYScrollbar.set)
listOutputs.grid(column=1, row=0, padx=0, pady=0)
listOutputsXScrollbar.config(command = listOutputs.xview)
listOutputsYScrollbar.config(command = listOutputs.yview)

githubButton = tk.Button(secondRowFrame, text=githubURL)
githubButton.bind("<Button-1>", githubClick)
githubButton.grid(column=0, row=2, pady=(10, 0), sticky=tk.E, columnspan=3)


window.mainloop()

