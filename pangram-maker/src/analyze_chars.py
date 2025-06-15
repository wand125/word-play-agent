#!/usr/bin/env python3
"""
文字連続性分析ツール
日本語テキストから文字の連続パターンを分析
"""

import sys
from collections import defaultdict, Counter

# ひらがな46文字
HIRAGANA = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

def analyze_bigrams(text):
    """2文字の連続パターンを分析"""
    bigrams = defaultdict(Counter)
    
    # ひらがなのみ抽出
    hiragana_text = [char for char in text if char in HIRAGANA]
    
    # 2文字組を収集
    for i in range(len(hiragana_text) - 1):
        first = hiragana_text[i]
        second = hiragana_text[i + 1]
        bigrams[first][second] += 1
    
    return bigrams

def find_valid_sequences(bigrams, min_count=1):
    """有効な文字連続を抽出"""
    sequences = defaultdict(list)
    
    for first_char, followers in bigrams.items():
        valid_followers = [char for char, count in followers.items() 
                          if count >= min_count]
        if valid_followers:
            sequences[first_char] = sorted(valid_followers)
    
    return sequences

def find_dead_ends(sequences):
    """行き止まり文字（後続がない）を検出"""
    all_chars = HIRAGANA
    dead_ends = []
    
    for char in all_chars:
        if char not in sequences or not sequences[char]:
            dead_ends.append(char)
    
    return dead_ends

def find_starting_chars(sequences):
    """開始に適した文字を検出"""
    # 多くの後続を持つ文字
    start_candidates = []
    
    for char, followers in sequences.items():
        if len(followers) >= 10:  # 10文字以上の後続を持つ
            start_candidates.append((char, len(followers)))
    
    return sorted(start_candidates, key=lambda x: x[1], reverse=True)

def print_analysis(sequences):
    """分析結果を表示"""
    print("=== 文字連続性分析結果 ===\n")
    
    # 各文字の後続可能文字
    print("【後続可能文字】")
    for char in sorted(sequences.keys()):
        followers = sequences[char]
        print(f"{char} → {', '.join(followers)} ({len(followers)}文字)")
    
    print("\n【統計情報】")
    # 後続文字数の統計
    follower_counts = [len(followers) for followers in sequences.values()]
    if follower_counts:
        avg_followers = sum(follower_counts) / len(follower_counts)
        print(f"平均後続文字数: {avg_followers:.1f}")
        print(f"最大後続文字数: {max(follower_counts)}")
        print(f"最小後続文字数: {min(follower_counts)}")
    
    # 行き止まり文字
    dead_ends = find_dead_ends(sequences)
    if dead_ends:
        print(f"\n行き止まり文字: {', '.join(dead_ends)}")
    
    # 開始に適した文字
    start_chars = find_starting_chars(sequences)
    if start_chars:
        print("\n開始に適した文字:")
        for char, count in start_chars[:10]:
            print(f"  {char}: {count}文字の後続")

def analyze_perfect_pangram_potential(sequences):
    """完全パングラムの可能性を分析"""
    print("\n=== 完全パングラム可能性分析 ===\n")
    
    # グラフとしての分析
    all_chars = set(sequences.keys())
    reachable = defaultdict(set)
    
    # 各文字から到達可能な文字を計算
    for start in all_chars:
        visited = set()
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            if current in sequences:
                for next_char in sequences[current]:
                    if next_char not in visited:
                        queue.append(next_char)
        
        reachable[start] = visited
    
    # 全文字に到達可能な開始文字
    complete_starts = []
    for char, reached in reachable.items():
        if len(reached) == 46:
            complete_starts.append(char)
    
    if complete_starts:
        print(f"全文字に到達可能な開始文字: {', '.join(complete_starts)}")
    else:
        print("警告: 全文字に到達可能な開始文字がありません")
    
    # 最長パスの推定
    print("\n各文字からの最大到達文字数:")
    for char, reached in sorted(reachable.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        print(f"  {char}: {len(reached)}文字")

if __name__ == "__main__":
    # サンプルテキスト（実際の日本語文章）
    sample_text = """
    春になると桜が咲く。夏は海で泳ぐ。秋には紅葉を見る。冬は雪が降る。
    日本の四季は美しい。朝日が昇り、夕日が沈む。鳥が鳴き、風が吹く。
    若者も年寄りも、みんなで楽しむ。布で作った服を着て、山へ行く。
    雨の日は家で本を読む。晴れた日は外で遊ぶ。
    """
    
    if len(sys.argv) > 1:
        # ファイルから読み込み
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sample_text
    
    # 分析実行
    bigrams = analyze_bigrams(text)
    sequences = find_valid_sequences(bigrams)
    
    # 結果表示
    print_analysis(sequences)
    analyze_perfect_pangram_potential(sequences)