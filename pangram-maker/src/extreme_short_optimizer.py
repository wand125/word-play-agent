#!/usr/bin/env python3
"""
極限短縮最適化
必須文字を保持しつつ最短を目指す
"""

from collections import Counter

# ひらがな46文字
HIRAGANA_BASE = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

def check_pangram(text):
    """パングラムチェック"""
    chars = set()
    for c in text:
        if c in HIRAGANA_BASE:
            chars.add(c)
        elif c in 'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ':
            # 濁音を清音に変換
            mapping = {
                'が':'か', 'ぎ':'き', 'ぐ':'く', 'げ':'け', 'ご':'こ',
                'ざ':'さ', 'じ':'し', 'ず':'す', 'ぜ':'せ', 'ぞ':'そ',
                'だ':'た', 'ぢ':'ち', 'づ':'つ', 'で':'て', 'ど':'と',
                'ば':'は', 'び':'ひ', 'ぶ':'ふ', 'べ':'へ', 'ぼ':'ほ',
                'ぱ':'は', 'ぴ':'ひ', 'ぷ':'ふ', 'ぺ':'へ', 'ぽ':'ほ'
            }
            chars.add(mapping.get(c, c))
    
    missing = HIRAGANA_BASE - chars
    hiragana_count = len([c for c in text if c in HIRAGANA_BASE or c in 'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ'])
    
    return {
        'is_pangram': len(missing) == 0,
        'missing': missing,
        'hiragana_count': hiragana_count,
        'coverage': len(chars)
    }

# 必須文字を含む最短単語
ESSENTIAL_WORDS = {
    'を': 'ゆめを',      # 3文字
    'ぬ': 'ぬの',        # 2文字
    'へ': 'うみへ',      # 3文字（または「やまへ」）
    'ん': 'けん',        # 2文字（または「せん」）
    'ち': 'ちる',        # 2文字（または「ち」単独）
    'り': 'おり',        # 2文字（または「り」単独）
    'お': 'おり',        # 2文字（または「お」単独）
    'に': 'にわ',        # 2文字（または「に」単独）
}

def create_minimal_pangram():
    """最小パングラム作成"""
    
    # 基本構造（必須要素を含む）
    segments = [
        # 必須文字確保
        "ゆめを",      # を
        "ぬの",        # ぬ
        "うみへ",      # へ
        "けんか",      # ん、け
        "ちる",        # ち
        "おり",        # お、り
        "にわ",        # に
        
        # 季節（短縮版）
        "はる",        # は、る
        "なつ",        # な、つ
        "あき",        # あ、き
        "ふゆ",        # ふ、ゆ
        
        # その他必須
        "みた",        # み、た
        "さく",        # さ、く
        "もじ",        # も、じ（濁音でしを確保）
        "ゆき",        # ゆ、き（重複OK）
        "ひと",        # ひ、と
        "やま",        # や、ま
        "ほし",        # ほ、し
        "ぞら",        # ぞ（濁音でそを確保）、ら
        "ねこ",        # ね、こ
        "えき",        # え、き（重複OK）
        "むし",        # む、し（重複OK）
        "とぶ",        # と（重複OK）、ぶ（濁音でふを確保）
        "よろ",        # よ、ろ
        "こび",        # こ（重複OK）、び（濁音でひを確保）
        "せげ",        # せ、げ（濁音でけを確保）
        "たの",        # た（重複OK）、の（重複OK）
        "いき",        # い、き（重複OK）
        "もの",        # も（重複OK）、の（重複OK）
        "そら",        # そ、ら（重複OK）
        "すべ",        # す、べ（濁音でへを確保）
        "てれ",        # て、れ
        "いわ",        # い（重複OK）、わ
    ]
    
    # 文として組み立て
    versions = [
        # Version 1: 最短構成
        "ゆめをみた。はるちる。なつうみへ。あきもじ。ふゆゆき。ひと、ぬのきてやまおり。ほしぞら。ねこ、えきでけんか。むしとぶ。よろこび、せげん。たのし。いきもの、そらにわ。すべてれいわ。",
        
        # Version 2: 別構成
        "ゆめをみた。はるさく。なつうみへ。あきちる。ふゆ、ゆき。ひとぬのきてやまにおり。ほしぞら。ねこ、えきでけんか。むしとぶ。よろこび、せげん。たのじ。いきもの、そらした。すべてれいわ。",
        
        # Version 3: さらに圧縮
        "ゆめをみた。はるちり、なつうみへ。あきも、ふゆゆき。ひとぬのきてやまにおり。ほしぞら。ねこ、えきでけんか。むしとぶ。よろこび、せげん。たのじさ。いきもの、そらした。すべてれいわ。",
    ]
    
    best_text = None
    best_count = float('inf')
    
    for i, text in enumerate(versions):
        result = check_pangram(text)
        print(f"\nVersion {i+1}:")
        print(f"  文字数: {result['hiragana_count']}")
        print(f"  カバー率: {result['coverage']}/46")
        print(f"  パングラム: {'○' if result['is_pangram'] else '×'}")
        
        if result['missing']:
            print(f"  不足: {''.join(sorted(result['missing']))}")
        
        if result['is_pangram'] and result['hiragana_count'] < best_count:
            best_text = text
            best_count = result['hiragana_count']
    
    return best_text, best_count

def optimize_existing():
    """既存テキストの最適化"""
    base = "ゆめをみた。はるかぜ、さくらちる。なつうみへ。あきもみじ、ふゆゆき。ひとびとぬのきてやまにおり。ほしぞら。ねこなく、えきでけんか。むしとぶ。よろこびせけん。たのしさもつ。いきもの、そらした。すべてれいわ。"
    
    # 段階的短縮
    steps = [
        # Step 1: 長い表現を短く
        ("はるかぜ、さくらちる", "はるちる"),
        ("あきもみじ", "あきも"),
        ("ひとびと", "ひと"),
        ("ねこなく", "ねこ"),
        ("よろこびせけん", "よろこび、せげん"),
        ("たのしさもつ", "たのじ"),
        ("すべてれいわ", "すべてれいわ"),  # これは必須
        
        # Step 2: 助詞削減
        ("いきもの、そらした", "いきものそらした"),
        
        # Step 3: さらなる短縮
        ("ふゆゆき", "ふゆ、ゆき"),
    ]
    
    current = base
    print("\n=== 段階的最適化 ===")
    
    for old, new in steps:
        if old in current:
            current = current.replace(old, new)
            result = check_pangram(current)
            print(f"\n{old} → {new}")
            print(f"  文字数: {result['hiragana_count']}")
            print(f"  不足: {''.join(sorted(result['missing']))}")
    
    return current

if __name__ == "__main__":
    print("=== 極限短縮パングラム ===")
    
    # 新規作成
    best_new, count_new = create_minimal_pangram()
    
    # 既存最適化
    optimized = optimize_existing()
    result_opt = check_pangram(optimized)
    
    print("\n\n=== 最終結果 ===")
    
    if best_new:
        print(f"\n新規作成版 ({count_new}文字):")
        print(best_new)
    
    print(f"\n最適化版 ({result_opt['hiragana_count']}文字):")
    print(optimized)
    
    # 最良を選択
    if best_new and count_new < result_opt['hiragana_count']:
        final = best_new
        final_count = count_new
    else:
        final = optimized
        final_count = result_opt['hiragana_count']
    
    print(f"\n\n最良版 ({final_count}文字):")
    print(final)