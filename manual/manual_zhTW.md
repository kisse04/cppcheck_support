# Cppcheck Premium 使用手冊
Cppcheck 團隊，Cppcheck Solutions AB

## 簡介
Cppcheck 是用於 C/C++ 程式碼的分析工具。它提供獨特的程式碼分析來偵測錯誤，並專注於偵測未定義行為與危險的程式碼結構。目標是只偵測真正的錯誤，並盡可能產生少量的誤報（錯誤地回報的警告）。Cppcheck 的設計可分析你的 C/C++ 程式碼，即使它包含非標準語法（例如嵌入式專案常見的情況）。

支援的程式碼與平台：
- Cppcheck 會檢查包含各種編譯器擴充、內嵌組語碼等的非標準程式碼。
- Cppcheck 應該可由任何支援 C++11 或更新版本的編譯器編譯。
- Cppcheck 跨平台，可用於各種 POSIX/Windows 等環境。

Cppcheck 的檢查並非完美。有些應該被找出的錯誤，Cppcheck 可能無法偵測。

### 關於靜態分析
靜態分析可找出的錯誤類型：
- 未定義行為
- 使用危險的程式碼模式
- 程式碼風格

也有許多錯誤無法透過靜態分析找出。靜態分析工具並不了解你的程式真正意圖。如果程式輸出雖然有效但不符合預期，多數情況下不會被靜態分析工具偵測到。例如：若小程式在螢幕上輸出 “Helo” 而非 “Hello”，很可能沒有任何工具會抱怨。

靜態分析應作為品質保證的補充，它不能取代：
- 謹慎的設計
- 測試
- 動態分析
- Fuzzing

## 開始使用
### GUI
雖然不是必須，但建立新的專案檔是很好的第一步。你可以調整一些選項以獲得更好的結果。

在專案設定對話框中，第一個選項是「Import project」。建議可用時優先使用此功能。Cppcheck 可以匯入：
- Visual Studio solution / project
- 編譯資料庫（可由 CMake/qbs 等建置檔產生）
- Borland C++ Builder 6

填完專案設定並按下 OK 後，Cppcheck 會開始分析。

### 命令列
#### 第一次測試
以下是簡單程式碼：

```c
int main()
{
    char a[10];
    a[10] = 0;
    return 0;
}
```

將其存成 `file1.c` 並執行：

```
cppcheck file1.c
```

Cppcheck 的輸出會是：

```
Checking file1.c...
[file1.c:4]: (error) Array 'a[10] 'index 10 out of bounds
```

#### 檢查資料夾中的所有檔案
一般程式會有許多原始檔。Cppcheck 可檢查目錄中的所有原始檔：

```
cppcheck path
```

若 `path` 是資料夾，Cppcheck 會遞迴檢查該資料夾內所有原始檔：

```
Checking path/file1.cpp...
1/2 files checked 50% done
Checking path/file2.cpp...
2/2 files checked 100% done
```

#### 手動檢查或使用專案檔
你可以手動指定要檢查的檔案/路徑與設定，或使用建置環境（如 CMake 或 Visual Studio）。

我們無法確定哪種方式（專案檔或手動設定）會有最好結果，建議兩者都試試。可能會得到不同結果，要找到最多錯誤可能需要同時使用兩種方式。後續章節會更詳細說明。

#### 依檔案篩選器檢查
使用 `--file-filter=<str>` 可設定檔案篩選器，只檢查符合的檔案。

例如下列命令表示可以檢查 `src/test1.cpp` 與 `src/test/file1.cpp`，但不會檢查 `src/file2.cpp`：

```
cppcheck src/ --file-filter=src/test*
```

檔案篩選器可使用 `**`、`*`、`?`：
- `**`：匹配零個或多個字元（含路徑分隔符）
- `*`：匹配零個或多個字元（不含路徑分隔符）
- `?`：匹配任意單一字元（不含路徑分隔符）

`--file-filter` 的常見用途是檢查整個專案，但只檢查特定檔案：

```
cppcheck --project=compile_commands.json --file-filter=src/*.c
```

通常 `compile_commands.json` 會包含絕對路徑。但不管它包含絕對或相對路徑，`--file-filter=src/*.c` 的意義是：
- 相對路徑為 `test1.c` 的檔案不會被檢查。
- 相對路徑為 `src/test2.c` 的檔案會被檢查。
- 相對路徑為 `src/test3.cpp` 的檔案不會被檢查。

#### 排除檔案或資料夾
選項 `-i` 用於指定要排除的檔案/資料夾範圍。例如以下指令會排除 `src/c` 下的所有檔案：

```
cppcheck -isrc/c src
```

`-i` 不會在前處理階段使用，無法用來排除被 include 的標頭。

模式可使用 `**`、`*`、`?`：
- `**`：匹配零個或多個字元（含路徑分隔符）
- `*`：匹配零個或多個字元（不含路徑分隔符）
- `?`：匹配任意單一字元（不含路徑分隔符）

`-i` 的常見用途是檢查專案，但排除特定檔案/資料夾：

```
cppcheck --project=compile_commands.json -itest
```

通常 `compile_commands.json` 會包含絕對路徑。但不管它包含絕對或相對路徑，`-itest` 的意義是：
- 相對路徑為 `test1.cpp` 的檔案會被檢查。
- 相對路徑為 `test/somefile.cpp` 的檔案不會被檢查。

#### Clang 解析器（實驗性）
預設 Cppcheck 使用內建 C/C++ 解析器。不過有實驗性選項可改用 Clang 解析器。

先安裝 clang，然後使用 `--clang`。

技術上，Cppcheck 會執行 clang 並使用 `-ast-dump` 選項。Clang 的輸出會被匯入並轉成 Cppcheck 的正常格式，再進行一般 Cppcheck 分析。

也可以透過 `--clang=clang-10` 指定自訂 clang 執行檔，或使用路徑指定。Windows 上若未用路徑，會自動加上 `.exe` 副檔名。

## 嚴重性（Severities）
訊息可能的嚴重性如下：

**error**
- 程式碼執行時會發生未定義行為或其他錯誤，例如記憶體洩漏或資源洩漏。

**warning**
- 程式碼執行時可能出現未定義行為。

**style**
- 風格問題，例如未使用的函式、冗餘程式碼、const 正確性、運算子優先順序、可能的錯誤。

**performance**
- 根據常見知識提出的效能建議，但不一定能量化速度提升。

**portability**
- 可攜性警告。實作定義行為、64 位可攜性，或「可能如你所想」的未定義行為等。

**information**
- 設定問題，與語法正確性無關，但 Cppcheck 設定可改進。

## 範本程式碼的可能加速分析
Cppcheck 會具現化（instantiate）你的程式碼中的樣板。若樣板遞迴，可能導致分析變慢並消耗大量記憶體。當偵測到潛在問題時，Cppcheck 會輸出資訊訊息。

範例程式碼：

```cpp
template <int i>
void a()
{
    a<i+1>();
}
void foo()
{
    a<0>();
}
```

Cppcheck 輸出：

```
test.cpp:4:5: information: TemplateSimplifier: max template
recursion (100) reached for template 'a<101> '. You might
want to limit Cppcheck recursion. [templateRecursion]
    a<i+1>();
    ^
```

如你所見，Cppcheck 已具現化 `a<i+1>` 直到 `a<101>`，然後停止。

限制樣板遞迴的方法：
- 加入樣板特化
- 設定 Cppcheck（可在 GUI 專案檔對話框中設定）

含樣板特化的範例：

```cpp
template <int i>
void a()
{
    a<i+1>();
}
void foo()
{
    a<0>();
}
#ifdef __cppcheck__
template<> void a<3>() {}
#endif
```

檢查此程式碼時可使用 `-D__cppcheck__`。

## Cppcheck 建置資料夾
使用 Cppcheck 建置資料夾不是強制，但建議使用。Cppcheck 會在該資料夾保存分析資訊。

優點：
- 加速分析，允許增量分析。重新檢查時只會分析變更的檔案。
- 多執行緒時仍可進行整體程式分析。

命令列設定方式：`--cppcheck-build-dir=path`。

範例：

```
mkdir b
# 所有檔案都被分析
cppcheck --cppcheck-build-dir=b src
# 更快！會重用未變更檔案的結果
cppcheck --cppcheck-build-dir=b src
```

GUI 中則在專案設定中設定。

## 匯入專案
你可以匯入部分專案檔與建置設定。

### Cppcheck GUI 專案
你可以在命令列工具中匯入並使用 Cppcheck GUI 專案檔：

```
cppcheck --project=foobar.cppcheck
```

Cppcheck GUI 有些選項命令列無法直接使用。若要使用這些選項，可匯入 GUI 專案檔。命令列工具的用法刻意保持簡潔，因此選項有限。

要在專案中忽略特定資料夾，可用 `-i`：

```
cppcheck --project=foobar.cppcheck -ifoo
```

### CMake
產生編譯資料庫：

```
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON .
```

會在目前資料夾產生 `compile_commands.json`。接著執行：

```
cppcheck --project=compile_commands.json
```

要忽略特定資料夾可用 `-i`：

```
cppcheck --project=compile_commands.json -ifoo
```

### Visual Studio
可對單一專案檔（`*.vcxproj`）或整個解決方案（`*.sln`）執行 Cppcheck。

對整個解決方案執行：

```
cppcheck --project=foobar.sln
```

對單一專案執行：

```
cppcheck --project=foobar.vcxproj
```

兩者都會分析所有可用設定。若要限定單一設定：

```
cppcheck --project=foobar.sln "--project-configuration=Release|Win32"
```

在 Cppcheck GUI 中可選擇只分析單一 debug 設定。若要在命令列使用此選項，請在 GUI 建立此設定後，再匯入 GUI 專案檔。

要忽略特定資料夾可用 `-i`：

```
cppcheck --project=foobar.vcxproj -ifoo
```

### C++ Builder 6
對 C++ Builder 6 專案執行：

```
cppcheck --project=foobar.bpr
```

要忽略特定資料夾可用 `-i`：

```
cppcheck --project=foobar.bpr -ifoo
```

### 其他
若能產生編譯資料庫，就能匯入 Cppcheck。

在 Linux 中可使用 bear（build ear）工具從任意建置工具產生編譯資料庫：

```
bear -- make
```

## 前處理器設定
若使用 `--project`，Cppcheck 會自動使用匯入專案檔內的前處理器設定，你大多不需額外設定。

若未使用 `--project`，可能需要手動設定一些前處理器選項。不過 Cppcheck 也會自動配置 defines。

### 自動配置前處理器 defines
Cppcheck 會自動嘗試不同的前處理器 define 組合，以盡可能提高分析覆蓋率。

以下檔案有 3 個錯誤（當 x、y、z 被指派時）：

```c
#ifdef A
x=100/0;
#ifdef B
y=100/0;
#endif
#else
z=100/0;
#endif
#ifndef C
#error C must be defined
#endif
```

`-D` 表示名稱已定義。若未使用該 define，Cppcheck 不會分析。`-U` 表示名稱未定義。若未使用該 define，Cppcheck 也不會分析。`--force` 與 `--max-configs` 用於控制要檢查的組合數量。

使用 `-D` 時，Cppcheck 只會檢查 1 個設定，除非搭配以下選項。

範例：

```
# 測試所有設定
# 可找到所有錯誤
cppcheck test.c
# 只測試設定 "-DA"
# 找不到錯誤（#error）
cppcheck -DA test.c
# 只測試設定 "-DA -DC"
# 找到第一個錯誤
cppcheck -DA -DC test.c
# 測試設定 "-DC"
# 找到最後一個錯誤
cppcheck -UA test.c
# 測試所有包含 "-DA" 的設定
# 找到前兩個錯誤
cppcheck --force -DA test.c
```

### Include 路徑
要加入 include 路徑，使用 `-I` 後接路徑。

Cppcheck 的前處理器基本上像一般前處理器一樣處理 include，但當遇到缺少的標頭時，其他前處理器會停止，Cppcheck 只會輸出資訊訊息並繼續解析程式碼。

此行為的目的，是讓 Cppcheck 不一定要看到整個程式碼也能運作。實際上建議不要提供所有 include 路徑。雖然讓 Cppcheck 看到類別宣告有助於檢查成員實作，但傳入標準程式庫標頭並不建議，因為分析無法完全正確，且會讓檢查時間變長。對這類情況，建議使用 `.cfg` 檔提供函式與型別的實作資訊，詳見下文。

## 平台
請使用與目標環境一致的平台設定。預設 Cppcheck 使用本機平台設定，若你的程式碼在本機編譯與執行通常可正常運作。

Cppcheck 內建 Unix 與 Windows 的平台設定，可用 `--platform` 指定。

也可以建立自訂平台設定 XML，例如：

```xml
<?xml version="1"?>
<platform>
  <char_bit>8</char_bit>
  <default-sign>signed</default-sign>
  <sizeof>
    <short>2</short>
    <int>4</int>
    <long>4</long>
    <long-long>8</long-long>
    <float>4</float>
    <double>8</double>
    <long-double>12</long-double>
    <pointer>4</pointer>
    <size_t>4</size_t>
    <wchar_t>2</wchar_t>
  </sizeof>
</platform>
```

## C/C++ 標準
使用命令列 `--std` 指定 C/C++ 標準。

Cppcheck 會假設程式碼相容最新 C/C++ 標準，但可用此選項覆寫。

可用選項：
- `c89`：C 程式碼相容 C89
- `c99`：C 程式碼相容 C99
- `c11`：C 程式碼相容 C11
- `c17`：C 程式碼相容 C17
- `c23`：C 程式碼相容 C23（預設）
- `c++03`：C++ 程式碼相容 C++03
- `c++11`：C++ 程式碼相容 C++11
- `c++14`：C++ 程式碼相容 C++14
- `c++17`：C++ 程式碼相容 C++17
- `c++20`：C++ 程式碼相容 C++20
- `c++23`：C++ 程式碼相容 C++23
- `c++26`：C++ 程式碼相容 C++26（預設）

## Cppcheck 建置目錄
使用 Cppcheck 建置目錄是很好的作法。命令列使用 `--cppcheck-build-dir`，GUI 則在專案選項中設定。

重新檢查程式碼會更快。Cppcheck 不會分析未變更的程式碼，舊的警告會從建置目錄載入並再次回報。

若使用多執行緒，整體程式分析無法運作；除非你使用 Cppcheck 建置目錄。例如 `unusedFunction` 警告需要整體程式分析。

## 抑制（Suppressions）
如果要過濾掉某些錯誤不生成警告，可以使用抑制。

若遇到誤報，請回報給 Cppcheck 團隊以便修正。

### 純文字抑制
錯誤抑制的格式為：

```
[error id]:[filename]:[line]
[error id]:[filename2]
[error id]
```

error id 是要抑制的訊息 id。警告 id 會在一般 cppcheck 文字輸出中以方括號顯示。

error id 與 filename 模式可使用 `**`、`*`、`?`：
- `**`：匹配零個或多個字元（含路徑分隔符）
- `*`：匹配零個或多個字元（不含路徑分隔符）
- `?`：匹配任意單一字元（不含路徑分隔符）

建議所有作業系統的檔名模式都使用正斜線 `/` 作為路徑分隔符。

### 命令列抑制
使用命令列 `--suppress=` 指定抑制，例如：

```
cppcheck --suppress=memleak:src/file1.cpp src/
```

### 抑制檔案
你可以建立抑制檔，例如：

```text
// suppress memleak and exceptNew errors in the file src/file1.cpp
memleak:src/file1.cpp
exceptNew:src/file1.cpp
uninitvar // suppress all uninitvar errors in all files
```

抑制檔可包含空白行與註解。註解必須以 `#` 或 `//` 開頭，且位於行首或抑制行之後。

使用抑制檔的方式：

```
cppcheck --suppressions-list=suppressions.txt src/
```

### XML 抑制
可用 XML 檔指定抑制，例如：

```xml
<?xml version="1.0"?>
<suppressions>
  <suppress>
    <id>uninitvar</id>
    <fileName>src/file1.c</fileName>
    <lineNumber>10</lineNumber>
    <symbolName>var</symbolName>
  </suppress>
</suppressions>
```

`id` 與 `fileName` 模式可使用 `**`、`*`、`?`：
- `**`：匹配零個或多個字元（含路徑分隔符）
- `*`：匹配零個或多個字元（不含路徑分隔符）
- `?`：匹配任意單一字元（不含路徑分隔符）

XML 格式可擴充，未來可能加入更多屬性。

使用 XML 抑制檔的方式：

```
cppcheck --suppress-xml=suppressions.xml src/
```

### 行內抑制（Inline suppressions）
你也可以在程式碼中加入包含特殊關鍵字的註解來抑制警告。但加入註解會略微犧牲可讀性。

以下程式碼通常會產生錯誤訊息：

```c
void f() {
    char arr[5];
    arr[10] = 0;
}
```

輸出：

```
cppcheck test.c
[test.c:3]: (error) Array 'arr[5] 'index 10 out of bounds
```

啟用行內抑制：

```
cppcheck --inline-suppr test.c
```

#### 格式
可用以下方式抑制警告：

```text
// cppcheck-suppress aaaa
```

用 `[]` 在同一註解中抑制多個 id：

```text
// cppcheck-suppress [aaaa, bbbb]
```

針對一段程式碼抑制警告 aaaa：

```text
// cppcheck-suppress-begin aaaa
...
// cppcheck-suppress-end aaaa
```

針對一段程式碼抑制多個 id：

```text
// cppcheck-suppress-begin [aaaa, bbbb]
...
// cppcheck-suppress-end [aaaa, bbbb]
```

針對整個檔案抑制警告 aaaa：

```text
// cppcheck-suppress-file aaaa
```

針對整個檔案抑制多個 id：

```text
// cppcheck-suppress-file [aaaa, bbbb]
```

在巨集使用處抑制警告 aaaa：

```text
// cppcheck-suppress-macro aaaa
#define MACRO ...
...
x = MACRO; // <- aaaa warnings are suppressed here
```

在巨集使用處抑制多個 id：

```text
// cppcheck-suppress-macro [aaaa, bbbb]
#define MACRO ...
...
x = MACRO; // <- aaaa and bbbb warnings are suppressed here
```

#### 註解可放在程式碼前或同一行
程式碼前：

```c
void f() {
    char arr[5];
    // cppcheck-suppress arrayIndexOutOfBounds
    arr[10] = 0;
}
```

程式碼同一行：

```c
void f() {
    char arr[5];
    arr[10] = 0; // cppcheck-suppress arrayIndexOutOfBounds
}
```

在此例中有兩行程式碼與一個抑制註解。抑制註解只作用在 1 行：`a = b + c;`。

```c
void f() {
    a = b + c; // cppcheck-suppress abc
    d = e + f;
}
```

特殊情況（向後相容）：若註解與 `{` 在同一行，則抑制會套用到第一行程式碼。

```c
void f() { // cppcheck-suppress arrayIndexOutOfBounds
    char arr[5];
    arr[10] = 0;
}
```

可抑制多個 id：

```c
// cppcheck-suppress arrayIndexOutOfBounds
// cppcheck-suppress zerodiv
arr[10] = arr[10] / 0;
```

使用單一抑制註解在程式碼前：

```c
void f() {
    char arr[5];
    // cppcheck-suppress[arrayIndexOutOfBounds,zerodiv]
    arr[10] = arr[10] / 0;
}
```

程式碼同一行：

```c
void f() {
    char arr[5];
    arr[10] = arr[10] / 0; // cppcheck-suppress[arrayIndexOutOfBounds,zerodiv]
}
```

#### Symbol name
你可以指定行內抑制只套用到特定符號：

```text
// cppcheck-suppress aaaa symbolName=arr
```

或：

```text
// cppcheck-suppress[aaaa symbolName=arr, bbbb]
```

#### 抑制說明註解
你可以在抑制中加入說明：

```text
// cppcheck-suppress[warningid] some comment
// cppcheck-suppress warningid ; some comment
// cppcheck-suppress warningid // some comment
```

## XML 輸出
Cppcheck 可產生 XML 格式輸出。使用 `--xml` 開啟。

檢查檔案並輸出 XML 的範例：

```
cppcheck --xml file1.cpp
```

範例報告：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<results version="2">
  <cppcheck version="1.66"/>
  <errors>
    <error id="someError" severity="error" msg="short error text"
           verbose="long error text" inconclusive="true" cwe="312">
      <location file0="file.c" file="file.h" line="1"/>
    </error>
  </errors>
</results>
```

### `<error>` 元素
每個錯誤都以 `<error>` 元素回報。屬性如下：
- `id`：錯誤 id，也是有效符號名稱
- `severity`：error/warning/style/performance/portability/information
- `msg`：短格式的錯誤訊息
- `verbose`：長格式的錯誤訊息
- `inconclusive`：當錯誤訊息不確定時使用
- `cwe`：問題的 CWE ID（僅當訊息已知對應 CWE 時使用）
- `remark`：可選屬性，為 remark 註解的說明/理由

### `<location>` 元素
錯誤所有相關位置會以 `<location>` 列出，主要位置列在最前。

屬性：
- `file`：檔名，可為相對或絕對路徑
- `file0`：來源檔名（可選）
- `line`：行號
- `info`：該位置的簡短資訊（可選）

## 重新格式化文字輸出
若要讓輸出看起來不同，可以使用範本（template）。

### 預定輸出格式
使用 `--template=vs` 可得到 Visual Studio 相容輸出：

```
cppcheck --template=vs samples/arrayIndexOutOfBounds/bad.c
```

輸出如下：

```
Checking samples/arrayIndexOutOfBounds/bad.c ...
samples/arrayIndexOutOfBounds/bad.c(6): error: Array
'a[2] 'accessed at index 2, which is out of bounds.
```

使用 `--template=gcc` 可得到 gcc 相容輸出：

```
cppcheck --template=gcc samples/arrayIndexOutOfBounds/bad.c
```

輸出如下：

```
Checking samples/arrayIndexOutOfBounds/bad.c ...
samples/arrayIndexOutOfBounds/bad.c:6:6: warning: Array
'a[2] 'accessed at index 2, which is out of bounds. [arrayIndexOutOfBounds]
a[2] = 0;
^
```

### 使用者自訂輸出格式（單行）
可自訂輸出樣式，例如：

```
cppcheck \
  --template="{file}:{line}:{column}: {severity}:{message}" \
  samples/arrayIndexOutOfBounds/bad.c
```

輸出：

```
Checking samples/arrayIndexOutOfBounds/bad.c ...
samples/arrayIndexOutOfBounds/bad.c:6:6: error: Array
'a[2] 'accessed at index 2, which is out of bounds.
```

逗號分隔格式：

```
cppcheck \
  --template="{file},{line},{severity},{id},{message}" \
  samples/arrayIndexOutOfBounds/bad.c
```

輸出：

```
Checking samples/arrayIndexOutOfBounds/bad.c ...
samples/arrayIndexOutOfBounds/bad.c,6,error,arrayIndexOutOfBounds,
Array 'a[2] 'accessed at index 2, which is out of bounds.
```

### 使用者自訂輸出格式（多行）
許多警告會包含多個位置。範例程式碼：

```c
void f(int *p)
{
    *p = 3; // line 3
}
int main()
{
    int *p = 0; // line 8
    f(p); // line 9
    return 0;
}
```

在第 3 行可能有空指標解參照。Cppcheck 可顯示推導過程的額外位置資訊。你需要同時使用 `--template` 與 `--template-location`，例如：

```
cppcheck \
  --template="{file}:{line}: {severity}: {message}\n{code}" \
  --template-location="{file}:{line}: note: {info}\n{code}" multiline.c
```

Cppcheck 輸出：

```
Checking multiline.c ...
multiline.c:3: warning: Possible null pointer dereference: p
*p = 3;
^
multiline.c:8: note: Assignment 'p=0', assigned value is 0
int *p = 0;
^
multiline.c:9: note: Calling function 'f', 1st argument 'p'value is 0
f(p);
^
multiline.c:3: note: Null pointer dereference
*p = 3;
^
```

第一行警告由 `--template` 格式化，其餘行則由 `--template-location` 格式化。

### `--template` 的格式化符號
可用符號：
- `{file}`：檔名
- `{line}`：行號
- `{column}`：欄位
- `{callstack}`：輸出所有位置，每個位置以 `[{file}:{line}]` 表示，並以 `->` 分隔。例如：`[multiline.c:8] -> [multiline.c:9] -> [multiline.c:3]`
- `{inconclusive:text}`：若警告不確定，輸出指定文字（文字不可包含 `}`），例如 `{inconclusive:inconclusive,}`
- `{severity}`：error/warning/style/performance/portability/information
- `{message}`：警告訊息
- `{id}`：警告 id
- `{remark}`：若有 remark 註解，輸出 remark 文字
- `{code}`：實際程式碼
- `\t`：Tab
- `\n`：換行
- `\r`：CR

### `--template-location` 的格式化符號
可用符號：
- `{file}`：檔名
- `{line}`：行號
- `{column}`：欄位
- `{info}`：該位置的資訊訊息
- `{code}`：實際程式碼
- `\t`：Tab
- `\n`：換行
- `\r`：CR

## 報告中的警告理由（Justifications）
你可以在原始碼加入 remark 註解，說明為何有警告/違規。

remark 註解需：
- 以 `REMARK` 開頭
- 可加在產生警告的程式碼上方，或同一行的後方

範例：

```c
void foo(void) {
    // REMARK Initialize x with 0
    int x = 0;
}
```

Cppcheck 文字輸出預設不顯示 remark，可用 `--template` 的 `{remark}` 顯示：

```
$ ./cppcheck --enable=style \
  --template="{file}:{line}: {message} [{id}]\n{remark}" test1.c
Checking test1.c ...
test1.c:4: Variable 'x'is assigned a value that is never used. [unreadVariable]
Initialize x with 0
```

在 XML 輸出中，註解文字會出現在 `remark` 屬性：

```
$ ./cppcheck --enable=style --xml test1.c
....
remark="Initialize x with 0"
....
```

## 外掛（Addons）
外掛是用於分析 Cppcheck dump 檔的腳本，以檢查安全編碼規範相容性並定位問題。

Cppcheck 內建一些外掛，如下所列。

### 支援的外掛
**namingng.py**
- 可設定並檢查命名規範。
- 需要一個定義命名規範的設定檔。預設檔名為 `namingng.config.json`，也可指定其他檔名。

命名規範設定範例：

```json
{
  "RE_VARNAME": ["[a-z]*[a-zA-Z0-9_]*\\Z"],
  "RE_PRIVATE_MEMBER_VARIABLE": null,
  "RE_FUNCTIONNAME": ["[a-z0-9A-Z]*\\Z"],
  "_comment": "comments can be added to the config with underscore-prefixed keys",
  "include_guard": {
    "input": "path",
    "prefix": "GUARD_",
    "case": "upper",
    "max_linenr": 5,
    "RE_HEADERFILE": "[^/].*\\.h\\Z",
    "required": true
  },
  "var_prefixes": {"uint32_t": "ui32"},
  "function_prefixes": {"uint16_t": "ui16",
                         "uint32_t": "ui32"}
}
```

**threadsafety.py**
- 分析 Cppcheck dump 檔，找出執行緒安全問題（例如多執行緒使用的 static local 物件）。

**y2038.py**
- 檢查 Linux 系統的 2038 年問題安全性。需修改過的環境。詳見完整說明。

### 執行外掛
使用 `--addon` 執行外掛：

```
cppcheck --addon=namingng.py somefile.c
```

若有自訂腳本也可用：

```
cppcheck --addon=mychecks.py somefile.c
```

可用 JSON 檔設定外掛執行方式，例如：

```json
{
  "script": "mychecks.py",
  "args": [
    "--some-option"
  ],
  "ctu": false
}
```

使用該 JSON 執行外掛：

```
cppcheck --addon=mychecks.json somefile.c
```

Cppcheck 會先在本地資料夾尋找外掛，再到安裝資料夾。也可明確指定路徑，例如：

```
cppcheck --addon=path/to/my-addon.py somefile.c
```

## 程式庫設定
使用外部程式庫（如 WinAPI、POSIX、gtk、Qt 等）時，Cppcheck 不知道這些程式庫的函式、型別或巨集，可能導致分析失敗或誤判。但可透過適當的設定檔修正。

Cppcheck 已包含多個程式庫設定檔，可依下述方式載入。注意：C/C++ 標準函式庫設定檔 `std.cfg` 永遠會載入。若你為常見程式庫建立或更新設定檔，歡迎提供給 Cppcheck 專案。

### 使用 .cfg 檔
使用 `--library=<lib>` 載入 Cppcheck 內建 .cfg 檔。下表為目前已存在的程式庫：

| .cfg 檔案 | 程式庫 | 備註 |
| --- | --- | --- |
| avr.cfg |  |  |
| bento4.cfg | Bento4 |  |
| boost.cfg | Boost |  |
| bsd.cfg | BSD |  |
| cairo.cfg | cairo |  |
| cppcheck-lib.cfg | Cppcheck | 用於 Cppcheck 程式碼庫的自我檢查 |
| cppunit.cfg | CppUnit |  |
| dpdk.cfg |  |  |
| embedded_sql.cfg |  |  |
| emscripten.cfg |  |  |
| ginac.cfg |  |  |
| gnu.cfg | GNU |  |
| googletest.cfg | GoogleTest |  |
| gtk.cfg | GTK |  |
| icu.cfg |  |  |
| kde.cfg | KDE |  |
| libcerror.cfg | libcerror |  |
| libcurl.cfg | libcurl |  |
| libsigc++.cfg | libsigc++ |  |
| lua.cfg |  |  |
| mfc.cfg | MFC |  |
| microsoft_atl.cfg | ATL |  |
| microsoft_sal.cfg | SAL annotations |  |
| microsoft_unittest.cfg | CppUnitTest |  |
| motif.cfg |  |  |
| nspr.cfg |  |  |
| ntl.cfg |  |  |
| opencv2.cfg | OpenCV |  |
| opengl.cfg | OpenGL |  |
| openmp.cfg | OpenMP |  |
| openssl.cfg | OpenSSL |  |
| pcre.cfg | PCRE |  |
| posix.cfg | POSIX |  |
| python.cfg |  |  |
| qt.cfg | Qt |  |
| ruby.cfg |  |  |
| sdl.cfg |  |  |
| sfml.cfg |  |  |
| sqlite3.cfg | SQLite |  |
| std.cfg | C/C++ 標準函式庫 | 預設載入 |
| tinyxml2.cfg | TinyXML-2 |  |
| vcl.cfg |  |  |
| windows.cfg | Win32 API |  |
| wxsqlite3.cfg |  |  |
| wxsvg.cfg |  |  |
| wxwidgets.cfg | wxWidgets |  |
| zephyr.cfg |  |  |
| zlib.cfg | zlib |  |

### 建立自訂 .cfg 檔
你可以為專案建立自己的 .cfg 檔。使用 `--check-library` 可取得建議提示。

你可以在 Cppcheck GUI 中使用 Library Editor 編輯設定檔，位於 View 選單。

`.cfg` 檔格式詳見「Reference: Cppcheck .cfg format」文件（https://cppcheck.sourceforge.io/reference-cfg-format.pdf）。

## HTML 報告
可將 Cppcheck 的 XML 輸出轉成 HTML 報告。需要 Python 與 pygments 模組（http://pygments.org/）。

在 Cppcheck 原始碼樹中有 `htmlreport` 資料夾，內含可將 Cppcheck XML 轉成 HTML 的腳本。

以下指令產生說明畫面：

```
htmlreport/cppcheck-htmlreport -h
```

輸出內容：

```
Usage: cppcheck-htmlreport [options]
Options:
-h, --help show this help message and exit
--file=FILE The cppcheck xml output file to read defects from.
Default is reading from stdin.
--report-dir=REPORT_DIR
The directory where the html report content is written.
--source-dir=SOURCE_DIR
Base directory where source code files can be found.
```

使用範例：

```
cppcheck gui/test.cpp --xml 2> err.xml
cppcheck-htmlreport --file=err.xml --report-dir=test1 --source-dir=.
```

## 檢查等級
### Reduced
「reduced」檢查等級會進行有限的資料流分析。若開發者希望在開發時直接執行 cppcheck，並需要比「normal」更快的結果，可考慮使用。

### Normal
預設為「normal」。目標是在「合理時間」內提供有效的檢查。

「normal」適用於開發期間：
- 編輯檔案時檢查
- 阻擋變更進入儲存庫
- 等等

### Exhaustive
若可以等待更久以取得結果，可使用 `--check-level=exhaustive` 啟用「exhaustive」檢查。

「exhaustive」適合：
- 每晚建置
- 等等

## 加速分析
### 限制前處理器設定
基於效能考量，可能需要限制要檢查的前處理器設定組合。

### 限制 ValueFlow：max if count
命令列選項 `--performance-valueflow-max-if-count` 可調整函式內 if 的最大數量。

超過此限制會在該函式中限制資料流分析。限制並不激烈：
- 其他函式的分析不受影響。
- 僅針對某些特定資料流分析；仍有一些資料流分析一定會執行。
- 所有檢查仍會執行。受限函式仍可能有許多警告。

有些資料流分析的時間會隨 if 數量呈指數增長，此限制用來避免分析時間爆炸。

### GUI 選項
GUI 中有多個限制分析的選項。

在 GUI：
- 開啟專案對話框。
- 在「Analysis」分頁有多個選項。

若也想在命令列使用這些限制，可匯入 GUI 專案檔並使用 `--project`。

## Cppcheck Premium
### Bug hunting
這種分析比一般分析更「吵」，多數警告會是誤報（cppcheck 會錯誤地指出有問題）。設計目標是在每個檔案中不超過約 5～10 個誤報。

這並不適合用於一般 CI 或日常開發的靜態分析，噪音太高，因此不適用。

它適合用於你正在找 bug 並可以接受噪音的情境，例如：
- 你剛開發新功能，想確認沒有 bug。
- 作為產品發行測試的一部分，只對修改過的檔案進行 bug hunting。
- 等等

技術上，「sound」分析會偵測所有 bug；「soundy」的目標是偵測大多數 bug，並將噪音維持在合理水準。

Cppcheck 的 bug hunting 分析是「soundy」。

命令：

```
cppcheck --premium=bughunting ....
```

### 編碼標準
啟用 Autosar 檢查器：

```
cppcheck --premium=autosar ....
```

啟用 Cert C 檢查器：

```
cppcheck --premium=cert-c ....
```

啟用 Cert C++ 檢查器：

```
cppcheck --premium=cert-c++ ....
```

啟用 Misra C 2012 檢查器：

```
cppcheck --premium=misra-c-2012 ....
```

啟用 Misra C 2023 檢查器：

```
cppcheck --premium=misra-c-2023 ....
```

啟用 Misra C 2025 檢查器：

```
cppcheck --premium=misra-c-2025 ....
```

啟用 Misra C++ 2008 檢查器：

```
cppcheck --premium=misra-c++-2008 ....
```

啟用 Misra C++ 2023 檢查器：

```
cppcheck --premium=misra-c++-2023 ....
```

### 檢查所有 C 與 C++ 檔
`cert-c` 與 `misra-c-*` 編碼標準針對 C，因此預設只檢查 C 檔。

`autosar`、`cert-c++` 與 `misra-c++-*` 針對 C++，因此預設只檢查 C++ 檔。

若要檢查所有檔案，可在標準名稱後加上 `:all`。

範例：

```
# Misra C 檢查器只會對 C 檔執行，不會對 C++ 檔執行
cppcheck --premium=misra-c-2025 path
# Misra C 檢查器會對 C 與 C++ 檔執行
cppcheck --premium=misra-c-2025:all path
```

## 相容性報告
### 圖形介面
啟用某些編碼標準後執行分析，接著點選 File 選單的「Compliance report...」。

### 命令列
Cppcheck Premium 內含 `compliance-report` 工具。若不帶參數執行，可列出所有可用選項。

以下為產生 Misra C 2012 相容性報告的範例：

```
cppcheck --premium=misra-c-2012 --xml-version=3 src 2> results.xml
compliance-report --misra-c-2012 --project-name=Device --project-version=2.3 \
  --output-file=report.html results.xml
```

選項說明：
- `--misra-c-2012`：產生 misra-c-2012 相容性報告
- `--project-name`：專案名稱
- `--project-version`：專案版本
- `--output-file`：輸出的 html 檔名
- `results.xml`：Cppcheck 的 XML 輸出

## 指標（Metrics）
要產生 metrics，加入 `--premium=metrics`。metrics 會儲存在 XML v3 報告中。範例：

```
cppcheck --premium=metrics test.c --xml-version=3 2> res.xml
```

我們提供簡單的 Python 腳本將 metrics 轉成 CSV：

```
python3 HISReport.py -f res.xml -j path/to/cppcheck-id-mapping.json -o test.csv
```

`cppcheck-id-mapping.json` 位於 Cppcheck Premium 安裝資料夾，例如 `/opt/cppcheckpremium` 或 `C:\Program Files\Cppcheck Premium`。

目前沒有現成的 HTML/PDF 報告方案。你可輕鬆調整 `HISReport.py` 讓它輸出 HTML，並生成符合需求的報告。

## 授權
### 商業條款
Cppcheck Premium 授權資訊：https://www.cppcheck.com/plans-pricing

### 安裝 / 註冊
請參閱 Cppcheck Premium 網站：https://www.cppcheck.com

### 授權檔路徑
Premium 外掛會在預先定義的路徑中尋找授權檔。若要在命令列指定任意授權檔路徑，可使用 `--premium-license-file`。

範例：

```
cppcheck --premium-license-file=path/to/file.lic test.cpp
```

若明確指定路徑，premium 外掛不會再搜尋預設路徑。

## 疑難排解
### 步驟 1：檢查 premiumaddon 除錯輸出
若授權無法使用，可執行 `premiumaddon` 並加上 `--debug` 取得授權驗證細節。

Windows：

```
premiumaddon.exe --debug
```

Linux/Mac：

```
premiumaddon --debug
```

上述命令可在任意資料夾執行。

### 步驟 2：清理 Cppcheck 建置目錄
命令列：若使用 `--cppcheck-build-dir`，請移除指定資料夾內所有檔案後重新檢查。

Cppcheck GUI：GUI 預設會建立 cppcheck 建置目錄。清除所有結果並重新檢查。可點工具列的刷子圖示清除結果，或從 Edit 選單選擇「Clear results」。

### 步驟 3：移除 cppcheck-premium-loc 檔案
若專案資料夾中有 `cppcheck-premium-loc` 檔案，請移除。

若分析時仍產生此檔，請檢查你的腳本為何會產生此檔案。
