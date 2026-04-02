@echo off
REM COPIA_TXT.BAT SCRIP
setlocal

set "origem=D:\Work\ProjetosDev\task-manager"
set "destino=D:\Work\ProjetosDev\__copiaemtxt__"

echo Iniciando copia dos arquivos na %origem% para o %destino%
if not exist "%destino%" mkdir "%destino%"

echo Copiando arquivos .py...
for %%f in ("%origem%\*.py") do (
    echo Copiando: %%f -> "%destino%\%%~nf.txt"
    copy "%%f" "%destino%\%%~nf.txt" /Y
)

echo Copiando arquivos .md...
for %%f in ("%origem%\*.md") do (
    echo Copiando: %%f -> "%destino%\%%~nf.txt"
    copy "%%f" "%destino%\%%~nf.txt" /Y
)

echo Gerando arquivo consolidado...
type "%origem%\*.py" "%origem%\*.md" > "%destino%\_taskmanager.txt"

echo Concluido!
pause

REM END OF COPIA_TXT.BAT SCRIPT