@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ── 專案根目錄與輸出 ──────────────────────────────────────────────
set "ROOT=D:\SWProject\test\880100009\defrostTest2024\8801000009"
set "OUTXML=%ROOT%\cppcheck8801000009.xml"

REM ── 組出 -I "子路徑A" -I "子路徑B" ...（僅加入有 .h/.hpp 的資料夾） ──
set "INC="
for /F "delims=" %%D in ('dir /B /AD /S "%ROOT%"') do (
  if exist "%%D\*.h" (
    set INC=!INC! -I "%%D"
  ) else if exist "%%D\*.hpp" (
    set INC=!INC! -I "%%D"
  )
)

echo Using root path: "%ROOT%"
echo Include args: %INC%
echo.

REM 目標資料夾必須存在
if not exist "%ROOT%" (
  echo ERROR: ROOT not found: "%ROOT%"
  exit /b 1
)

REM ── 執行 Cppcheck──────────────────────────────────
"C:\Program Files\Cppcheck Premium\cppcheck.exe" ^
  %INC% ^
  --performance-valueflow-max-if-count=10 ^
  --premium=misra-c-2025 ^
  --enable=all ^
  --inconclusive ^
  --std=c11 ^
  --platform=win64 ^
  --xml ^
  "%ROOT%" ^
  2>"%OUTXML%"

Endlocal
