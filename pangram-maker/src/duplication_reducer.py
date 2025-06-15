#!/usr/bin/env python3
"""
重複削減最適化エンジン
重複の多い文字を含む単語を置換
"""

from collections import Counter

# ひらがな
HIRAGANA_BASE = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')
HIRAGANA_ALL = set('あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゆよらりるれろわをん')

def analyze_duplicates(text):
    """重複分析"""
    hiragana_chars = [c for c in text if c in HIRAGANA_ALL]
    counter = Counter(hiragana_chars)
    
    # 清音化してカウント
    seion_chars = []
    for c in text:
        if c in HIRAGANA_BASE:
            seion_chars.append(c)
        elif c in 'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ':
            mapping = {
                'が':'か', 'ぎ':'き', 'ぐ':'く', 'げ':'け', 'ご':'こ',
                'ざ':'さ', 'じ':'し', 'ず':'す', 'ぜ':'せ', 'ぞ':'そ',
                'だ':'た', 'ぢ':'ち', 'づ':'つ', 'で':'て', 'ど':'と',
                'ば':'は', 'び':'ひ', 'ぶ':'ふ', 'べ':'へ', 'ぼ':'ほ',
                'ぱ':'は', 'ぴ':'ひ', 'ぷ':'ふ', 'ぺ':'へ', 'ぽ':'ほ'
            }
            seion_chars.append(mapping.get(c, c))
    
    seion_counter = Counter(seion_chars)
    missing = HIRAGANA_BASE - set(seion_counter.keys())
    
    return {
        'total_hiragana': len(hiragana_chars),
        'duplicates': [(c, cnt) for c, cnt in counter.items() if cnt >= 2],
        'missing_seion': missing,
        'seion_count': seion_counter
    }

# 重複削減のための置換辞書
REDUCTION_DICT = {
    # 「き」を含む単語の代替
    'いきもの': ['もの', 'いちもつ', 'ぶつ'],
    'あきちる': ['あき', 'ちる'],
    'ゆき': ['ゆき'],  # 必須なので残す
    'えき': ['えき'],  # 必須
    
    # 「た」を含む単語の代替
    'みた': ['みる', 'みて'],
    'たのじ': ['らく', 'たの'],
    'した': ['した'],  # 必須
    
    # 「の」を含む単語の代替
    'たのじ': ['らく', 'たの'],
    'いきもの': ['もの', 'ぶつ'],
    
    # 「し」を含む単語の代替
    'ほしぞら': ['ほし', 'そら', 'よぞら'],
    'むしとぶ': ['むし', 'とぶ'],
    
    # その他の最適化
    'よろこび': ['よろ', 'よろこび'],
    'すべてれいわ': ['すれいわ', 'れいわ'],
}

def create_optimized_versions():
    """最適化版の作成"""
    
    base = "ゆめをみた。はるさく。なつうみへ。あきちる。ふゆ、ゆき。ひとぬのきてやまにおり。ほしぞら。ねこ、えきでけんか。むしとぶ。よろこび、せげん。たのじ。いきもの、そらした。すべてれいわ。"
    
    versions = [
        # Version 1: いきもの→もの、たのじ→らく
        "ゆめをみた。はるさく。なつうみへ。あきちる。ふゆ、ゆき。ひとぬのきてやまにおり。ほしぞら。ねこ、えきでけんか。むしとぶ。よろこび、せげん。らく。もの、そらした。すべてれいわ。",
        
        # Version 2: むしとぶ→むし、そらとぶ
        "ゆめをみた。はるちる。なつうみへ。あきさく。ふゆゆき。ひとぬのきてやまにおり。ほしぞら。ねこ、えきでけんか。むし。よろこび、せげん。たのじ。もの、そらとぶ。すべてれいわ。",
        
        # Version 3: ほしぞら→ほし、よぞら追加
        "ゆめをみた。はるさく。なつうみへ。あき。ふゆゆき。ひとぬのきてやまにおり。ほし。ねこ、えきでけんか。むしとぶ。よろこび、せげん。らく。もの、よぞらした。すべてれいわ。ちる。",
        
        # Version 4: みた→みる
        "ゆめをみる。はるさく。なつうみへ。あきちる。ふゆゆき。ひとぬのきてやまにおり。ほしぞら。ねこ、えきでけんか。むし。よろこび、せげん。らく。もの、そらとぶ。すべてれいわ。",
        
        # Version 5: 大胆な再構成
        "ゆめをみた。はる。なつうみへ。あきもみじ。ふゆ。ひとぬのきてやまにおり。ほし。ねこ、えきでけんか。むしとぶ。よろこび、せげん。さくちる。らく。もの、そらした。すれいわ。ゆき。",
    ]
    
    best_result = None
    best_count = float('inf')
    
    for i, text in enumerate(versions):
        analysis = analyze_duplicates(text)
        print(f"\nVersion {i+1}:")
        print(f"  文字数: {analysis['total_hiragana']}")
        print(f"  不足: {''.join(sorted(analysis['missing_seion']))}")
        
        if not analysis['missing_seion'] and analysis['total_hiragana'] < best_count:
            best_result = text
            best_count = analysis['total_hiragana']
            
            # 重複状況
            print("  重複(2回以上):")
            for char, count in sorted(analysis['duplicates'], key=lambda x: x[1], reverse=True):
                if count >= 3:
                    print(f"    {char}: {count}回")
    
    return best_result, best_count

def extreme_reduction():
    """極限の重複削減"""
    
    # 必須要素を最小限に
    essential_segments = [
        "ゆめを",      # を
        "ぬの",        # ぬ
        "へ",          # へ（単独または「うみへ」）
        "けんか",      # ん、け
        "ちる",        # ち、る
        "おり",        # お、り
        "に",          # に（単独）
    ]
    
    # 70文字を目指す構成
    extreme_versions = [
        # 極限版1
        "ゆめをみた。はる。なつうみへ。あき、ちる。ふゆ。ひとぬのきてやま、おり。ほし。ねこ、えきでけんか。むし、とぶ。よろ、せげん。らく。もの、そらにさく。すべてれいわ。ゆき、もじ。",
        
        # 極限版2  
        "ゆめをみる。はるさく。なつうみへ。あき。ふゆ。ひとぬのきてやまにおり。ほし、ちる。ねこ、えきでけんか。むしとぶ。よろこび、せげん。らく。もの、そらした。すれいわ。ゆき、もじ。",
        
        # 極限版3
        "ゆめをみた。はる、ちり。なつうみへ。あきさく。ふゆ。ひとぬのきてやまにおり。ほし。ねこ、えきでけんか。むし、とぶ。よろ、せげん。らく。ものそらした。すべてれいわ。ゆき、もじ。",
    ]
    
    for i, text in enumerate(extreme_versions):
        analysis = analyze_duplicates(text)
        print(f"\n極限版{i+1}:")
        print(f"  文字数: {analysis['total_hiragana']}")
        print(f"  不足: {''.join(sorted(analysis['missing_seion']))}")

if __name__ == "__main__":
    print("=== 重複削減最適化 ===")
    
    # 通常の最適化
    best_text, best_count = create_optimized_versions()
    
    print("\n\n=== 極限削減への挑戦 ===")
    extreme_reduction()
    
    if best_text:
        print(f"\n\n=== 最良結果 ===")
        print(f"文字数: {best_count}文字")
        print(f"テキスト:\n{best_text}")