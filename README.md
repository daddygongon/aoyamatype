# AoyamaType

**aoyamatype** は、タイピング練習用の Python パッケージです。コマンドラインからタイピング練習ができ、スキル向上をサポートします。

---
### インストール方法
pythonがインストールされpipが使用できることが前提です。
以下のコマンドを実行してください  
`pip install git+https://github.com/37021463/aoyamatype.git`

パッケージのインストールが完了できればこちらの[URL](https://kwanseio365-my.sharepoint.com/:f:/g/personal/ijv85378_nuc_kwansei_ac_jp/ElNx956B6chEppmidaLVxm4BUMw0mT9WP4NU0cGyJH1hDA?e=uCca4V  
)からdata.zipをダウンロードしてください。    

次に`aoyamatype -d [PATH]` (PATHはダウンロードしたdata.zipのもの)とし、コマンドを入力してください。  
aoyamatype と打つことでコマンド一覧が表示されます。

---
### コマンド一覧
`aoyamatype`  
`aoyamatype -r`  
`aoyamatype -c`  
`aoyamatype -d [PATH]`  
`aoyamatype <file_number(1~97)>`  

---

### エラーと対策
+ pip install git+https://github.com/37021463/aoyamatype.git
が実行できずgitがない場合はこちらの[gitのホームページ](https://git-scm.com/)から自分のPCにあったgitをダウンロードしてください。  

+ インストール時に以下のような警告文が表示される場合、aoyamatypeと打ってもコマンドが見つからない場合  
[WARNING: The script aoyamatype.exe is installed in'C:\Users\...\Python311\Scripts' which is not on PATH.]  
PythonのScriptがインストールされるディレクトリが環境変数PATHに含まれていない可能性があります。  
環境変数PATHに警告文で表示されたPATHを追加してください。    
詳しくはこちらの[サイト](https://www.javadrive.jp/python/install/index3.html  
)を参考にしてみてください。  

+ aoyamatype -d [PATH]でzipフォルダを正常に展開できない場合は以下の点をもう一度確認してください。
1. フォルダの名称がdata.zipになっているか
2. ダウンロードしたdataフォルダがzip形式になっているか
3. PATHが本当にdata.zipのものになっているか(フォルダを右クリックでパスのコピーがあるはずです)