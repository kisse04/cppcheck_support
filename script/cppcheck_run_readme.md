# cppcheck_run 腳本說明

本資料夾提供兩個執行 Cppcheck 的腳本：`cppcheck_run.bat` 與 `cppcheck_run.py`。兩者都會自動收集包含 `*.h/*.hpp` 的資料夾並加入 `-I`，並使用 Cppcheck Premium 以 MISRA C 2025 規則執行檢查，輸出 XML 報告。

## 需求
- Windows
- Cppcheck Premium 已安裝（預設路徑：`C:\Program Files\Cppcheck Premium\cppcheck.exe`）
- Python 3.7+（僅 `cppcheck_run.py` 需要）

## cppcheck_run.bat

### 功能摘要
- 設定專案根目錄 `ROOT` 與輸出檔 `OUTXML`
- 遞迴搜尋 `ROOT` 下含 `*.h` 或 `*.hpp` 的資料夾並加入 `-I`
- 以固定參數執行 Cppcheck，將 XML 輸出寫入 `OUTXML`（Cppcheck 的 XML 會從 stderr 輸出）

### 主要參數（在 .bat 內設定）
- `ROOT`：專案根目錄
- `OUTXML`：輸出 XML 檔案路徑

### 執行方式
直接執行 `cppcheck_run.bat`。請先在檔案內修改 `ROOT` 與 `OUTXML`。

### 使用的 Cppcheck 參數
- `--performance-valueflow-max-if-count=10`
- `--premium=misra-c-2025`
- `--enable=all`
- `--inconclusive`
- `--std=c11`
- `--platform=win64`
- `--xml`

## cppcheck_run.py

### 功能摘要
- 自動收集 include 目錄（排除常見輸出/暫存資料夾）
- 若命令列長度過長，嘗試建立 junction 聚合資料夾 `_cppcheck_includes` 以縮短 `-I` 列表
- 產生 `include_paths.txt`（記錄實際使用的 include 路徑）
- 執行 Cppcheck 產生 XML（stderr），可選擇產生 HTML 報告

### 參數說明
- `--root`：專案根目錄（必填）
- `--cppcheck`：`cppcheck.exe` 路徑（預設：`C:\Program Files\Cppcheck Premium\cppcheck.exe`）
- `--outxml`：輸出 XML 檔案（預設：`<root>\cppcheck.xml`）
- `--exclude`：要排除的資料夾名稱（預設包含 `.git`, `build`, `out`, `bin`, `obj`, `Debug`, `Release`, `x64`, `x86` 等）
- `--html`：輸出 HTML 報告
- `--htmlreport`：`cppcheck-htmlreport.py` 路徑（預設：`C:\Program Files\Cppcheck Premium\cppcheck-htmlreport.py`）
- `--report-dir`：HTML 報告輸出資料夾（預設：`<root>\html`）
- `--title`：HTML 報告標題（預設：`Cppcheck Report - <root 目錄名>`）
- `--py`：執行 Python 的指令（預設：`py`）

### 範例
只輸出 XML：
```
py cppcheck_run.py --root "D:\SWProject\test\880100009\defrostTest2024\8801000009"
```

輸出 XML + HTML：
```
py cppcheck_run.py --root "D:\SWProject\test\880100009\defrostTest2024\8801000009" --html --title "Cppcheck Report 8801000009"
```

### 使用的 Cppcheck 參數
- `--relative-paths=<root>`
- `--performance-valueflow-max-if-count=10`
- `--premium=misra-c-2025`
- `--enable=all`
- `--inconclusive`
- `--std=c11`
- `--platform=win64`
- `--xml --xml-version=2`

### 輸出
- XML：`--outxml` 指定的路徑（預設 `<root>\cppcheck.xml`）
- HTML（可選）：`--report-dir` 指定的資料夾（預設 `<root>\html`）
- include 記錄：`<root>\include_paths.txt`

## 注意事項
- 若 `cppcheck_run.py` 嘗試建立 junction 失敗，會回退為大量 `-I` 參數，可能導致 Windows 命令列長度限制錯誤。
- 若需要 HTML 報告，請確認 `cppcheck-htmlreport.py` 路徑正確且可由指定 Python 執行。
