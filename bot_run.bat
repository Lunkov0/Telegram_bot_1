@echo off

call %~dp0venv\scripts\activate

cd %~dp0

set TOKEN=6679199342:AAH2CHgDn0mpdhXLs34SwIhJRopWgOybvXI

python bot.py

pause