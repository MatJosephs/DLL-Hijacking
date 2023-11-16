# Proof of Concept DLLs
## Compiling and Executing

Cross-compile using  ```86_64-w64-mingw32-gcc -shared -o poc.dll simple_poc.c```, respectively ```86_64-w64-mingw32-gcc -shared -o poc.dll privesc_poc.c```

Execute using ```rundll32 poc.dll,a```.

## Description

### simple_poc.c

A simple Proof of Concept displaying a messagebox upon execution.

### privesc_poc.c

A Proof of Concept which check for Admin privileges. If admin privileges are granted, it displays a messagebox saying "Imagine this is a reverse shell...". Otherwise, it displays a message box saying "Please run as Administrator" and enters an infinite loop.
