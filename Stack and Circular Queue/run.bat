@echo off
chcp 65001 >nul
title StructLab - Stack and Circular Queue CLI
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0main.ps1"
pause
