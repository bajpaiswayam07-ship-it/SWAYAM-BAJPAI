@echo off
echo ========================================================
echo   SoundWave - Compiling C++ Core Engine and Testing
echo ========================================================

where g++ >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] g++ compiler not found in PATH!
    pause
    exit /b 1
)

echo [1/4] Compiling Native C++ Shared Library (playlist_core.dll)...
g++ -std=c++17 -O2 -shared -static-libgcc -static-libstdc++ -DBUILDING_CORE_DLL -I cpp_core\include cpp_core\src\DoublyLinkedList.cpp cpp_core\src\TrieSearch.cpp cpp_core\src\RecommendationEngine.cpp cpp_core\src\Sorter.cpp cpp_core\src\PlaylistManager.cpp cpp_core\src\api_exports.cpp -o cpp_core\playlist_core.dll

if %errorlevel% neq 0 (
    echo [ERROR] Failed to compile playlist_core.dll!
    pause
    exit /b 1
)
echo [SUCCESS] playlist_core.dll built successfully.

echo [2/4] Compiling Standalone C++ Terminal Application (music_core_cli.exe)...
g++ -std=c++17 -O2 -static-libgcc -static-libstdc++ -I cpp_core\include cpp_core\src\DoublyLinkedList.cpp cpp_core\src\TrieSearch.cpp cpp_core\src\RecommendationEngine.cpp cpp_core\src\Sorter.cpp cpp_core\src\PlaylistManager.cpp cpp_core\src\main_cli.cpp -o music_core_cli.exe

if %errorlevel% neq 0 (
    echo [ERROR] Failed to compile music_core_cli.exe!
    pause
    exit /b 1
)
echo [SUCCESS] music_core_cli.exe built successfully.

echo [3/4] Compiling and Running C++ DSA Unit Tests...
g++ -std=c++17 -O2 -I cpp_core\include cpp_core\src\DoublyLinkedList.cpp cpp_core\src\TrieSearch.cpp cpp_core\src\RecommendationEngine.cpp cpp_core\src\Sorter.cpp tests\test_cpp.cpp -o tests\test_cpp.exe
tests\test_cpp.exe

if %errorlevel% neq 0 (
    echo [ERROR] C++ Unit Tests Failed!
    pause
    exit /b 1
)

echo [4/4] Running Python-C++ Bridge Integration Test...
REM Run python test
set "PYCMD=python"
%PYCMD% --version >nul 2>nul
if %errorlevel% neq 0 (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PYCMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    )
)
"%PYCMD%" tests\test_bridge.py
"%PYCMD%" tests\test_auth.py

echo.
echo ========================================================
echo   ALL BUILDS AND TESTS COMPLETED WITH 100%% SUCCESS!
echo ========================================================
if "%1"=="" pause
