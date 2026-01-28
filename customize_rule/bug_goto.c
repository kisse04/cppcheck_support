/*
 * bug_goto.c
 *
 * 測試用途：刻意寫多種 "goto" 讓 Cppcheck 自訂規則可以抓到。
 * 每個例子都有中文說明，讓不懂程式的人也能理解為什麼 goto 危險。
 */

#include <stdio.h>

/* ---------------------------------------------------------
 * 1. 最基本的 goto：跳到下面的特定標籤
 * --------------------------------------------------------- */
void test_basic_goto()
{
    printf("[1] Before goto\n");
    goto after;   // <-- 測試用的 goto

after:
    printf("[1] After goto\n");
}

/* ---------------------------------------------------------
 * 2. 前向跳轉（forward goto）
 *   工程師可能會寫到這行，然後跳到更下面的標籤，跳過一堆邏輯
 * --------------------------------------------------------- */
void test_forward_goto(int x)
{
    if (x < 0)
        goto error_handler; // <-- 測試 goto（前向跳轉）

    printf("[2] 正常流程：x >= 0\n");
    return;

error_handler:
    printf("[2] 錯誤流程：x < 0\n");
}

/* ---------------------------------------------------------
 * 3. 後向跳轉（backward goto）
 *    這等同於手寫死迴圈（某些版本的 goto 會造成不可控流程）
 * --------------------------------------------------------- */
void test_backward_goto()
{
    int counter = 0;

start:                          // 標籤（goto 跳回這裡）
    printf("[3] counter = %d\n", counter);
    counter++;

    if (counter < 3)
        goto start;            // <-- 測試 goto（後向跳轉）

    printf("[3] Done\n");
}

/* ---------------------------------------------------------
 * 4. goto 跳出多層流程
 *    有些人用 goto 來強制跳出二層迴圈或 if，非常不容易維護
 * --------------------------------------------------------- */
void test_goto_out_of_nested()
{
    int i, j;

    for (i = 0; i < 3; i++)
    {
        for (j = 0; j < 3; j++)
        {
            printf("[4] i=%d, j=%d\n", i, j);
            if (i == 1 && j == 1)
                goto exit_all;   // <-- 測試 goto（跳離多層）
        }
    }

exit_all:
    printf("[4] goto 離開多層迴圈\n");
}

/* ---------------------------------------------------------
 * 5. 多個 goto 混在一起
 * --------------------------------------------------------- */
void test_multiple_goto(int x)
{
    if (x == 0)
        goto zero_case;       // <-- goto

    if (x == 1)
        goto one_case;        // <-- goto

    goto end;                 // <-- goto（預設分支）

zero_case:
    printf("[5] x = 0\n");
    goto end;                 // <-- goto

one_case:
    printf("[5] x = 1\n");

end:
    printf("[5] End\n");
}

/* ---------------------------------------------------------
 * 主程式：執行所有測試
 * --------------------------------------------------------- */
int main()
{
    test_basic_goto();
    test_forward_goto(-1);
    test_backward_goto();
    test_goto_out_of_nested();
    test_multiple_goto(1);

    return 0;
}
