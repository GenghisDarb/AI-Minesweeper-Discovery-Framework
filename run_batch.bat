@echo off
where wolfram >nul 2>nul
if %errorlevel%==0 (
    echo Wolfram Engine detected. Running batch scripts...
    wolfram -script wolfram\run_all.wls
) else (
    echo Wolfram Engine not found. Using pre-generated files.
)
