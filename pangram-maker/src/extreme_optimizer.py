#!/usr/bin/env python3
"""
極限最適化エンジン
文構造を根本から見直す革新的アプローチ
"""

import random
from collections import Counter
import itertools

# ひらがな46文字
HIRAGANA = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

def count_hiragana_only(text):
    """ひらがなのみをカウント"""
    return len([c for c in text if c in HIRAGANA])

# 極限短縮辞書
EXTREME_REPLACEMENTS = {
    # 超短縮パターン
    'かぜふくはなちる': ['風花散', 'かぜちる'],
    'あきもみじめで': ['秋見で', 'もみじ'],
    'ふゆゆき': ['冬雪', 'ゆき'],
    'わかものとしより': ['皆', 'みな'],
    'ぬのきてやまへ': ['山へ', 'やま'],
    'ほしぞら': ['星', 'そら'],
    'ねこなくえきで': ['猫駅', 'ねこ'],
    'むしなく': ['虫', 'む'],
    'それぞれちがう': ['各', 'ちがう'],
    'よろこびせけんに': ['喜び', 'よろこぶ'],
    'ひとがたのしさをもつ': ['楽し', 'たのし'],
    'すべてのいきもの': ['皆', 'みな'],
    'おなじした': ['下', 'した'],
    
    # 文末処理
    'そらのした': ['下', 'した'],
    'おなじそらした': ['皆下', 'した'],
}

# 必須文字を含む最短単語
ESSENTIAL_WORDS = {
    'を': ['を', 'をも'],
    'ん': ['ん', 'せん', 'けん'],
    'ぬ': ['ぬ', 'いぬ', 'きぬ'],
    'へ': ['へ', 'へや'],
    'ろ': ['ろ', 'いろ'],
    'ゐ': [],  # 現代仮名では不要
    'ゑ': [],  # 現代仮名では不要
}

def create_minimal_pangram():
    """最小限のパングラムを構築"""
    used_chars = set()
    segments = []
    
    # 基本構造（必須要素を含む）
    base_segments = [
        "ゆめをみた",  # を
        "はるかぜ",    # は、る、か、ぜ
        "さくらちる",  # さ、く、ら、ち、る
        "なつうみへ",  # な、つ、う、み、へ
        "あきもみじ",  # あ、き、も、み、じ
        "ふゆゆき",    # ふ、ゆ、き
        "ひとぬのきて", # ひ、と、ぬ、の、き、て
        "やま",        # や、ま
        "ほしぞら",    # ほ、し、ぞ、ら
        "ねこなく",    # ね、こ、な、く
        "えきで",      # え、き、で
        "けんか",      # け、ん、か
        "むしとぶ",    # む、し、と、ぶ
        "よろこび",    # よ、ろ、こ、び
        "せけん",      # せ、け、ん
        "たのしさ",    # た、の、し、さ
        "いきもの",    # い、き、も、の
        "そらした",    # そ、ら、し、た
        "すべてれいわ", # す、べ、て、れ、い、わ
    ]
    
    # 使用文字を確認
    for segment in base_segments:
        for char in segment:
            if char in HIRAGANA:
                used_chars.add(char)
    
    # 不足文字を確認
    missing = HIRAGANA - used_chars
    print(f"基本構造での不足文字: {''.join(sorted(missing))}")
    
    # 最適な組み合わせを探す
    return optimize_combination(base_segments)

def optimize_combination(segments):
    """セグメントの最適な組み合わせを探す"""
    # 各セグメントを短縮可能か確認
    optimized_segments = []
    
    for segment in segments:
        # 短縮可能なパターンを探す
        shortened = False
        for pattern, replacements in EXTREME_REPLACEMENTS.items():
            if pattern in segment and replacements:
                # 最短の置換を選択
                shortest = min(replacements, key=len)
                if len(shortest) < len(segment):
                    optimized_segments.append(shortest)
                    shortened = True
                    break
        
        if not shortened:
            optimized_segments.append(segment)
    
    # 文として組み立て
    result = build_sentence(optimized_segments)
    return result

def build_sentence(segments):
    """セグメントから文を構築"""
    # グループ化して文を作る
    sentences = []
    current = []
    
    for i, seg in enumerate(segments):
        current.append(seg)
        
        # 適切な位置で区切る
        if i > 0 and i % 3 == 0:
            sentences.append(''.join(current) + '。')
            current = []
    
    if current:
        sentences.append(''.join(current) + '。')
    
    return ''.join(sentences)

def extreme_search():
    """極限探索"""
    print("=== 極限パングラム探索 ===\n")
    
    # 手動で構築した極限短縮版
    manual_attempts = [
        # 試行1: 最短を目指す
        "ゆめをみた。はるかぜさくらちる。なつうみへ。あきもみじふゆゆき。ひとぬのきてやま。ほしぞら。ねこなくえきでけんか。むしとぶ。よろこびせけん。たのしさ。いきものそらした。すべてれいわ。",
        
        # 試行2: 重複を削減
        "ゆめをみる。はるかぜさくらちり、なつうみへ。あきもみじ、ふゆゆき。ひとぬのきてやま。ほしぞら、ねこなく。えきでけんか、むしとぶ。よろこび、せけんに。たのしさもつ。いきもの、そらした。すべてれいわ。",
        
        # 試行3: 極限圧縮
        "ゆめをみた。はるさくら、なつうみへ。あきもみじ、ふゆ。ひとぬのきてやま。ほしぞら。ねこ、えきでけんか。むしとぶ。よろこびせけん。たのし。いきものそらした。すべてれいわ。",
    ]
    
    best_text = None
    best_count = float('inf')
    
    for i, text in enumerate(manual_attempts):
        hiragana_count = count_hiragana_only(text)
        hiragana_only = [c for c in text if c in HIRAGANA]
        char_count = Counter(hiragana_only)
        missing = HIRAGANA - set(char_count.keys())
        
        print(f"\n試行{i+1}:")
        print(f"テキスト: {text}")
        print(f"ひらがな数: {hiragana_count}")
        print(f"総文字数: {len(text)}")
        print(f"不足文字: {''.join(sorted(missing))}")
        
        if not missing and hiragana_count < best_count:
            best_text = text
            best_count = hiragana_count
    
    # アルゴリズムによる探索
    print("\n\n=== アルゴリズム探索 ===")
    algorithmic_result = algorithmic_search()
    
    if algorithmic_result:
        algo_count = count_hiragana_only(algorithmic_result)
        if algo_count < best_count:
            best_text = algorithmic_result
            best_count = algo_count
    
    return best_text, best_count

def algorithmic_search():
    """アルゴリズムによる極限探索"""
    # 必須要素のリスト
    essentials = [
        "ゆめを",      # を
        "ぬの",        # ぬ
        "へ",          # へ
        "ん",          # ん
    ]
    
    # 季節表現（短縮版）
    seasons = [
        "はるさくら",
        "なつうみ",
        "あきもみじ", 
        "ふゆゆき",
    ]
    
    # その他の要素
    elements = [
        "ひと", "やま", "ほしぞら",
        "ねこ", "えき", "けんか",
        "むし", "とぶ", "よろこび",
        "せけ", "たのし", "いきもの",
        "そらした", "すべてれいわ",
    ]
    
    # 最適な組み合わせを探す
    best_combination = None
    best_length = float('inf')
    
    # 100回試行
    for _ in range(100):
        # ランダムに組み合わせる
        combination = essentials + seasons + elements
        random.shuffle(combination)
        
        # 文を構築
        text = ""
        for i, elem in enumerate(combination):
            text += elem
            if i % 4 == 3:
                text += "。"
            elif i % 2 == 1:
                text += "、"
        
        if not text.endswith("。"):
            text += "。"
        
        # 評価
        hiragana_only = [c for c in text if c in HIRAGANA]
        char_count = Counter(hiragana_only)
        missing = HIRAGANA - set(char_count.keys())
        
        if not missing and len(hiragana_only) < best_length:
            best_combination = text
            best_length = len(hiragana_only)
    
    return best_combination

if __name__ == "__main__":
    best_text, best_count = extreme_search()
    
    if best_text:
        print(f"\n\n=== 最良の結果 ===")
        print(f"テキスト: {best_text}")
        print(f"ひらがな数: {best_count}文字")
        print(f"総文字数: {len(best_text)}文字")
        
        # 詳細分析
        hiragana_only = [c for c in best_text if c in HIRAGANA]
        char_count = Counter(hiragana_only)
        
        print(f"\n文字使用頻度（3回以上）:")
        for char, count in sorted(char_count.items(), key=lambda x: x[1], reverse=True):
            if count >= 3:
                print(f"  {char}: {count}回")