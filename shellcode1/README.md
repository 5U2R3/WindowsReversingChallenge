# MalwareTech shellcode1 writeup

## 概要
本記事はMalwareTech氏によるマルウェア解析初心者向け演習問題のWriteupです。  
MalwareTech氏のWindowsReversingは、初心者に一般的なマルウェアのテクニックに慣れてもらうことを目的にしています。  
ファイルを解析し、答えとなるフラグを見つけます。  
演習問題となるファイルはMalwareTech氏のGithubにて公開されています。  

## 環境
OS:Parrot Security 6.3(lorikeet)  
IDA 7.6  
Ghidra Version 11.3  
Java Version 21.0.6  
pyghidraを使用

## shellcode1-[★☆☆☆☆]
shellcode1の解析を行っていきます。  
shellcode1.zipを7zコマンドを用いて展開するとshellcode1.exe_が出てきます。  
拡張子が"exe_"のため、Windowsの実行ファイルと考えられますがまずはファイル形式を判別します。 

↓fileコマンドを用いてファイルの判別
![writeup-001](/shellcode1/shellcode-writeup-001.PNG)  
ファイル判別の結果、shellcode1.exe_は32bitのWindows実行ファイルであることがわかります。  
表層解析にはファイル判別の他、文字列の抽出やインポート関数の調査がありますが今回はIDAにファイルを読み込みんで確認していくことにします。  
IDAにshellcode1.exe_をインポートします。  
まずは文字列を抽出し確認します。  
IDAから[View > Open subviews > strings]をクリック
文字列を確認したところ、FLAGに直接繋がりそうな文字列は特に見当たらないです。  
続いてインポート関数を確認します。  
IDAから[View > Open subviews > imports]をクリック  
インポートされている関数にKERNEL32.DLLからGetProcessHeap、HeapAlloc、VirtualAllocが見受けられます。  
NTDLL.DLLからはmemcpy、memsetがインポートされていることからプログラム内で確保したヒープ領域へデータをコピーしているのではないかと予想ができます。  
予想を踏まえて早速IDA Viewを見ていきます。  

↓shellcode1.exe_をアセンブルした結果  

0x00402289でGetProcessHeap()、0x00402290でHeapAlloc()が呼び出されています。  
解析時にWindowsAPIの定義を確認しながら進めていくことでプログラムがどのような動作をしているかのヒントになります。  
[HeapAlloc関数](https://learn.microsoft.com/ja-jp/windows/win32/api/heapapi/nf-heapapi-heapalloc)

>DECLSPEC_ALLOCATOR LPVOID HeapAlloc(  
　[in] HANDLE hHeap,  
　[in] DWORD  dwFlags,  
　[in] SIZE_T dwBytes  
);

HeapAlloc関数はヒープからメモリブロックを割り当てる関数です。
関数が成功した場合の戻り値は割り当てられたメモリブロックへのポインタ  
第1引数のhHeapはHeapCreate関数またはGetProcessHeap関数によって返されたメモリの割り当て元となるヒープへのハンドル、第3引数のdwBytesは割り当てるバイト数を指定するようです。  
HeapAlloc関数の定義を踏まえた上で改めてIDAを見てみるとHeapAllocを呼び出す前にpushされているeaxはGetProcessHeapの戻り値となっていることがわかります。  
dwBytesに位置する数値は10hがpushされています。  
結果としてHeapAlloc関数によって16バイトのヒープメモリが割り当てられたということになります。  
HeapAlloc関数を実行後、戻り値となる割り当てられた16バイトのヒープメモリブロックへのポインタがeaxに格納されます。  
0x00402296でeax(HeapAlloc関数の戻り値)は[ebp+var_4]に格納されます。  
その後、0x0040229Cで割り当てられたヒープメモリブロックにoffset unk_404040が格納されます。  
unk_404040は現状では意味が分からない文字列が並んでいます。  
0x004022A7ではunk_404040を引数としてstrlenが呼び出されています。  
strlen関数は戻り値として引数に指定された文字列の長さを返します。  
strlenの戻り値は0x004022B2で[ecx+4]に格納されます。ecxは0x004022AFで[ebp+var_4]が格納されており結果としてstrlenの戻り値は[ebp+var_4+4]、ヒープメモリブロックのoffset unk_404040の後に格納されるということがわかります。  
つづいて0x004022C0にてVirtualAlloc関数が呼び出されます。
[VirtualAlloc関数](https://learn.microsoft.com/ja-jp/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc)  

>LPVOID VirtualAlloc(  
　[in, optional] LPVOID lpAddress,  
　[in]           SIZE_T dwSize,  
　[in]           DWORD  flAllocationType,  
　[in]           DWORD  flProtect  
);  

VirtualAlloc関数は呼び出し元プロセスの仮想アドレス空間内のページ領域の状態を予約、コミット、または変更する関数です。  

