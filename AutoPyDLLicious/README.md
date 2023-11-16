# AutoPyDLLicious

AutoPyDLLicious is a Windows tool for automating the process of discovering and exploiting DLL Hijacks. It is a wrapper over ProcMon which does the following:
1. Starts ProcMon and logs the data in log.pml
2. Once ProcMon is manually stopped it opens log.pml and changes it to log.csv
3. It parses the logs and sets the appropriate filters for discovering DLL hijacks
4. It prompts the user to select the application to test for DLL hijacks
5. It attempts to write poc.dll in the location of each hijackable path (one by one)
6. It runs the application and checks whether a messagebox was produced. If so, it saves the path to hijacked.txt


## Usage
1. Run AutoPyDLLicious
2. Start various applications
3. Close ProcMon
4. Select the application to test for DLL hijacking
5. Wait while AutoPyDLLicious does the rest
6. Check hijacked.txt

   

https://github.com/MatJosephs/DLL-Hijacking/assets/73303726/8cda9377-f7e2-4964-8892-01bbb373b25b


