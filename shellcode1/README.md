# CTFから学ぶShellcode実行の仕組み

## 概要
本記事はMalwareTech氏によるマルウェア解析初心者向け演習問題を解きながら、Shellcodeが実行される仕組みを解説していきます。  
MalwareTech氏のWindowsReversingは、初心者に一般的なマルウェアのテクニックに慣れてもらうことを目的にしています。  
演習問題となるファイルはMalwareTech氏のブログにて公開されています。  
https://malwaretech.com/

## 目的
CTFを解きながら、Shellcodeが実行される仕組みを理解する。  

## 環境
OS:Windows11 24H2(OSビルド26100.6899)  
IDA Free 8.4  
Ghidra Version 11.4.2 ※solveスクリプト作成用  
Java Version 21.0.6  
pyghidraを使用  
!!!注意:解析を行う際はオフラインのVMなど隔離環境を用いてください。!!!

## shellcode1-[★☆☆☆☆]  
shellcode1はシェルコードベースのマルウェア解析の初心者向け入門書として位置付けられています。  
提供されたバイナリを解析し、フラグとなる文字列を探していきます。  
マルウェアの解析は、表層解析、動的解析、コード解析・静的解析、メモリ解析といった複数種類の解析手法があります。  
今回は表層解析と静的解析を用いてShellcode1にアプローチしていきます。  

■表層解析  

↓Detect It Easyの結果
![writeup-001](/shellcode1/Dit_Shellcode1.png)  

0x00402289でGetProcessHeap()、0x00402290でHeapAlloc()が呼び出されています。  
解析時にWindowsAPIの定義を確認しながら進めていくことでプログラムがどのような動作をしているかのヒントになります。  
[HeapAlloc関数](https://learn.microsoft.com/ja-jp/windows/win32/api/heapapi/nf-heapapi-heapalloc)

>DECLSPEC_ALLOCATOR LPVOID HeapAlloc(  
　[in] HANDLE hHeap,  
　[in] DWORD  dwFlags,  
　[in] SIZE_T dwBytes  
);

[VirtualAlloc関数](https://learn.microsoft.com/ja-jp/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc)  

>LPVOID VirtualAlloc(  
　[in, optional] LPVOID lpAddress,  
　[in]           SIZE_T dwSize,  
　[in]           DWORD  flAllocationType,  
　[in]           DWORD  flProtect  
);  

VirtualAlloc関数は呼び出し元プロセスの仮想アドレス空間内のページ領域の状態を予約、コミット、または変更する関数です。  

