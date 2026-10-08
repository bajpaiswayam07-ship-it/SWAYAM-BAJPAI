@echo off
setlocal
echo ========================================================
echo   Starting SoundWave Music Playlist Management System
echo ========================================================

REM Check if Python is available in PATH
set "PYCMD=python"
%PYCMD% --version >nul 2>nul
if %errorlevel% neq 0 (
    set "PYCMD=py"
    %PYCMD% --version >nul 2>nul
    if %errorlevel% neq 0 (
        if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
            set "PYCMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        ) else (
            echo [ERROR] Python not found! Please make sure Python 3 is installed.
            pause
            exit /b 1
        )
    )
)

REM Check if C++ DLL is compiled, compile if missing
if not exist "cpp_core\playlist_core.dll" (
    echo [INFO] Compiling C++ core engine DLL...
    g++ -std=c++17 -O2 -shared -static-libgcc -static-libstdc++ -DBUILDING_CORE_DLL -I cpp_core\include cpp_core\src\DoublyLinkedList.cpp cpp_core\src\TrieSearch.cpp cpp_core\src\RecommendationEngine.cpp cpp_core\src\Sorter.cpp cpp_core\src\PlaylistManager.cpp cpp_core\src\api_exports.cpp -o cpp_core\playlist_core.dll
)

echo [INFO] Launching SoundWave GUI...
"%PYCMD%" python_ui\gui.py
endlocal
