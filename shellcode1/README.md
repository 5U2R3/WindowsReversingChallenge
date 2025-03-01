# MalwareTech shellcode1 writeup

## 概要
本記事はMalwareTech氏によるマルウェア解析初心者向け演習問題のWriteupです。  
MalwareTech氏のWindowsReversingは、初心者に一般的なマルウェアのテクニックに慣れてもらうことを目的にしています。  
ファイルを解析し、答えとなるフラグを見つけましょう。  
演習問題となるファイルはMalwareTech氏のGithubにて公開されています。  

## 環境
OS:Parrot Security 6.3(lorikeet)  
Ghidra Version 11.3  
Java Version 21.0.6  
pyghidraを使用

## shellcode1-[★☆☆☆☆]
shellcode1の解析を行っていきます。  
shellcode1.zipを7zコマンドを用いて展開するとshellcode1.exe_が出てきます。  
拡張子が"exe_"のため、Windowsの実行ファイルと考えられますがまずはファイル形式を判別します。 

↓fileコマンドを用いてファイルの判別

ファイル判別の結果、shellcode1.exe_は32bitのWindows実行ファイルであることがわかります。  
表層解析にはファイル判別の他、文字列の抽出やインポート関数の調査がありますが今回はGhidraにファイルを読み込み後に確認していくことにします。  
Ghidraにshellcode1.exe_をインポートします。  
まずは文字列を抽出し確認します。  
Ghidra CodeBrowerから[Window > Defined Strings]をクリック
文字列を確認したところ、FLAGに直接繋がりそうな文字列は特に見当たらないです。  
続いてインポート関数を確認します。  
Symbol Treeから[imports]を展開します。  
インポートされている関数にKERNEL32.DLLからGetProcessHeap、HeapAllocが見受けられます。  
また、NTDLL.DLLからはmemcpy、memsetがインポートされていることからプログラム内でヒープ領域へ何らかのデータをコピーしているのではないかと予想ができます。  
予想を踏まえて早速デコンパイル結果を見ていきます。  

↓shellcode1.exe_のDecompile  

entry関数の17行目でGetProcessHeap()、18行目でHeapAlloc()が実行されていることがわかります。  
解析時にはWindowsAPIの定義を確認しながら進めていくことが重要です。  
