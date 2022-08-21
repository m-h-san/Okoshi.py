# 🖊️ Okoshi.py
これは音声/動画ファイルから、***外部のバイナリに投げたり、ライブラリの力に全力で頼り***文字起こしをして、最終的にテキストファイルに整形した文章を吐くスクリプトです。  
速度的にグラフィックボードの載ったコンピュータで動作させることをおすすめします。  
このスクリプト内では外部のライブラリ、バイナリに調整したファイルを投げているだけで、音声認識の処理はしていません。  
ライブラリなどを開発してくださっいるデベロッパの方、ありがとうございます。（準備と後片付け以外人任せみたいな感じです）

## 💬 開発途中です
このスクリプトはまだ作成途中であるため指定されたファイルが実在するかの確認などが行われません。  
**このスクリプトを使用した結果生じたいかなる損害に対しても作成者は責任を負うことができません。**
  
## ✨ 利用可能な文字起こし
 - [ESPNet2](https://github.com/espnet/espnet)及び[ESPNet_Model_Zoo](https://github.com/espnet/espnet_model_zoo)を使用した文字起こし  
 Pythonのライブラリをpipでインストールし、このスクリプトを使用します。
 環境構築が大変です。
   
 - [Julius](https://github.com/julius-speech/julius)を使用した文字起こし  
 **かんたんに直せるかもしれないのですがやる気がいまないのでLinuxのみでの動作**  
 Julius公式で配布されている[dictation-kit](https://github.com/julius-speech/dictation-kit)同梱のコンパイル済みバイナリを使用できます。
 dictation-kitのみをそのまま使った状態での精度はESPNetより悪い印象です。

# 👀 使用方法

## ⚡ このリポジトリをクローン
```git clone git@github.com:m-h-san/Okoshi.py.git```  
  
## 🚄 ESPNetを使用する場合
ESPNet関係はnumpyなどを使うためpythonのバージョンは現在3.9.0でしか動作を確認していません(3.9.0よりいくつか上までは動きそうです)。  
3.10以降は2022年8月現在numpyが対応していないようなので[pyenv](https://github.com/pyenv/pyenv)を導入して、  
```pyenv install 3.9.0```  
したあと  
```pyenv local 3.9.0```  
しておくなどして、python3.9をインストールしておいてください。
### 🛰️ 依存ライブラリをクローン
ESPNetを使用する場合に依存するライブラリをインストールしておきます。  
```python3 -m pip install torch```  
```python3 -m pip install espnet_model_zoo```  
  
文を整形するために[GiNZA](https://megagonlabs.github.io/ginza/)を使用しているので、依存関係にあるそれをインストールしておきます。  
```python3 -m pip install -U ginza ja_ginza_electra```

### 🎬 ffmpegのインストール
文字起こしの効率化のためファイルを10分割します。  
また、wav形式かつ16000KHzのファイル以外が渡されたときに変換して文字起こしをします。  
そのために、ffmpegを導入して、コマンドラインで実行できるようパスを通す必要があります。
Arch系OSなら  
```pacman -S ffmpeg```  
で導入できるはずです。
### 🌟 このスクリプトを実行
```python3 ./okoshi.py --espnet /path/to/your/file```
 - `./okoshi.py`の部分はあなたのコンピュータ上にあるokoshi.pyのパスを指定してください。  
 - `/path/to/your/file`の部分は文字起こししたい動画、音声ファイルを指定してください。ファイルタイプはffmpegがwavに変換できるものであれば何でもOKです。

## 🚅 Juliusを使用する場合
pythonのバージョンはあまり関係ないと思いますが3.9.0でしかテストしていません。

### 🛰️ 依存ライブラリをクローン
文を整形するために[GiNZA](https://megagonlabs.github.io/ginza/)を使用しているので、依存関係にあるそれをインストールしておきます。  
```python3 -m pip install -U ginza ja_ginza_electra```

### 🎬 ffmpegのインストール
ffmpegを導入して、コマンドラインで実行できるようパスを通してください。
Arch系OSなら  
```pacman -S ffmpeg```  
で導入できるはずです。

### 📔 dictation-kitのver4.5をダウンロード
[こちら(直リンク)](https://osdn.net/frs/redir.php?m=gigenet&f=julius%2F71011%2Fdictation-kit-4.5.zip)からダウンロードしてOkoshi.pyと同じフォルダにZipから解凍したものを配置してください。

### 🌟 このスクリプトを実行
```python3 ./okoshi.py --julius /path/to/your/file```
 - `./okoshi.py`の部分はあなたのコンピュータ上にあるokoshi.pyのパスを指定してください。  
 - `/path/to/your/file`の部分は文字起こししたい動画、音声ファイルを指定してください。ファイルタイプはffmpegがwavに変換できるものであれば何でもOKです。
