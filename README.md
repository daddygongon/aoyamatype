# AoyamaType

**aoyamatype** は、タイピング練習用の Python パッケージです。コマンドラインからタイピング練習ができ、スキル向上をサポートします。

---
### インストール方法
以下のコマンドを実行してください  
pip install git+https://github.com/37021463/aoyamatype.git

以下のURLからdata.zipをダウンロードしてください。  
https://kwanseio365-my.sharepoint.com/:f:/g/personal/ijv85378_nuc_kwansei_ac_jp/ElNx956B6chEppmidaLVxm4BUMw0mT9WP4NU0cGyJH1hDA?e=uCca4V  
次にaoyamatype -d [PATH] PATHはダウンロードしたdata.zipのものとし、コマンドを入力してください。  
aoyamatype と打つことでコマンド一覧が表示されます。

---

### エラーと対策
+ pip install git+https://github.com/37021463/aoyamatype.git
が実行できずgitがない場合は以下のURLから自分のPCにあったgitをダウンロードしてください。  
https://git-scm.com/

+ インストール時に以下のような警告文が表示される場合  
[WARNING: The script aoyamatype.exe is installed in 'C:\Users\...\Python311\Scripts' which is not on PATH.]  
PythonのScriptがインストールされるディレクトリが環境変数PATHに含まれていません。  
環境変数PATHに警告文で表示されたPATHを追加してください。  
Unix系OSでは、~/.local/binをPATHに追加します。

詳しくは以下のサイトを参考にしてください。  
https://www.javadrive.jp/python/install/index3.html  

+ aoyamatype -d [PATH]でzipフォルダを正常に展開できない場合は以下の点をもう一度確認してください。
1. ダウンロードしたdataフォルダがzip形式になっているか
2. PATHが本当にdata.zipのものになっているか
