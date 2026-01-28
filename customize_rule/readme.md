使用說明
1) 在本資料夾執行下列指令，載入自訂規則檔並掃描範例檔：
   cppcheck --rule-file=no_goto.rule bug_goto.c

2) 規則來源：
   - no_goto.rule 會用 regex 比對 "goto label;" 形式的語句。
   - 觸發後會回報 id = style.no_goto，severity = error。

3) 範例檔：
   - bug_goto.c 內刻意放入多種 goto（基本、前向、後向、跳出多層、分支混用）。

4) 預期結果：
   - 每一個 goto 都會被偵測並回報錯誤訊息：
     "The use of goto is prohibited: Please use structured processes instead."
