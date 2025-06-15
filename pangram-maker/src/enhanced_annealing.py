#!/usr/bin/env python3
"""
改良版焼きなまし法
より積極的な置換と意味保持のバランス
"""

import random
import math
from collections import Counter
import re

# ひらがな46文字
HIRAGANA = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

# より積極的な置換辞書
AGGRESSIVE_REPLACEMENTS = {
    # 季節表現の極限短縮
    'はるかぜふきさくらちる': ['はるさくら', 'かぜちる'],
    'はるかぜさくらちる': ['はるちる', 'さくらかぜ'],
    'なつうみへいく': ['なつうみ', 'うみへ'],
    'あきもみじめで': ['もみじ', 'あきめで'],
    'ふゆゆきこんこん': ['ゆきふる', 'ふゆき'],
    'あきもみじふゆゆき': ['もみじゆき', 'あきふゆ'],
    
    # 人物の極限短縮
    'わかものとしより': ['ひとびと', 'みんな', 'ひと'],
    'ぬのきてやまへ': ['やまいく', 'ぬのきて'],
    
    # 場所・動作の短縮
    'ほしぞらにつきでる': ['つきでる', 'ほしみる'],
    'ねこなくえきで': ['ねこなく', 'えきで'],
    'えきでけんか': ['けんか', 'えき'],
    'むしとぶ': ['むしなく', 'とぶ'],
    'むしなく': ['むし', 'なく'],
    
    # 概念の極限短縮
    'それぞれちがうよろこび': ['よろこび', 'ちがい'],
    'よろこびせけんにある': ['よろこぶ', 'せけん'],
    'せけんにはある': ['せけん', 'ある'],
    'ひとがたのしさをもつ': ['たのしむ', 'ひと'],
    'ひとみなたのしむ': ['たのしむ', 'みな'],
    'すべてのいきもの': ['いきもの', 'すべて'],
    'いきものおなじそらした': ['そらした', 'いきもの'],
    'おなじそらのした': ['そらした', 'した'],
    
    # 助詞を含む表現の短縮
    'ゆめをみた': ['ゆめみる', 'みたゆめ'],
    'すべてれい': ['すれ', 'れい'],
    
    # 句読点の削減パターン
    '。': ['、', ' ', ''],
    '、': [' ', ''],
}

# 必須文字を含む最短表現
REQUIRED_CHARS = {
    'を': ['ゆめを', 'そらを', 'はなを'],
    'ん': ['せけん', 'にほん', 'みん'],
    'ぬ': ['ぬの', 'いぬ', 'ぬ'],
    'へ': ['やまへ', 'うみへ', 'へ'],
}

def analyze_text_detailed(text):
    """詳細なテキスト分析"""
    hiragana_only = [c for c in text if c in HIRAGANA]
    char_count = Counter(hiragana_only)
    
    # 各文字の使用回数
    usage_stats = {}
    for char in HIRAGANA:
        usage_stats[char] = char_count.get(char, 0)
    
    # 重複が多い文字のリスト
    high_duplicates = [(char, count) for char, count in char_count.items() if count > 3]
    
    return {
        'char_count': char_count,
        'usage_stats': usage_stats,
        'high_duplicates': high_duplicates,
        'missing_chars': HIRAGANA - set(char_count.keys()),
        'total_chars': sum(char_count.values()),
        'text_length': len(text)
    }

def smart_replacement(text, analysis):
    """分析に基づくスマートな置換"""
    # 最も重複している文字を特定
    if analysis['high_duplicates']:
        target_char = max(analysis['high_duplicates'], key=lambda x: x[1])[0]
        
        # その文字を含む長い表現を探す
        for pattern, replacements in AGGRESSIVE_REPLACEMENTS.items():
            if target_char in pattern and pattern in text:
                # 置換候補の中で、その文字を含まないものを優先
                best_replacement = None
                for rep in replacements:
                    if target_char not in rep or rep.count(target_char) < pattern.count(target_char):
                        best_replacement = rep
                        break
                
                if best_replacement:
                    return text.replace(pattern, best_replacement, 1)
    
    # 通常の置換
    patterns = list(AGGRESSIVE_REPLACEMENTS.keys())
    random.shuffle(patterns)
    
    for pattern in patterns:
        if pattern in text:
            replacements = AGGRESSIVE_REPLACEMENTS[pattern]
            replacement = random.choice(replacements)
            
            # 必須文字が消えないかチェック
            new_text = text.replace(pattern, replacement, 1)
            if all(char in new_text for char in ['を', 'ん', 'ぬ', 'へ']):
                return new_text
    
    return text

def optimize_with_target(initial_text, target_length=100, max_iterations=10000):
    """目標文字数を設定した最適化"""
    current_text = initial_text
    best_text = current_text
    best_length = len(current_text)
    
    temperature = 100.0
    cooling_rate = 0.995
    
    print(f"初期: {len(initial_text)}文字")
    
    for i in range(max_iterations):
        # 現在の分析
        analysis = analyze_text_detailed(current_text)
        
        # スマート置換
        new_text = smart_replacement(current_text, analysis)
        
        # 変化がない場合はランダム置換
        if new_text == current_text:
            patterns = [p for p in AGGRESSIVE_REPLACEMENTS.keys() if p in current_text]
            if patterns:
                pattern = random.choice(patterns)
                replacement = random.choice(AGGRESSIVE_REPLACEMENTS[pattern])
                new_text = current_text.replace(pattern, replacement, 1)
        
        # 評価
        new_analysis = analyze_text_detailed(new_text)
        
        # 受理判定
        delta_length = len(new_text) - len(current_text)
        delta_missing = len(new_analysis['missing_chars']) - len(analysis['missing_chars'])
        
        # 不足文字が増える場合は基本的に拒否
        if delta_missing > 0:
            accept_prob = 0.01
        # 文字数が減る場合は積極的に受理
        elif delta_length < 0:
            accept_prob = 0.95
        # 文字数が増える場合は温度に依存
        else:
            accept_prob = math.exp(-delta_length / temperature)
        
        if random.random() < accept_prob:
            current_text = new_text
            
            # ベスト更新
            if len(new_text) < best_length and not new_analysis['missing_chars']:
                best_text = new_text
                best_length = len(new_text)
                print(f"\n改善! {best_length}文字: {best_text[:50]}...")
                
                if best_length <= target_length:
                    print(f"\n★ {target_length}文字以下達成！")
                    break
        
        temperature *= cooling_rate
        
        if i % 1000 == 0:
            print(f".", end="", flush=True)
    
    return best_text

def create_ultra_short_pangram():
    """超短縮パングラムの作成"""
    # 複数の初期テキストから開始
    candidates = [
        # try03の最短版
        "はるかぜふきさくらちる。なつうみへいく。あきもみじめでふゆゆきこんこん。わかものとしよりぬのきてやまへ。ほしぞらにつきでる。ねこがなくえきでけんかむしとぶ。それぞれちがうよろこびせけんにはある。ひとがたのしさをもつ。すべてのいきものおなじそらのした。",
        
        # 焼きなまし結果
        "かぜふくはなちる。うみへ。あきもみじめでふゆゆき。わかものとしよりぬのきてやまへ。ほしぞら。ねこなくえきでむしなく。それぞれちがうよろこびせけんに。ひとがたのしさをもつ。すべてのいきものおなじそらのした。",
        
        # 手動調整版
        "ゆめをみた。はるかぜさくらちる。なつうみへ。あきもみじふゆゆき。わかものとしよりぬのきてやまへ。ほしぞら。ねこなくえきでけんか。むしとぶ。よろこびせけんにある。ひとみなたのしむ。いきものおなじそらした。すべてれい。",
    ]
    
    best_result = None
    best_length = float('inf')
    
    for i, candidate in enumerate(candidates):
        print(f"\n=== 候補{i+1}から最適化 ===")
        result = optimize_with_target(candidate, target_length=95)
        
        analysis = analyze_text_detailed(result)
        if not analysis['missing_chars'] and len(result) < best_length:
            best_result = result
            best_length = len(result)
    
    return best_result

if __name__ == "__main__":
    print("=== 超短縮パングラム作成 ===\n")
    
    # 実行
    final_text = create_ultra_short_pangram()
    
    if final_text:
        print(f"\n\n=== 最終結果 ===")
        print(f"テキスト: {final_text}")
        print(f"文字数: {len(final_text)}")
        
        # 最終分析
        final_analysis = analyze_text_detailed(final_text)
        print(f"不足文字: {''.join(sorted(final_analysis['missing_chars']))}")
        print(f"最高重複: {max(final_analysis['char_count'].values()) if final_analysis['char_count'] else 0}")
        
        # 重複文字の詳細
        print("\n重複文字（3回以上）:")
        for char, count in sorted(final_analysis['high_duplicates'], key=lambda x: x[1], reverse=True):
            print(f"  {char}: {count}回")