# 
# Okoshi v1.0
#
# This is an ASR processing software written in python, This program used ESPnet and Julius to run ASR process.
#

from posixpath import abspath
import subprocess
import shutil
import soundfile
import os
import argparse
import spacy

from espnet_model_zoo.downloader import ModelDownloader
from espnet2.bin.asr_inference import Speech2Text


def main():
    # コマンドライン引数など
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to transcription")
    parser.add_argument("--espnet", help="use espnet for transcription",
                        action="store_true")
    parser.add_argument("--julius", help="use julius for transcription",
                        action="store_true")
    args = parser.parse_args()

    # espnetとjuliusの分岐
    if args.espnet:
        print("ESPNet2モードで動作しています。\n\n\
このモードではpythonのライブラリを用いて音声認識を行い、動作要件が厳し目ですが外部のバイナリをダウンロードせずpipでインストールする複数のpythonライブラリを使用して文字起こしをすることができます。\n\
雑音や効果音を文字と認識してしまうことがあります。\n\n\
Juliusモードも利用可能です。\n\
JuliusモードではJulius公式で提供されるdictation-kitとそれに同梱されるjuliusのバイナリを使用します。\n\
ESPNetモードよりもはっきり聞こえない音に弱い印象で、使用している辞書に登録されていない言葉が多いため認識できない言葉が多いです。\n\
場合によりdictation-kit同梱のjuliusが動作しない場合があります。\n")
        yorn = input("\n続行しますか?(y/n)")
        if yorn == "y" or yorn == "Y":
            with_espnet(args.file)
        else:
            return


    elif args.julius:
        print("Juliusモードで動作しています。\n\n\
このモードではJulius公式で提供されるdictation-kitとそれに同梱されるjuliusのバイナリを使用します。\n\
ESPNetモードよりもはっきり聞こえない音に弱い印象で、使用している辞書に登録されていない言葉が多いため認識できない言葉が多いです。\n\
場合によりdictation-kit同梱のjuliusが動作しない場合があります。\n\n\
ESPNet2モードも利用可能です。\n\
ESPNet2モードではpythonのライブラリを用いて音声認識を行い、動作要件が厳し目ですが外部のバイナリをダウンロードせずpipでインストールする複数のpythonライブラリを使用して文字起こしをすることができます。\n\
雑音や効果音を文字と認識してしまうことがあります。\n")
        yorn = input("\n続行しますか?(y/n)")
        if yorn == "y" or yorn == "Y":
            with_julius(args.file)
        else:
            return
    else:
        print("--espnetオプションか--juliusオプションを指定してください")
        return

def with_julius(filepath):
    if os.path.isdir("dictation-kit-4.5"):
        print("Juliusのdictation-kit(4.5)が存在します。\n\
ダウンロードをスキップします。")
        julius      = "./dictation-kit-4.5/bin/linux/julius"
        main        = "./dictation-kit-4.5/main.jconf"
        am_dnn      = "./dictation-kit-4.5/am-dnn.jconf" 
        julius_dnn  = "./dictation-kit-4.5/julius.dnnconf"
        
        path = os.path.abspath(filepath)
        root_ext = os.path.splitext(filepath)[1]
        wavf = mp4_to_wav(False, path, root_ext)
        input_audio_file  = wavf
        
        args = [julius, "-C", main, "-C", am_dnn, "-dnnconf", julius_dnn, "-input", "rawfile", "-cutsilence", "-realtime"]
        print("\n\n🖋️ juliusのバイナリを用いて文字起こしを行っています。\nこの段階は長い時間を必要とする場合があります...\n")

        os.makedirs(os.path.dirname(path) + '/output/', exist_ok=True)
        txt_file = os.path.dirname(path) + '/output/' + os.path.basename(path.replace(os.path.splitext(os.path.basename(path))[1], '.txt'))
        f = open(txt_file, 'a')
        output = subprocess.run(args, input=input_audio_file, capture_output=True, text=True).stdout.splitlines(True)
        for sentence in output:
            if "sentence1:" in sentence:
                f.write(sentence[12:].replace(" ", ""))
        print("文字起こしが完了しました")
        f.close()
        os.remove(wavf)
        segment_sentence(txt_file, False)
        print('✅ テキストの文字起こしとテキストファイルへの出力が完了しました。\nファイルの保存場所は以下の通りです:')
        print(txt_file)
        
    else:
        print("Juliusのdictation-kit(4.5)を見つかりませんでした。\n\
このスクリプトと同じフォルダに配置されている必要があります。\n")
        yorn = input("すぐにダウンロードしますか?[400MBのZipファイルをDL/ストレージは1.5GB以上の空き容量必須](Y/n)")
        if yorn == "y" or yorn == "Y":
            download_julius()
        else:
            return

#Juliusのダウンロード
def download_julius():
    print("実装されていません")
    return

# espnetを使う場合
def with_espnet(filepath):
    path = os.path.abspath(filepath)
    root_ext = os.path.splitext(filepath)[1]
    wavf = mp4_to_wav(True, path, root_ext)
    # 学習済みをダウンロードし、音声認識モデルを作成
    print("変換用のモデルをダウンロードしています...\nすでにキャッシュされている場合スキップされます。\n")
    d = ModelDownloader()
    speech2text = Speech2Text(
            **d.download_and_unpack("kan-bayashi/csj_asr_train_asr_transformer_raw_char_sp_valid.acc.ave"),
            device="cuda"  # CPU で認識を行う場合は省略
        )

    files = os.listdir(os.path.dirname(wavf)+ "/temp/")
    files = sorted(files)
    for count, sound in enumerate(files, 1):
        speech, _ = soundfile.read(os.path.dirname(wavf) + "/temp/" + sound)
        nbests = speech2text(speech)
        out_text, *_ = nbests[0]
        os.makedirs(os.path.dirname(path) + '/output/', exist_ok=True)
        txt_file = os.path.dirname(path) + '/output/' + os.path.basename(path.replace(os.path.splitext(os.path.basename(path))[1], '.txt'))
        f = open(txt_file, 'a')
        print(str(count) + "回目の文字起こしが完了しました。")
        if count == 14:
            print()
        f.write(out_text)
        f.close()
    
    os.remove(wavf)
    shutil.rmtree(os.path.dirname(wavf) + "/temp/")
    segment_sentence(txt_file, True)
    print('✅ テキストの文字起こしとテキストファイルへの出力が完了しました。\nファイルの保存場所は以下の通りです:')
    print(txt_file)

# 音声ファイルへの変換と10秒単位の分割
def mp4_to_wav(split, otherextf, rootext):
    wavf = otherextf.replace(rootext, '.wav.tmp.okoshi')
    print("一時的にファイルをwav形式の16000KHzに変換しています...\n生成されたwavファイルを操作しないでください。\n")
    outstr_converting = subprocess.run(['ffmpeg', '-i', otherextf, '-ar', '16000', '-ac', '1', '-y', '-f', 'wav' ,wavf], 
                    encoding='utf-8', stdout=subprocess.PIPE)
    if split:
        print("一時的な、変換に使用するフォルダを作っています...\n生成されたフォルダを操作しないでください。\n")
        os.makedirs(os.path.dirname(wavf) + '/temp/', exist_ok=True)
        print("変換の速度を上げるため十秒単位で元ファイルの音声を分割しています...\n")
        outstr_cutting = subprocess.run(['ffmpeg', '-i', wavf, '-map', '0', '-c', 'copy', '-f', 'segment', '-segment_time', '10', '-reset_timestamps', '1', os.path.dirname(wavf)+ "/temp/" + os.path.basename(wavf) + "_%03d.wav" ],
                        encoding='utf-8', stdout=subprocess.PIPE)
    return wavf

#文章の整形(GiNZA使用)
def segment_sentence(txt_file, nline):
    print("GiNZAで文章を整形しています...")
    f = open(txt_file, 'r')
    text = f.read()
    nlp = spacy.load('ja_ginza_electra')
    doc = nlp(text)
    sentences = []
    for sent in doc.sents:
        # 文単位で配列の1要素となる
        sentences.append(sent)
    f.close()
    # 全て文単位にしたあと配列に全て保持してあるので、素のデータの書き込まれたテキストファイルを消す
    os.remove(txt_file)
    # 再度文単位に改行で区切り文章を再度生成した空のテキストファイルに書き出す
    for sentence in sentences:
        f = open(txt_file, 'a')
        if nline:
            f.write(str(sentence) + "\n")
        else:
            f.write(str(sentence))
        f.close()

if __name__ == "__main__":
    main()
