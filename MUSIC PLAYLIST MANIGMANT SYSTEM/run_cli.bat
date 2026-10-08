@echo off
echo ========================================================
echo   Launching SoundWave C++ Terminal CLI Core Engine
echo ========================================================

if not exist "music_core_cli.exe" (
    echo [INFO] Compiling music_core_cli.exe...
    g++ -std=c++17 -O2 -static-libgcc -static-libstdc++ -I cpp_core\include cpp_core\src\DoublyLinkedList.cpp cpp_core\src\TrieSearch.cpp cpp_core\src\RecommendationEngine.cpp cpp_core\src\Sorter.cpp cpp_core\src\PlaylistManager.cpp cpp_core\src\main_cli.cpp -o music_core_cli.exe
)

music_core_cli.exe
