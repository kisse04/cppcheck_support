# **Cppcheck**

|release-windows|OSS-Fuzz|Coverity Scan Build Status|include-what-you-use|License|
|:--:|:--:|:--:|:--:|:--:|
|[![release-windows](https://github.com/danmar/cppcheck/actions/workflows/release-windows.yml/badge.svg?branch=main)](https://github.com/danmar/cppcheck/actions/workflows/release-windows.yml)|[![OSS-Fuzz](https://oss-fuzz-build-logs.storage.googleapis.com/badges/cppcheck.svg)](https://bugs.chromium.org/p/oss-fuzz/issues/list?sort=-opened&can=1&q=proj:cppcheck)|[![Coverity Scan Build Status](https://img.shields.io/coverity/scan/512.svg)](https://scan.coverity.com/projects/512)|[![include-what-you-use](https://github.com/danmar/cppcheck/actions/workflows/iwyu.yml/badge.svg?branch=main)](https://github.com/danmar/cppcheck/actions/workflows/iwyu.yml)|[![License](https://img.shields.io/badge/license-GPL3.0-blue.svg)](https://opensource.org/licenses/GPL-3.0)


## 關於名稱

這個程式最初的名稱是「C++check」，後來改為「Cppcheck」。

儘管名稱如此，Cppcheck 同時為 C 與 C++ 設計。

## 使用手冊

可在線上閱讀手冊：[manual](https://cppcheck.sourceforge.io/manual.pdf)。

## 捐贈 CPU

Cppcheck 是資源有限的興趣專案。你可以捐贈 CPU（預設 1 核，或依需求更多；使用 `-j` 旗標可增加核心數）來協助我們。步驟如下：

 1. 下載並解壓 Cppcheck 原始碼。
 2. 執行（Linux/MacOS 範例）：
    ```
    cd cppcheck/
    python3 -m venv .venv
    source .venv/bin/activate

    pip install -r tools/donate-cpu-requirements.txt
    ./tools/donate-cpu.py
    ```

此腳本會分析 Debian 原始碼並將結果上傳至 cppcheck 伺服器。我們需要這些結果來改進 Cppcheck 並偵測回歸問題。

你可隨時用 Ctrl C 停止此腳本。

## 編譯

Cppcheck 需要支援（部分）C++11 的 C++ 編譯器。最低版本需求為 GCC 5.1 / Clang 3.5 / Visual Studio 2015。

若要建置 GUI 應用程式，你需要使用 CMake 建置系統。

建置命令列工具時，[PCRE](http://www.pcre.org/) 為選用。若啟用規則（rules）建置則會使用它。

有多種編譯方式：
* CMake - 跨平台建置工具
* （Windows）Visual Studio
* （Windows）Qt Creator + MinGW
* GNU 編譯器 - 透過 make 或直接編譯

最低需求的 Python 版本為 3.7。

### CMake

最低需求版本為 CMake 3.13。

範例：使用 cmake 編譯 Cppcheck：

```shell
cmake -S . -B build
cmake --build build
```

如果要編譯 GUI，可使用旗標。
-DBUILD_GUI=ON

若要支援規則（需要 pcre），使用旗標。
-DHAVE_RULES=ON

若為發行版建置，建議使用：
-DUSE_MATCHCOMPILER=ON

若要建置測試，使用旗標。
-DBUILD_TESTS=ON

使用 cmake 可產生 Visual Studio、XCode 等的專案檔案。

#### 建置特定組態

對於單組態產生器（如「Unix Makefiles」），可用以下方式產生並建置特定組態（例如「RelWithDebInfo」）：

```shell
cmake -S . -B build_RelWithDebInfo -DCMAKE_BUILD_TYPE=RelWithDebInfo ..
cmake --build build_RelWithDebInfo --config RelWithDebInfo
```

對於多組態產生器（如「Visual Studio 17 2022」），可使用：

```shell
cmake -S . -B build
cmake --build build --config RelWithDebInfo
```

### Visual Studio

使用 `cppcheck.sln` 檔案。該檔案為 Visual Studio 2019 設定，但平台工具集可輕鬆改為較舊或較新版本。解決方案包含 x86 與 x64 目標平台。

若要編譯規則（rules），請選擇「Release-PCRE」或「Debug-PCRE」組態。`pcre.lib`（x64 為 `pcre64.lib`）與 `pcre.h` 預期位於 `/externals`。可透過 [vcpkg](https://github.com/microsoft/vcpkg) 取得適用於 Visual Studio 的最新 PCRE 版本。

### Visual Studio（命令列）

若不想使用 Visual Studio IDE，可用命令列編譯 cppcheck： 

```shell
msbuild cppcheck.sln
```

### VS Code（Windows）

安裝 MSYS2 以取得 GNU toolchain（g++ 與 gdb）：https://www.msys2.org/。
在 `.vscode` 資料夾建立 `settings.json`，內容如下（依需求調整路徑）：

```
{
    "terminal.integrated.shell.windows": "C:\\msys64\\usr\\bin\\bash.exe",
    "terminal.integrated.shellArgs.windows": [
        "--login",
    ],
    "terminal.integrated.env.windows": {
        "CHERE_INVOKING": "1",
        "MSYSTEM": "MINGW64",
    }
}
```

在終端中執行 `make` 來建置 cppcheck。

若要除錯，於 `.vscode` 資料夾建立 `launch.json`，內容如下（涵蓋 cppcheck 與 misra.py 的除錯設定）：

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "cppcheck",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/cppcheck.exe",
            "args": [
                "--dump",
                "${workspaceFolder}/addons/test/misra/misra-test.c"
            ],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": true,
            "MIMode": "gdb",
            "miDebuggerPath": "C:/msys64/mingw64/bin/gdb.exe",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        },
        {
            "name": "misra.py",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/addons/misra.py",
            "console": "integratedTerminal",
            "args": [
                "${workspaceFolder}/addons/test/misra/misra-test.c.dump"
            ]
        }
    ]
}
```

### Qt Creator + MinGW

建置 CLI 需要 PCRE dll，可從此下載：
http://software-download.name/pcre-library-windows/

### GNU 編譯器

#### GNU make

簡單、未最佳化的建置（無相依性）：

```shell
make
```

你可以使用 `CXXOPTS`、`CPPOPTS`、`LDOPTS` 來附加到既有的 `CXXFLAGS`、`CPPFLAGS`、`LDFLAGS`，而不是覆寫它們。

建議的發行版建置：

```shell
make MATCHCOMPILER=yes FILESDIR=/usr/share/cppcheck HAVE_RULES=yes CXXOPTS="-O2" CPPOPTS="-DNDEBUG"
```

#### g++（進階使用者）

若你只想在無相依的情況下建置 Cppcheck，可使用：

```shell
g++ -o cppcheck -std=c++11 -Iexternals -Iexternals/simplecpp -Iexternals/tinyxml2 -Iexternals/picojson -Ilib -Ifrontend frontend/*.cpp cli/*.cpp lib/*.cpp externals/simplecpp/simplecpp.cpp externals/tinyxml2/tinyxml2.cpp
```

#### 旗標

-  `MATCHCOMPILER=yes`
   編譯時會將多個 `Token` 比對模式轉為更有效率的 C++ 程式碼（需要已安裝 Python）。

-  `FILESDIR=/usr/share/cppcheck`
   指定 cppcheck 檔案（addons、cfg、platform）安裝位置。

-  `HAVE_RULES=yes`
   啟用規則（需要已安裝 PCRE）。

-  `CXXOPTS="-O2"`
   啟用大部分編譯器最佳化。

-  `CPPOPTS="-DNDEBUG"`
   停用 assertions。

-  `HAVE_BOOST=yes`
   啟用 Boost 的更高效容器（需要已安裝 Boost）。

### MinGW

```shell
mingw32-make
```

若使用 `MATCHCOMPILER=yes` 時遇到以下錯誤，需透過 `PYTHON_INTERPRETER` 指定 Python 直譯器。

```
process_begin: CreateProcess(NULL, which python3, ...) failed.
makefile:24: pipe: No error
process_begin: CreateProcess(NULL, which python, ...) failed.
makefile:27: pipe: No error
makefile:30: *** Did not find a Python interpreter.  Stop.
```

### 其他編譯器/IDE

1. 建立空的專案檔/Makefile。
2. 將 cppcheck cli 與 lib 資料夾中的所有 cpp 檔加入專案檔/Makefile。
3. 將 externals 資料夾中的所有 cpp 檔加入專案檔/Makefile。
4. 編譯。

### 在 Linux 交叉編譯 Win32（CLI）版 Cppcheck

```shell
sudo apt-get install mingw32
make CXX=i586-mingw32msvc-g++ LDFLAGS="-lshlwapi" RDYNAMIC=""
mv cppcheck cppcheck.exe
```

## 套件

除了在你選擇的平台自行建置外，還有多種方式可取得預先建置的套件。<br/>

### 官方

官方套件由 Cppcheck 團隊維護。

- （Windows）官方 Windows 安裝程式可於 Cppcheck SourceForge 官方頁面取得：https://cppcheck.sourceforge.io。
- （Windows）目前開發版本的官方建置可透過 [release-windows](https://github.com/danmar/cppcheck/actions/workflows/release-windows.yml) 工作流程取得。`main` 分支為每晚建置，發行分支為每次提交建置。由於這些是開發版本，請勿用於生產環境！
  - 可攜版（portable）套件可從 `portable` artifact 取得，目前仍為進行中，詳見：https://trac.cppcheck.net/ticket/10771。
  - 安裝程式可從 `installer` artifact 取得。
- （多平台）由 Cppcheck 原作者提供、具額外功能的 Premium 版本可透過 https://www.cppcheck.com 購買。

### 第三方

第三方套件***不是***由 Cppcheck 團隊維護，而是由各自的打包者維護。

*Note:* 以下列表僅供資訊參考，順序不分先後。

*Note:* 請盡量從作業系統/發行版的官方主要來源取得套件，並確保取得最新釋出/標籤版本（請見 https://github.com/danmar/cppcheck/tags）。某些套件可能不包含最新修補版本。

*Note:* 部分問題可能與套件內含的額外補丁或打包方式相關。回報上游前，請先以官方版本驗證問題；否則可能需要回報給該套件維護者。文中原始錯字「need toreport」未修正。

- （Windows / Outdated）可攜版套件：https://portableapps.com/apps/development/cppcheck-portable
- （Windows / Outdated）套件：https://community.chocolatey.org/packages/cppcheck
- （Windows / Outdated）套件：https://winget.run/pkg/Cppcheck/Cppcheck
- （Windows）套件：https://scoop.sh/#/apps?q=cppcheck
- （Linux/Unix）多數主流發行版可透過其套件管理器（`yum`、`apt`、`pacman` 等）取得。概覽請見 https://pkgs.org/search/?q=cppcheck 或 https://repology.org/project/cppcheck。
- （Linux/Unix）除非使用 rolling 發行版，通常不會提供最新版本。另有多個外部（多為未支援）儲存庫，如 AUR（ArchLinux）、PPA（ubuntu）、EPEL（CentOS/Fedora）等可能提供較新版本。
- （Linux/Unix / Outdated）Canonical Snapcraft 套件（https://snapcraft.io/cppcheck / https://snapcraft.io/cppcheckgui）無人維護且包含非常舊的（開發）版本，請勿使用！詳情見 https://trac.cppcheck.net/ticket/11641。
- （MacOS）Homebrew 套件（`brew`）：https://formulae.brew.sh/formula/cppcheck
- （MacOS）套件：https://ports.macports.org/port/cppcheck
- （多平台）套件：https://anaconda.org/conda-forge/cppcheck
- （多平台）套件：https://conan.io/center/recipes/cppcheck
- 亦有來自各下載入口站的套件（主要為 Windows 安裝程式，有時為重新打包）。

## 網頁

https://cppcheck.sourceforge.io/
