#include <windows.h>
#include <stdio.h>
#include <sddl.h>

#pragma comment (lib, "user32.lib")

BOOL APIENTRY DllMain(HMODULE hModule,  DWORD  ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call)  {
    case DLL_PROCESS_ATTACH:
            HANDLE hToken;
            DWORD dwLengthNeeded;
            DWORD dwError;
            PTOKEN_MANDATORY_LABEL pTIL;

            // Open the primary access token of the current process
            if (!OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY, &hToken)) {
                dwError = GetLastError();
                printf("OpenProcessToken failed with error %d\n", dwError);
                return 1;
            }

            // Call GetTokenInformation to get the Token Mandatory Label
            if (!GetTokenInformation(hToken, TokenIntegrityLevel, NULL, 0, &dwLengthNeeded)) {
                dwError = GetLastError();
                if (dwError != ERROR_INSUFFICIENT_BUFFER) {
                    printf("GetTokenInformation (1st call) failed with error %d\n", dwError);
                    CloseHandle(hToken);
                    return 1;
                }
            }

            pTIL = (PTOKEN_MANDATORY_LABEL)malloc(dwLengthNeeded);
            if (pTIL == NULL) {
                printf("Memory allocation failed\n");
                CloseHandle(hToken);
                return 1;
            }

            if (!GetTokenInformation(hToken, TokenIntegrityLevel, pTIL, dwLengthNeeded, &dwLengthNeeded)) {
                dwError = GetLastError();
                printf("GetTokenInformation (2nd call) failed with error %d\n", dwError);
                free(pTIL);
                CloseHandle(hToken);
                return 1;
            }

            // Convert the integrity level to a string
            LPWSTR pSidString;
            ConvertSidToStringSidW(pTIL->Label.Sid, &pSidString);
            // Check for High integrity level, but could check for System, Domain Admin, or any other 
            if (lstrcmpW(pSidString, L"S-1-16-12288") == 0)
            {
                MessageBoxW(NULL, L"Imagine this is a reverse shell...", L"You are Admin", MB_ICONINFORMATION);
            }

            else
            {
                MessageBoxW(NULL, L"Please run the application as Administrator", L"Administrator Privileges Required", MB_ICONINFORMATION);
                while (1); // Infinite loop - does not allow the Application to run
            }

            free(pTIL);
            CloseHandle(hToken);

              break;
    case DLL_PROCESS_DETACH:
      break;
    case DLL_THREAD_ATTACH:
      break;
    case DLL_THREAD_DETACH:
      break;
    }
    return TRUE;
}

