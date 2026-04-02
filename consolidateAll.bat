@echo off
REM consolidateAll.BAT SCRIP
REM This script generates a single consolidated .txt file containing 
REM the combined content of all project files (such as .py and .md ). 
REM Its purpose is purely documentation: to provide an easy-to-read 
REM snapshot of the entire project in one place. Each time the script is executed, 
REM the consolidated file is regenerated, 
REM ensuring it always reflects the most up-to-date state of the project.

setlocal

echo Gerando arquivo consolidado do projeto...
type ".\*.py" ".\*.md" > ".\__taskmanager.txt"

echo Concluido!
pause

REM END OF consolidateAll.BAT SCRIPT