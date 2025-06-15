#!/usr/bin/env python3
"""
極限最適化エンジン
不要要素を徹底的に削除して60文字を目指す
"""

from collections import Counter

HIRAGANA_46 = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

def create_extreme_versions():
    """極限的な短縮版を作成"""
    
    # 現在の66文字版
    current = """ゆめをみた。はる。なつうみへ。あき、ちる。ふゆ。
ひとぬのきてやま、おり。ほし。ねこ、えきでけんか。
むし、とぶ。よろ、せげん。らく。もの、そらにさく。
すべてれいわ。ゆき、もじ。"""
    
    # 削除可能な要素
    removable = {
        'すべてれいわ': 7,  # 時代表現
        'らく': 2,           # 感情
        'よろ': 2,           # 感情断片
        'もじ': 2,           # メタ表現
        'はる': 2,           # 季節（他にもある）
        'ふゆ': 2,           # 季節（他にもある）
    }
    
    versions = []
    
    # Version 1: 基本削除版（れ、わ、じの代替必要）
    v1 = """ゆめをみた。あき。なつうみへ。ひとぬのきて。
ねこ、えきでけんか。むしとぶ。ほし。
やまにおり、ちる。せげん。ものさくそら。
ゆきふ。はじ。すれ。いわ。よ。ろ。"""
    
    # Version 2: さらに圧縮
    v2 = """ゆめをみた。あきいろ。なつうみへ。
ひとぬのきて。ねこ、えきでけんか。
むしとぶ。ほし。やまにおり、ちる。
せげん。ものさくそら。ゆきふ。
はじ。すれわ。よ。ろ。"""
    
    # Version 3: 究極圧縮
    v3 = """ゆめをみた。あきいろ。なつうみへ。
ひとぬのきて。ねこえきでけんか。
むしとぶ。ほしそら。やまにおり、ちる。
せげん。ものさく。ゆきふ。
はじ。すれわよろ。"""
    
    # Version 4: 60文字挑戦版
    v4 = """ゆめをみる。あきいろ。なつうみへ。
ひとぬのきて。ねこえきでけんか。
むしとぶ。ほしそら。やまおり、ちす。
せげん。ものさく。ゆきふ。
はじ。われよ。"""
    
    versions = [v1, v2, v3, v4]
    
    # 各バージョンを検証
    results = []
    for i, text in enumerate(versions):
        hiragana = [c for c in text if c in HIRAGANA_46]
        used = set(hiragana)
        missing = HIRAGANA_46 - used
        count = len(hiragana)
        
        results.append({
            'version': i + 1,
            'text': text,
            'count': count,
            'missing': missing,
            'is_pangram': len(missing) == 0
        })
    
    return results

def find_minimal_additions(missing_chars):
    """不足文字を補う最小の追加"""
    additions = {
        'れ': ['れ', 'これ', 'され', 'われ'],
        'わ': ['わ', 'われ', 'かわ', 'わら'],
        'じ': ['じ', 'はじ', 'ふじ', 'じめ'],
        'は': ['は', 'はな', 'はく', 'はり'],
        'せ': ['せ', 'せん', 'せき', 'せい'],
        'す': ['す', 'すき', 'すむ', 'すれ'],
        'よ': ['よ', 'よる', 'よい', 'よく'],
        'ろ': ['ろ', 'ろく', 'ころ', 'しろ'],
    }
    
    min_addition = []
    for char in missing_chars:
        if char in additions:
            min_addition.append(additions[char][0])
    
    return min_addition

if __name__ == "__main__":
    print("=== 極限最適化への挑戦 ===\n")
    
    results = create_extreme_versions()
    
    best_pangram = None
    best_count = float('inf')
    
    for result in results:
        print(f"Version {result['version']}:")
        print(f"  文字数: {result['count']}")
        print(f"  パングラム: {'✅' if result['is_pangram'] else '❌'}")
        
        if result['missing']:
            print(f"  不足: {''.join(sorted(result['missing']))}")
            additions = find_minimal_additions(result['missing'])
            print(f"  必要な追加: {', '.join(additions)} (+{sum(len(a) for a in additions)}文字)")
        
        if result['is_pangram'] and result['count'] < best_count:
            best_pangram = result
            best_count = result['count']
        
        print()
    
    if best_pangram:
        print(f"\n=== 最良結果: {best_count}文字 ===")
        print(best_pangram['text'])
    else:
        print("\n完全なパングラムは見つかりませんでした。")
        print("手動での調整が必要です。")