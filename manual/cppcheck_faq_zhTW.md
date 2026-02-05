# Cppcheck FAQ（路徑／授權／遠端映射使用）

> 目的：整理常見問題與排查方向，避免因為路徑、include 設定或授權識別導致掃描中斷／誤報。

## 0. 重要前提：不要使用中文路徑
- **不要把工程路徑、cppcheck 路徑、license 路徑放在含中文／特殊字元的目錄**。
- 建議統一使用純英文／數字／底線路徑，例如：
  - `C:\work\project_a\`
  - `I:\cppcheck_test\`
  - `Z:\tools\cppcheck\`

原因：部分工具鏈／外掛在處理非 ASCII 路徑時，可能出現解析失敗、找不到檔案、或異常中斷（常見表現包含 syntax error、include not found、license file open failed 等）。

---

## 1) 為什麼會出現「syntax error」？看起來像在檢查 STM 的標頭檔導致報錯並停止？
常見原因是：Cppcheck 在分析過程中遇到**無法解析的編譯環境**（例如 MCU/STM 相關標頭檔、編譯器擴充、巨集非常多），導致解析失敗。

建議：
1. **確認掃描對象**：只掃描你的原始碼目錄（`.c/.cpp`），避免把第三方／晶片 SDK 的標頭檔目錄當成掃描根目錄。
2. **補齊設定**（見第 2 節）：include 路徑（`-I`）、巨集定義（`-D`）、平台／編譯器相關設定。
3. 若是特定 header 觸發：
   - 優先把該 header 所在目錄當成 `-I`，而不是讓它出現在 `path`（掃描根目錄）裡。
   - 必要時對難解析的檔案做 **suppress／忽略**（視團隊規範）。

---

## 2) Path 是要掃碼的路徑；Include path 是標頭檔（.h）的位置
- **Path（掃描路徑）**：你希望 Cppcheck 直接檢查的原始碼位置（通常是工程的 `src/`，或目前目錄下的 `.c/.cpp`）。
- **Include path（`-I`）**：讓 Cppcheck 能找到 `#include "xxx.h"` 或 `<xxx.h>` 的目錄。

若未加入 include path（`-I`），Cppcheck 通常會提示：
- `missingIncludeSystem` / `missingInclude`（找不到標頭檔）

這類多半是 *information* 等級，但可能造成：
- 型別／巨集不完整 → 誤報增加
- 部分規則無法完整展開 → 掃描品質下降

**建議做法**：
- 把工程實際編譯會用到的 include 目錄都加上（與編譯器／IDE 設定一致）。
- 若需要額外 include 路徑，可在 Cppcheck 外掛／命令列參數中追加更多 `-I` 目錄（例如 `-I<cppcheck_folder>` 或工程 include 目錄）。
- 若缺少巨集定義，加入 `-D`（例如 `-D__cppcheck__`、晶片／平台相關巨集、`-DDEBUG` 等）。
- 更完整的參數與設定請參考 **Cppcheck manual**。

---

## 3) Cppcheck Premium 授權（2025 起）
- **Cppcheck Premium 自 2025 起不再提供個人／單獨授權**。
- 目前僅提供：
  - **Project**
  - **Enterprise**

（實際購買／授權策略以官方與代理商說明為準。）

---

## 4) 遠端伺服器上的 Cppcheck：用 Windows「映射網路磁碟機」可行嗎？
目前測試結論：**可行**。
- 可將遠端伺服器上的 Cppcheck 映射成本機磁碟使用。
- 本機可正常開啟 Cppcheck GUI 進行工程掃描。
- 也可在 VS Code 中設定並呼叫 Cppcheck 外掛，整體流程可行。

---

## 5) GUI 掃描時出現："Invalid license: Failed to open license file"，但仍有結果輸出
現象：
- 掃描能跑完並產生結果。
- 但出現 `Invalid license: Failed to open license file`。

風險：
- **無法確認 Premium 規則是否全部啟用**。
- 該錯誤可能導致 Premium 規則未載入或部分規則未執行，進而影響掃描完整性。

建議：
1. **與 Cppcheck 代理商確認**：在「網路映射磁碟」情境下，此 license 錯誤是否會影響 Premium 規則執行。
2. **手動指定授權檔位置**（見第 7 節），並確認錯誤是否消失。

---

## 6) VS Code 外掛也提示 Invalid license；且出現疑似與工程無關的誤報
現象：
- 外掛指向遠端映射路徑後可用，但同樣提示 `Invalid license`。
- 掃描過程出現較多疑似與工程無關的誤報。

可能原因：
- 授權未被正確識別（Premium 規則未載入／行為異常）。
- 工程設定不完整（include 路徑、巨集定義、標準／平台設定缺失）導致解析偏差。

建議：
1. 先釐清／解決 license 錯誤對掃描結果的影響（建議與代理商確認）。
2. 補齊外掛設定：
   - include paths（與編譯設定一致）
   - macros（`-D...`）
   - 必要時加入 suppress 規則

---

## 7) 手動指定 Premium 授權檔位置（GUI／外掛皆建議設定）
Cppcheck 使用說明提到可以手動指定授權檔位置。建議在 **命令列、GUI、VS Code 外掛** 都統一指定到遠端授權檔（或映射後的磁碟機路徑）。

### 命令列參數
- `--premium-license-file=<path-to-lic>`

範例（請使用英文路徑／映射磁碟）：
- `--premium-license-file=Z:\licenses\cppcheck-premium.lic`

### VS Code（cppcheck-official 外掛）
在外掛設定中：
- **Arguments / Additional command line arguments** 加上：
  - `--premium-license-file=Z:\licenses\cppcheck-premium.lic`

> 重點：license 檔案路徑也盡量不要放中文路徑；並確認 VS Code／外掛執行帳號對該路徑具有讀取權限。

---

## 8) 快速排查清單
1. 路徑是否全英文（工程／工具／license）？
2. 掃描 path 是否只指向原始碼，而不是把 SDK/include 目錄當成掃描根？
3. `-I` 是否補齊（與編譯一致）？
4. `-D` 巨集是否補齊（晶片型號／平台巨集／條件編譯）？
5. `Invalid license` 是否已透過 `--premium-license-file` 消除？
6. 若仍有誤報：匯出一條誤報對應檔案／行號，確認是否因缺 include／巨集導致解析錯誤。
