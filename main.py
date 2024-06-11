import os
import webbrowser

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
      parse(filename, entryNumberVar.get(), timeStampVar.get(), textVar.get())
      listOutputs.insert(srtFileNames.index(filename), filename + " ==> " + filename + ".txt")
    
def githubClick(event):
  webbrowser.open(githubURL, new=0, autoraise=True)

def parse(srtFileName, keepEntryNumber, keepTimeStamp, keepText):
  try:
    srtFile = open(srtFileName, "r")
  except FileNotFoundError:
    exit("[" + srtFile + "] : file not found")
  outputFile = open(srtFileName + ".txt", "w")

  currentEntry = 0
  for line in srtFile:
    currentEntry += 1
    arrowIndex = line.find("-->")
    endTimeStampIndex = arrowIndex + 16
    if arrowIndex > 0:
      entryNumber = line[:line.find(" ")]
      if not keepTimeStamp:
        line = entryNumber + "\n" + line[endTimeStampIndex:]
      else :
        line = line[:endTimeStampIndex] + "\n" + line[endTimeStampIndex:].strip()
      if not keepText:
        line = line[:endTimeStampIndex]
      if not keepEntryNumber:
        line = line[line.find(" "):]
    line = line.strip()
    if line and not (arrowIndex == -1 and not keepText):
      outputFile.write(line + "\n")


window = tk.Tk()
window.title("SRToTXT 1.0 - Nicolas Picavet")
window.resizable(0,0)


firstRowFrame = tk.Frame(window)
firstRowFrame.grid(column=0, row=0, sticky=tk.W)

oneLabel = tk.Label(firstRowFrame, text="1", font=(None, 28))
oneLabel.grid(column=0, row=0, padx=5, pady=2, rowspan=3)

entryNumberVar = tk.BooleanVar(value=False)
entryNumberCheckButton = tk.Checkbutton(firstRowFrame, text='Keep entry number',variable=entryNumberVar, onvalue=True, offvalue=False)
entryNumberCheckButton.grid(column=1, row=0, sticky=tk.W, padx=5, pady=2)
timeStampVar = tk.BooleanVar(value=False)
timeStampCheckButton = tk.Checkbutton(firstRowFrame, text='Keep timestamp',variable=timeStampVar, onvalue=True, offvalue=False)
timeStampCheckButton.grid(column=1, row=1, sticky=tk.W, padx=5, pady=2)
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

