# CTFから学ぶShellcode実行の仕組み

## 概要
本記事はMalwareTech氏によるマルウェア解析初心者向け演習問題を解きながら、Shellcodeが実行される仕組みを解説していきます。  
MalwareTech氏のWindowsReversingは、初心者に一般的なマルウェアのテクニックの理解と解析に慣れてもらうことを目的にしています。  
演習問題となるファイルはMalwareTech氏のブログにて公開されています。  
https://malwaretech.com/

## 目的
CTF形式の問題を解きながら、Shellcodeが実行される仕組みを理解する。  

## 環境
OS:Windows11 24H2(OSビルド26100.6899)  
IDA Free 8.4  
Ghidra Version 11.4.2 ※solveスクリプト作成用  
Java Version 21.0.6  
pyghidraを使用  
> [!WARNING]
> マルウェア解析は専門的な技術を必要とする危険な作業です。  
> オフラインのVMや独立した検証環境等の適切な環境と知識を持って  
> マルウェア解析を実施することを推奨します。  

## 解析順序
マルウェアの機能と特徴を理解し、システムへの影響を評価するため、様々な解析手法が存在します。  
マルウェアの解析は次の順序でアプローチすることが重要であると私は考えます。  
1. 表層解析(解析難易度：易)  
   プログラムを実行せずに分析対象ファイルに関連付けられているメタデータを抽出し、マルウェアの情報を集める手法
2. コード解析・静的解析(解析難易度：難)  
   プログラムを実行せずに分析対象ファイルを逆アセンブルし、コードを調べて動作を理解する手法
3. 動的解析(解析難易度：中)  
   プログラムを実行し、動作を監視しながら挙動を理解する手法  

多くの参考書や資料では解析の難易度順に説明されており、  
コード解析・静的解析よりも先に動的解析が説明されますが、  
動的解析は実際の悪意のあるマルウェアにおいては解析環境の検知や破壊といった挙動を行う可能性もあり、  
解析の当たりを決めずに実行するだけではマルウェアの正しい挙動を把握できない可能性があります。  
そのため、動的解析はコード解析・静的解析を先に実施し、主要な挙動を理解して進めることが重要です。  
※主要な挙動を理解して実行する点はペネトレーションテストなどで使用されるPoCにも同様のことが言えます。

## shellcode1-[★☆☆☆☆]  
shellcode1はシェルコードベースのマルウェア解析の初心者向け入門書として位置付けられています。  
提供されたバイナリを解析し、フラグとなる文字列を探していきます。  
今回は表層解析と静的解析を用いてShellcode1にアプローチしていきます。  

### 表層解析

↓Detect It Easyの結果
![writeup-001](/shellcode1/Dit_Shellcode1.png)  

### 静的解析
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

## まとめ
