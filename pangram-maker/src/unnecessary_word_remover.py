#!/usr/bin/env python3
"""
不要単語削除エンジン
必須文字以外の冗長な要素を削除
"""

from collections import Counter

# ひらがな
HIRAGANA_BASE = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

def analyze_necessity(text):
    """各単語の必要性を分析"""
    segments = text.replace('。', '、').split('、')
    segments = [s.strip() for s in segments if s.strip()]
    
    # 各セグメントの分析
    analysis = []
    for seg in segments:
        hiragana = [c for c in seg if c in HIRAGANA_BASE]
        unique_chars = set(hiragana)
        
        analysis.append({
            'segment': seg,
            'length': len(hiragana),
            'unique_chars': unique_chars,
            'unique_count': len(unique_chars),
            'efficiency': len(unique_chars) / len(hiragana) if hiragana else 0
        })
    
    return analysis

def find_redundant_segments(analysis):
    """冗長なセグメントを特定"""
    # 全体の文字使用状況を確認
    all_chars = set()
    for item in analysis:
        all_chars.update(item['unique_chars'])
    
    redundant = []
    for item in analysis:
        # このセグメントを除いても全文字が揃うかチェック
        other_chars = set()
        for other in analysis:
            if other != item:
                other_chars.update(other['unique_chars'])
        
        if all_chars.issubset(other_chars):
            redundant.append(item)
    
    return redundant

def create_minimal_pangram():
    """最小構成のパングラムを作成"""
    
    base_text = """ゆめをみた。はる。なつうみへ。あき、ちる。ふゆ。
ひとぬのきてやま、おり。ほし。ねこ、えきでけんか。
むし、とぶ。よろ、せげん。らく。もの、そらにさく。
すべてれいわ。ゆき、もじ。"""
    
    # 必須要素（貴重な文字を含む）
    essential = {
        'ゆめを': set('ゆめを'),  # 「を」が貴重
        'うみへ': set('うみへ'),  # 「へ」が貴重
        'ぬの': set('ぬの'),      # 「ぬ」が貴重
        'けんか': set('けんか'),  # 「ん」が貴重
    }
    
    # 削除候補
    removable = [
        'すべてれいわ',  # 7文字
        'らく',          # 2文字
        'よろ',          # 2文字
        'もじ',          # 2文字
        'はる',          # 2文字（季節は一部でOK）
        'ふゆ',          # 2文字（季節は一部でOK）
    ]
    
    # 必要な文字の確保
    required_chars = {
        'れ': ['われ', 'これ', 'それ'],
        'わ': ['われ', 'わら', 'かわ'],
        'じ': ['じ', 'じかん', 'ふじ'],
        'ふ': ['ふく', 'ふる', 'ふ'],
    }
    
    # 複数の構成案を生成
    versions = []
    
    # Version 1: 極限削除版
    v1 = """ゆめをみた。なつうみへ。ひとぬのきて、ちる。
ねこ、えきでけんか。むし。ほし。
やまおり、とぶ。せげん。ものさく。
ゆきふる。はそら。じ。われ。"""
    
    # Version 2: さらに短縮
    v2 = """ゆめをみた。なつうみへ。ひとぬのきて。
ねこ、えきでけんか。むしとぶ。ほし。
やまおり、ちる。せげん。ものさく。
ゆきふ。はそら。じ。われ。"""
    
    # Version 3: 究極版
    v3 = """ゆめをみた。うみへ。ひとぬのきて。
ねこえきでけんか。むしとぶ。ほし。
やまおり、なつちる。せげん。ものさく。
ゆきふ。はそら。じ。われ。"""
    
    versions = [v1, v2, v3]
    
    return versions

def verify_pangram(text):
    """パングラムの検証"""
    hiragana = [c for c in text if c in HIRAGANA_BASE]
    used_chars = set(hiragana)
    missing = HIRAGANA_BASE - used_chars
    
    return {
        'is_pangram': len(missing) == 0,
        'char_count': len(hiragana),
        'missing_chars': missing,
        'used_chars': used_chars
    }

if __name__ == "__main__":
    print("=== 不要単語削除による極限圧縮 ===\n")
    
    # 現在のテキストを分析
    current = """ゆめをみた。はる。なつうみへ。あき、ちる。ふゆ。
ひとぬのきてやま、おり。ほし。ねこ、えきでけんか。
むし、とぶ。よろ、せげん。らく。もの、そらにさく。
すべてれいわ。ゆき、もじ。"""
    
    analysis = analyze_necessity(current)
    print("現在の構成分析:")
    for item in sorted(analysis, key=lambda x: x['efficiency']):
        print(f"  {item['segment']}: {item['length']}文字, 効率{item['efficiency']:.2f}")
    
    print("\n=== 最小構成版の生成 ===\n")
    
    versions = create_minimal_pangram()
    best_version = None
    best_count = float('inf')
    
    for i, version in enumerate(versions):
        result = verify_pangram(version)
        print(f"Version {i+1}:")
        print(f"  文字数: {result['char_count']}")
        print(f"  パングラム: {'✅' if result['is_pangram'] else '❌'}")
        if result['missing_chars']:
            print(f"  不足: {''.join(sorted(result['missing_chars']))}")
        
        if result['is_pangram'] and result['char_count'] < best_count:
            best_version = version
            best_count = result['char_count']
        print()
    
    if best_version:
        print(f"\n=== 最良結果: {best_count}文字 ===")
        print(best_version)