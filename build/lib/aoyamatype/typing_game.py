import sys
import time
import os
import threading
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import zipfile
from pathlib import Path
import optparse

def load_lines_from_file(file_path):
    "読み込んだファイルを一行づつ返す"
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    return lines

def get_user_input():
    try:
        return input().strip()
    except EOFError:
        return ''

def get_aoyamatype_directory():
    """ホームディレクトリに .aoyamatype フォルダを作成し、そのパスを返す"""
    home_directory = Path(os.environ.get('HOME') or os.environ.get('USERPROFILE'))
    aoyamatype_directory = home_directory / '.aoyamatype'
    
    if not aoyamatype_directory.exists():
        aoyamatype_directory.mkdir()
    
    return aoyamatype_directory

def get_text_data_directory():
    """ホームディレクトリの .aoyamatype フォルダに text_data フォルダを作成し、そのパスを返す"""
    aoyamatype_directory = get_aoyamatype_directory()
    text_data_directory = aoyamatype_directory / 'text_data'
    
    if not text_data_directory.exists():
        text_data_directory.mkdir()
    
    return text_data_directory

def get_data_file_path(file_name):
    """text_data フォルダ内のファイルパスを返す"""
    text_data_directory = get_text_data_directory()
    data_file_path = text_data_directory / file_name
    return data_file_path

def counter(word1, word2):
    "入力単語を空白区切りでカウント、テキストと比べる"
    ws1 = word1.split()
    ws2 = word2.split()
    count = 0
    i, j = 0, 0
    while i < len(ws1) and j < len(ws2):
        if ws1[i] == ws2[j]:
            count += 1
        i += 1
        j += 1
    return count

def record_session_data(file_name, total_words, total_time):
    """トレーニングデータをホームディレクトリ直下の .aoyamatype/training_data.txt に記録"""
    aoyamatype_directory = get_aoyamatype_directory()
    training_data_file = aoyamatype_directory / 'training_data.txt'
    
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S +0900")
    
    with open(training_data_file, 'a', encoding='utf-8') as file:
        file.write(f"{date_str},{file_name},{total_words},{total_time}\n")

def print_log():
    "トレーニング履歴とスキルチェック履歴を表示、グラフ化"
    aoyamatype_directory = get_aoyamatype_directory()
    training_log_file = aoyamatype_directory / 'training_data.txt'
    speed_data_file = aoyamatype_directory / 'speed_data.txt'

    # トレーニング履歴
    print("\nトレーニング履歴:")
    if training_log_file.is_file():
        logs = {}
        total_time_spent = 0
        training_dates = []
        training_scores = []
        
        with open(training_log_file, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) < 4:
                    continue
                date_str, file_name, total_words, _ = parts
                date_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S +0900")
                total_words = int(total_words)
                
                # 過去1週間のデータのみ保持
                if date_time >= datetime.now() - timedelta(days=7):
                    training_dates.append(date_time)
                    training_scores.append(total_words)

                if file_name not in logs:
                    logs[file_name] = {'last_date': date_str, 'total_words': total_words, 'count': 1}
                else:
                    logs[file_name]['last_date'] = date_str
                    logs[file_name]['total_words'] = total_words
                    logs[file_name]['count'] += 1

                total_time_spent += 20  # Each session is 20 seconds

        print(f"{'step':<10} | {'types':<5} | {'score':<11} | {'last_date':<20}")
        print('-' * 50)
        
        for file_name, data in sorted(logs.items()):
            step_number = file_name.split('-')[1].split('.')[0]
            print(f"STEP-{step_number:<5} | {data['count']:<5} | {data['total_words']:<11} | {data['last_date']:<20}")

        total_minutes, total_seconds = divmod(total_time_spent, 60)
        total_hours, total_minutes = divmod(total_minutes, 60)
        print(f"\nTotal time spent typing: {total_hours}時間 {total_minutes}分")
    else:
        print("No training data found.")

    # スキルチェック履歴
    print("\nスキルチェック履歴:")
    skill_dates = []
    skill_times = []
    
    if speed_data_file.is_file():
        with open(speed_data_file, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) < 4:
                    continue
                date_str, _, total_time, _ = parts
                date_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S +0900")
                skill_dates.append(date_time)
                skill_times.append(float(total_time))

        print(f"{'Date':<20} | {'Time (seconds)':<15}")
        print('-' * 40)
        for date, time_taken in zip(skill_dates, skill_times):
            print(f"{date.strftime('%Y-%m-%d %H:%M:%S')} | {time_taken:.2f}")
    else:
        print("No skill check data found.")
    
    # グラフを並べて表示
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # トレーニング履歴のグラフ（過去1週間分）
    if training_dates and training_scores:
        ax1.plot(training_dates, training_scores, marker='o', color='g')
        ax1.set_title("Training Scores Over Last 7 Days")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Score")
        ax1.grid(True)
        ax1.tick_params(axis='x', rotation=45)

    # スキルチェック履歴のグラフ
    if skill_dates and skill_times:
        ax2.plot(skill_dates, skill_times, marker='o', color='b')
        ax2.set_title("Skill Check Times Over Time")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Time Taken (seconds)")
        ax2.grid(True)
        ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
def record_skill_check_data(total_words, total_time):
    """スキルチェックのデータを .aoyamatype/speed_data.txt に記録（文字数で保存）"""
    aoyamatype_directory = get_aoyamatype_directory()
    speed_data_file = aoyamatype_directory / 'speed_data.txt'
    
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S +0900")
    
    # 打ち込んだ文字数（合計文字数）を計算
    total_characters = sum(len(word) for word in total_words)

    with open(speed_data_file, 'a', encoding='utf-8') as file:
        file.write(f"{date_str},{len(total_words)},{total_time},{total_characters}\n")

def print_keyboard_layout():
    print(" q \ w \ e \ r t \ y u \ i \ o \ p")
    print("  a \ s \ d \ f g \ h j \ k \ l \ ; enter")
    print("sh z \ x \ c \ v b \ n m \ , \ . \  shift")
    
def skill_check(word_list_path):
    # word.list ファイルから単語を読み込む
    words = load_lines_from_file(word_list_path)

    # ランダムに20単語を選択
    selected_words = random.sample(words, 20)

    print("スキルチェックを開始します。20個の単語をタイプしてください。")
    input("Enterキーを押して開始...")

    start_time = time.time()

    # タイピングゲームの開始
    for i, word in enumerate(selected_words, 1):
        while True:
            print_keyboard_layout()
            print(f"{i}. {word}")
            user_input = get_user_input()

            if user_input == word:
                break
            else:
                print("間違っています。もう一度入力してください。")

    end_time = time.time()
    total_time = end_time - start_time

    # スキルチェック結果を記録
    record_skill_check_data(selected_words, total_time)

    minutes, seconds = divmod(total_time, 60)
    print(f"スキルチェック完了！かかった時間: {int(minutes)}分 {int(seconds)}秒")
def play_typing_game(lines, file_name):
    total_words = 0
    index = 0
    total_time = 60  # 制限時間（秒）
    start_time = time.time()

    print("タイピングゲームへようこそ！")
    print_keyboard_layout()
    input("Enterキーを押して開始...")

    while time.time() - start_time < total_time:
        line = lines[index % len(lines)]
        print(f"{line}")

        user_input = None
        input_thread = threading.Thread(target=lambda: globals().update({'user_input': get_user_input()}))
        input_thread.start()
        input_thread.join(timeout=total_time - (time.time() - start_time))

        if input_thread.is_alive():
            print("時間切れ！")
            break

        user_input = globals().get('user_input', '')

        words_count = counter(line, user_input)  # 新しいカウンター関数を使用
        total_words += words_count

        print(f"{total_words}")  # スコアを表示

        index += 1  # タイプミスがあっても次の行に進む

    print(f"時間切れ！{total_time}秒で合計{total_words}個の単語を正しくタイプしました。")

    # セッションのデータを記録
    record_session_data(file_name, total_words, total_time)

def extract_zip_to_text_data(zip_path):
    """指定された zip ファイルを text_data フォルダに展開"""
    text_data_directory = get_text_data_directory()
    
    if not os.path.exists(zip_path):
        print(f"Error: '{zip_path}' が見つかりません。")
        sys.exit(1)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(text_data_directory)
    print(f"'{zip_path}' を {text_data_directory} に展開しました。")

def show_help():
    """コマンド一覧と使用方法を表示"""
    print("以下のURLからdata.zipをダウンロードしてください")
    print("https://kwanseio365-my.sharepoint.com/:u:/g/personal/ijv85378_nuc_kwansei_ac_jp/EXOuTKW9DtxHujQPLmjbWYYByXTgE1yy5hx5fHEYjZZG5A?e=kbngES")
    print("最初に　aoyamatype -d [PATH]　を実行してください。PATHはダウンロードしたdata.zipのものです。")
    print("\nコマンド一覧:")
    print("  -r          タイピング履歴を表示")
    print("  -c          スキルチェックを開始")
    print("  -d [PATH]   data.zip を text_data フォルダに展開")
    print("  <file_number> ファイル番号(1~97)でタイピングを開始")

def main():
    # OptionParserオブジェクトを作成
    parser = optparse.OptionParser(usage="usage: %prog [options] <file_number>")

    # オプションを追加
    parser.add_option("-d", "--data", dest="zip_file_path", help="data.zip を text_data フォルダに展開")
    parser.add_option("-r", "--record", action="store_true", dest="record", help="タイピング履歴を表示")
    parser.add_option("-c", "--check", action="store_true", dest="check", help="スキルチェックを開始")

    # 引数を解析
    (options, args) = parser.parse_args()

    # オプションに基づく処理
    if options.zip_file_path:
        extract_zip_to_text_data(options.zip_file_path)
    elif options.record:
        print_log()
    elif options.check:
        word_list_path = get_data_file_path('word.list')
        skill_check(word_list_path)
    elif len(args) == 1:
        try:
            step_number = int(args[0])
        except ValueError:
            print(f"Error: '{args[0]}' は有効なステップ番号ではありません。")
            sys.exit(1)

        text_file_name = f'STEP-{step_number}.txt'
        text_file_path = get_data_file_path(text_file_name)
        if not text_file_path.exists():
            print(f"Error: '{text_file_name}' が見つかりません。")
            sys.exit(1)

        lines = load_lines_from_file(text_file_path)
        play_typing_game(lines, text_file_name)
    else:
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
