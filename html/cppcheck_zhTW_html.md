# Cppcheck - C/C++ 靜態程式碼分析工具

## 頁面資訊
- 標題：Cppcheck - A tool for static C/C++ code analysis
- 說明：Cppcheck 是用於 C/C++ 程式碼的分析工具。它能偵測編譯器通常無法偵測的錯誤類型。目標是零誤報。
- 關鍵字：Cppcheck、開源、分析工具、C/C++、程式碼、錯誤、bug、編譯器、邊界檢查、記憶體洩漏、過時函式、未初始化變數、未使用函式
- RSS：Project News — `http://sourceforge.net/p/cppcheck/news/feed`

## 導覽
- 首頁：`/`
- Wiki：`http://sourceforge.net/p/cppcheck/wiki/`
- 論壇：`http://sourceforge.net/p/cppcheck/discussion/`
- 議題（Issues）：`http://trac.cppcheck.net`
- 開發者資訊：`/devinfo/`
- 線上示範：`/demo/`
- 專案頁：`http://sourceforge.net/projects/cppcheck/`

## 章節索引
- [Download](#download)
- [Features](#features)
- [News](#news)
- [Documentation](#documentation)
- [Support](#support)
- [Contribute](#contribute)

**Cppcheck** 是用於 C/C++ 程式碼的 **靜態分析工具**。它提供**獨特的程式碼分析**來偵測錯誤，並專注於偵測未定義行為與危險的程式碼結構。目標是將誤報（false positives）降到非常少。Cppcheck 的設計可分析你的 C/C++ 程式碼，即使它包含非標準語法（嵌入式專案中很常見）。

**Cppcheck** 同時提供開源版本（本頁）與具備擴充功能與支援的 **Cppcheck Premium**。更多資訊與商業版購買選項請見：`https://www.cppcheck.com?utm_source=sourceforge&utm_medium=opensource&utm_campaign=websitelink`

## Download

### Cppcheck 2.19（開源）

| 平台 | 檔案 |
| --- | --- |
| Windows 64-bit（不支援 XP） | [Installer](https://github.com/danmar/cppcheck/releases/download/2.19.0/cppcheck-2.19.0-x64-Setup.msi) |
| 原始碼（.zip） | [Archive](https://github.com/danmar/cppcheck/archive/2.19.0.zip) |
| 原始碼（.tar.gz） | [Archive](https://github.com/danmar/cppcheck/archive/2.19.0.tar.gz) |

### Packages
Cppcheck 也可由各種套件管理器安裝；不過你可能會取得較舊版本。

#### Debian
```
sudo apt-get install cppcheck
```

#### Fedora
```
sudo yum install cppcheck
```

#### Mac
```
brew install cppcheck
```

## Features
- 以獨特的程式碼分析偵測多種類型的錯誤。
- 提供命令列介面與圖形化介面。
- 特別著重偵測未定義行為。

### Unique analysis
使用多個靜態分析工具通常是好方法。每個工具都有其獨特特性，許多研究都已證實這點。

那麼 Cppcheck 的獨特之處在哪裡？

Cppcheck 使用 **不健全（unsound）的流程敏感（flow sensitive）分析**。其他分析器常使用基於抽象詮釋（abstract interpretation）的路徑敏感（path sensitive）分析，這也很棒，但各有優缺點。理論上，路徑敏感分析優於流程敏感分析；但在實務上，這代表 Cppcheck 會偵測到其他工具偵測不到的錯誤。

在 Cppcheck 中，資料流分析不僅是「向前（forward）」，而且是「雙向（bi-directional）」。多數分析器會診斷以下程式：

```c
void foo(int x)
{
    int buf[10];
    if (x == 1000)
        buf[x] = 0; // <- ERROR
}
```

多數工具能判斷陣列索引會是 1000，因此會越界。

Cppcheck 也會診斷以下情況：

```c
void foo(int x)
{
    int buf[10];
    buf[x] = 0; // <- ERROR
    if (x == 1000) {}
}
```

### Undefined behaviour
- 死指標
- 除以零
- 整數溢位
- 不合法的位移運算元
- 不合法的型別轉換
- 不合法的 <acronym title="Standard Template Library">STL</acronym> 使用
- 記憶體管理
- 空指標解參照
- 邊界越界檢查
- 未初始化變數
- 寫入 const 資料

### Security
2017 年最常見的安全性弱點類型（CVE 數量）如下：

| 類別 | 數量 | Cppcheck 是否可偵測 |
| --- | --- | --- |
| Buffer Errors | [2530](https://nvd.nist.gov/vuln/search/statistics?results_type=statistics&cwe_id=CWE-119) | 少數 |
| Improper Access Control | [1366](https://nvd.nist.gov/vuln/search/statistics?results_type=statistics&cwe_id=CWE-284) | 少數（非預期的後門） |
| Information Leak | [1426](https://nvd.nist.gov/vuln/search/statistics?results_type=statistics&cwe_id=CWE-200) | 少數（非預期的後門） |
| Permissions, Privileges, and Access Control | [1196](https://nvd.nist.gov/vuln/search/statistics?results_type=statistics&cwe_id=CWE-264) | 少數（非預期的後門） |
| Input Validation | [968](https://nvd.nist.gov/vuln/search/statistics?results_type=statistics&cwe_id=CWE-20) | 否 |

使用 Cppcheck 找到的 CVE：
- [CVE-2017-1000249](https://nvd.nist.gov/vuln/detail/CVE-2017-1000249)：檔案：堆疊式緩衝區溢位。由 Thomas Jarosch 使用 Cppcheck 發現，原因為條件判斷錯誤。
- [CVE-2013-6462](https://nvd.nist.gov/vuln/detail/CVE-2013-6462)：X.org 中 23 年的堆疊溢位，使用 Cppcheck 找到。此問題在多篇文章中被描述（[link](https://www.theregister.co.uk/2014/01/09/x11_has_privilege_escalation_bug/)）。
- [CVE-2012-1147](https://nvd.nist.gov/vuln/detail/CVE-2012-1147)：expat 2.1.0 之前的 readfilemap.c 允許情境依賴的攻擊者透過大量特製 XML 檔導致拒絕服務（檔案描述元耗盡）。

這些 CVE 在 Google 搜尋「cppcheck CVE」時會出現。也歡迎將搜尋結果與其他靜態分析工具做比較。

安全專家建議使用靜態分析，且從安全觀點來看，使用多種工具是最佳做法。

### Coding standards

| 編碼標準 | 開源版 | Premium |
| --- | --- | --- |
| Misra C 2012 - original rules | Partial | Yes |
| Misra C 2012 - amendment #1 | Partial | Yes |
| Misra C 2012 - amendment #2 | Partial | Yes |
| Misra C 2012 - amendment #3 |  | Yes |
| Misra C 2012 - amendment #4 |  | Yes |
| Misra C 2012 - Compliance report |  | Yes |
| Misra C 2012 - Rule texts | User provided | Yes |
| Misra C 2023 |  | Yes |
| Misra C++ 2008 |  | Yes |
| Misra C++ 2023 |  | Yes |
| Cert C |  | Yes |
| Cert C++ |  | Yes |
| Autosar |  | [Partial](https://files.cppchecksolutions.com/autosar.html) |

### All checks
Cppcheck 的所有檢查列表請見：`http://sourceforge.net/p/cppcheck/wiki/ListOfChecks`

## Clients and plugins
Cppcheck 已整合到許多常見開發工具中，例如：

- **Buildbot** - [integrated](https://docs.buildbot.net/latest/manual/configuration/steps/cppcheck.html)
- **CLion** - [Cppcheck plugin](https://plugins.jetbrains.com/plugin/8143)
- **Code::Blocks** - *integrated*
- **CodeDX**（軟體保證工具） - [integrated](http://codedx.com/code-dx-standard/)
- **CodeLite** - *integrated*
- **CppDepend 5** - [integrated](http://www.cppdepend.com/CppDependV5.aspx)
- **Eclipse** - [Cppcheclipse](https://github.com/cppchecksolutions/cppcheclipse/wiki/Installation)
- **gedit** - [gedit plugin](http://github.com/odamite/gedit-cppcheck)
- **github** - [Codacy](https://www.codacy.com/)、[Codety](https://www.codety.io/) 與 [SoftaCheck](http://www.softacheck.com/)
- **Hudson** - [Cppcheck Plugin](http://wiki.hudson-ci.org/display/HUDSON/Cppcheck+Plugin)
- **Jenkins** - [Cppcheck Plugin](http://wiki.jenkins-ci.org/display/JENKINS/Cppcheck+Plugin)
- **KDevelop** - [integrated since v5.1](https://kdevelop.org/)
- **Mercurial (Linux)** - [pre-commit hook](http://sourceforge.net/p/cppcheck/wiki/mercurialhook/) - 提交時檢查新錯誤（需互動式終端）
- **QtCreator** - [Qt Project Tool (qpt)](https://sourceforge.net/projects/qtprojecttool/files)
- **Tortoise SVN** - [Adding a pre-commit hook script](http://omerez.com/automatic-static-code-analysis/)
- **Vim** - [Vim Compiler](https://vimhelp.org/quickfix.txt.html#compiler-cppcheck)
- **Visual Studio** - [Visual Studio plugin](https://github.com/VioletGiraffe/cppcheck-vs-addin/releases/latest)
- **VScode** - [VScode plugin](https://marketplace.visualstudio.com/items?itemName=NathanJ.cppcheck-plugin)

## Other static analysis tools
使用多種工具比只用一種更好。每個工具都有獨特的程式碼分析，因此建議也搭配其他工具。

Cppcheck 主要關注錯誤而非風格問題，因此專注風格問題的工具是很好的補充。

Cppcheck 盡力避免誤報。但有時人們希望偵測所有錯誤，即使會產生許多誤警告，例如在發行前想確認完全沒有 bug。比 Cppcheck 更「吵」的工具可能是好的補充。

即使設計目標與 Cppcheck 相同的工具，也可能成為不錯的補充。靜態分析領域很大，Cppcheck 只涵蓋其中一小部分。沒有工具能覆蓋整個領域。要等到所有人工測試因某工具而淘汰的那一天，仍非常遙遠。

## News
- RSS 項目清單為空
- 查看所有新聞：`https://sourceforge.net/p/cppcheck/news/`

## Documentation
你可以閱讀 [manual](manual.pdf) 或下載一些 [articles](http://sourceforge.net/projects/cppcheck/files/Articles/)。

## Support
- 使用 [Trac](http://trac.cppcheck.net) 回報 bug 與功能需求
- 在 IRC 頻道提問：[irc://irc.libera.chat/#cppcheck](irc://irc.libera.chat/#cppcheck)

## Donate CPU
Cppcheck 專案是資源有限的興趣專案。你可以透過捐贈 CPU（1 核或更多）來協助我們，步驟很簡單：

1. 下載並解壓 Cppcheck 原始碼
2. 執行腳本：`python cppcheck/tools/donate-cpu.py`

此腳本會分析 Debian 原始碼並將結果上傳到 cppcheck 伺服器。我們需要這些結果來改進 Cppcheck 並偵測回歸問題。

你可隨時用 `Ctrl C` 停止腳本。

## Contribute
你可以參與貢獻，專案需要更多幫助。

可能有興趣的簡報：
- [Contribute to open source static analysis](https://www.youtube.com/watch?v=Cc_U1Hil0S4)

**Testing**
- 挑選專案並用最新版 Cppcheck 測試其原始碼。
- 將你在 Cppcheck 中發現的問題回報到 [Trac](http://trac.cppcheck.net)。

**Developing**
- 從 [Trac](http://trac.cppcheck.net) 挑選一個議題。
- 為該議題撰寫測試案例（並在該議題留言指出測試案例）。
- 或者挑選一個失敗的測試案例並嘗試修正。
- 製作 patch 並提交到 Trac：小改動可直接 inline；否則附加檔案提交。

**Marketing**
- 撰寫文章、評論，或告訴朋友們我們的專案。使用者越多、測試越多、專案就越好。

**Design**
- 想出新的檢查項目，並在 [Trac](http://trac.cppcheck.net) 建立 ticket。

**Integration**
- 為你喜歡的 IDE 撰寫外掛，或為你的發行版/作業系統建立套件。

**Technical Writing**
- 改善對於已發現 bug 的文件。目前只有少量 bug 有文件說明。
