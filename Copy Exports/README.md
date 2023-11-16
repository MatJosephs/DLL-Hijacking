# Copy Exports

Sometimes, DLL Hijacks fail because the application is expecting specific exports from the DLL. This has been explained in the following [SecurityCafe Article](https://securitycafe.ro/2023/06/19/dll-hijacking-finding-vulnerabilities-in-pestudio-9-52/).
In this case, we can find the original/expected DLL, extract the exports using **extract_def.py** and cross-compile the new DLL using the definition file.

## Example
dll_hijack.c -  **DLL Hijacking PoC**

SensApi.dll - **Target DLL**

```bash
python3 extract_def.py SensApi.dll
86_64-w64-mingw32-gcc -shared -o dll_hijack.dll dll_hijack.c SensApi.def -S
```
