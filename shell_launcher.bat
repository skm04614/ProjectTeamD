@echo off
setlocal

if "%~1"=="" (
    python -m custom_shell.cshell
) else (
    python -m custom_shell.cshell %1
)

endlocal