# aoyamatype/typing_game.py

import sys
import time
import os
import threading
from datetime import datetime

def load_lines_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    return lines

def counter(word1, word2):
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

def get_user_input():
    try:
        return input().strip()
    except EOFError:
        return ''

def record_session_data(file_name, total_words, total_time):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S +0900")
    data_directory = 'data'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    with open(os.path.join(data_directory, 'training_date.txt'), 'a', encoding='utf-8') as file:
        file.write(f"{date_str},{file_name},{total_words},{total_time}\n")

def play_typing_game(lines, file_name):
    total_words = 0
    index = 0
    total_time = 20  # 制限時間（秒）
    start_time = time.time()

    print("タイピングゲームへようこそ！")
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m aoyamatype <file_number>")
        sys.exit(1)

    file_number = sys.argv[1]
    file_path = f"data/STEP-{file_number}.txt"

    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    # ファイルから行のリストを読み込む
    lines = load_lines_from_file(file_path)

    # ゲームを開始する
    play_typing_game(lines, file_path)
