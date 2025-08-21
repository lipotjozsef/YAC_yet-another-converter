from sys import argv, platform
from subprocess import CREATE_NO_WINDOW, PIPE, Popen
from os import mkdir, startfile
from os.path import isdir, basename, abspath, join, exists
from datetime import datetime
from tkinter import Tk, Button, StringVar, OptionMenu, messagebox
from tkinter.ttk import Progressbar
import ffmpeg
from ffmpeg._run import output_operator
from formats import getFormats

myPath = abspath("converted/")
currentDate: str = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
outPath = join(myPath, currentDate)
logPath = abspath("lastlog.txt")

root: Tk = Tk()
fileBar: Progressbar = Progressbar(root, orient="horizontal", length=125)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.title("YAC - Yet Another Converter")
root.resizable(False, False)
root.geometry(f'200x200+{root.winfo_pointerx()}+{root.winfo_pointery()}')

rArgs: list= argv[1:]

barFillerValue : float = 100 / len(rArgs)

# monkey patch from user github - thank god
# https://github.com/kkroening/ffmpeg-python/issues/686#issuecomment-2664474089
@output_operator()
def patched_run_async(
    stream_spec,
    cmd='ffmpeg',
    pipe_stdin=False,
    pipe_stdout=False,
    pipe_stderr=False,
    quiet=False,
    overwrite_output=False,
):
    # hide windows console
    creationflags = 0
    if platform == "win32":
        creationflags = CREATE_NO_WINDOW

    args = ffmpeg._run.compile(stream_spec, cmd, overwrite_output=overwrite_output)
    stdin_stream = PIPE if pipe_stdin else None
    stdout_stream = PIPE if pipe_stdout or quiet else None
    stderr_stream = PIPE if pipe_stderr or quiet else None
    return Popen(
        args, stdin=stdin_stream, stdout=stdout_stream, stderr=stderr_stream, creationflags=creationflags
    )

ffmpeg._run.run_async = patched_run_async

if len(rArgs) == 0:
    messagebox.showerror("Hiba!", "Nem adott meg fáljt!\nKilépés.")
    exit(-1)

if isdir(rArgs[0]):
    messagebox.showerror("Hiba!", "Mappákat nem lehet átalakítani!")
    exit(-1)

def main():

    myFormats: str = getFormats(basename(rArgs[0]))
    
    selectedExt: StringVar = StringVar(value=myFormats[0])
    OptionMenu(root, selectedExt, *myFormats).grid(row = 0, column = 0, sticky='sew', padx = 50)
    Button(root, text="Kezdés", command=lambda: startProcess(myFormats, selectedExt.get())).grid(row = 1, column = 0, sticky='new', padx = 50, pady=10)
    fileBar.grid(row = 2, column = 0, sticky='n')
    if not exists(logPath):
        mkdir(logPath)

    if not exists(myPath):
        mkdir(myPath)


    root.mainloop()

def startProcess(myFormats: list[str], selectedExt: str):
    if not exists(outPath):
        mkdir(outPath)
    allsum = 0
    for filePath in rArgs:
        if processFile(abspath(filePath), myFormats, '.'+selectedExt):
            allsum += 1
            fileBar["value"] += barFillerValue
    messagebox.showinfo("Információ", f"Kész az átalakítás!\n{allsum}/{len(rArgs)} fálj átalakítva")
    startfile(outPath)
    root.destroy()

def processFile(filePath: str, formats: list[str], myExt: str):
    fileName = basename(filePath)
    fileBasename, fileExt = fileName.split('.')
    myOutput =join(outPath, fileBasename+myExt)
    if fileExt in formats:
        ffmpeg.input(filePath).output(myOutput, loglevel="quiet").run()
        return True
    return False
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open(logPath, "w") as f:
            f.write(f"{str(e)}\nLogged at {currentDate}")
