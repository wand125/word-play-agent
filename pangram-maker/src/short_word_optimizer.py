#!/usr/bin/env python3
"""
短単語最適化エンジン
より短い単語への置換による極限短縮
"""

from collections import Counter
import re

# ひらがな46文字
HIRAGANA_BASE = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')
HIRAGANA_ALL = set('あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゆよらりるれろわをん')

# 短縮辞書（長い表現→短い表現）
SHORTENING_DICT = {
    # 季節関連
    'はるかぜ': ['かぜ', 'はる'],
    'さくらちる': ['さく', 'ちる', 'はな'],
    'なつうみへいく': ['うみへ', 'なつへ'],
    'なつうみへ': ['うみへ', 'なつ'],
    'あきもみじめで': ['もみじ', 'あき'],
    'あきもみじ': ['もみじ', 'あき'],
    'ふゆゆきこんこん': ['ゆき', 'ふゆ'],
    'ふゆゆき': ['ゆき', 'ふゆ'],
    
    # 人・動物
    'ひとびと': ['ひと', 'みな'],
    'わかものとしより': ['ひと', 'みな'],
    'ねこがなく': ['ねこ'],
    'ねこなく': ['ねこ'],
    'むしとぶ': ['むし', 'とぶ'],
    'むしがとぶ': ['むし'],
    
    # 場所・動作
    'ぬのきてやまへ': ['やまへ', 'ぬのきて'],
    'ぬのきてやま': ['やま', 'ぬの'],
    'やまにおり': ['やまへ', 'やま'],
    'ほしぞら': ['ほし', 'そら'],
    'えきでけんか': ['えき', 'けんか'],
    
    # 感情・概念
    'よろこびせけん': ['よろこび', 'よろ'],
    'よろこび': ['よろ', 'うれし'],
    'たのしさもつ': ['たのし', 'たの'],
    'たのしさ': ['たの', 'らく'],
    'すべてのいきもの': ['いきもの', 'もの'],
    'いきもの': ['もの', 'いき'],
    'すべてれいわ': ['すれいわ', 'れいわ'],
    'そらのした': ['した', 'そら'],
    'そらした': ['した', 'そら'],
    
    # 文末表現
    'をみた': ['みた'],
    'にある': ['ある'],
    'せけんに': ['せけん'],
}

def analyze_text(text):
    """テキスト分析"""
    all_hiragana = [c for c in text if c in HIRAGANA_ALL]
    base_hiragana = [c for c in text if c in HIRAGANA_BASE]
    
    # 濁音を清音に変換してカウント
    normalized = []
    for c in text:
        if c in 'がぎぐげござじずぜぞだぢづでどばびぶべぼ':
            # 濁音を清音に
            mapping = {'が':'か', 'ぎ':'き', 'ぐ':'く', 'げ':'け', 'ご':'こ',
                      'ざ':'さ', 'じ':'し', 'ず':'す', 'ぜ':'せ', 'ぞ':'そ',
                      'だ':'た', 'ぢ':'ち', 'づ':'つ', 'で':'て', 'ど':'と',
                      'ば':'は', 'び':'ひ', 'ぶ':'ふ', 'べ':'へ', 'ぼ':'ほ'}
            normalized.append(mapping.get(c, c))
        elif c in 'ぱぴぷぺぽ':
            # 半濁音を清音に
            mapping = {'ぱ':'は', 'ぴ':'ひ', 'ぷ':'ふ', 'ぺ':'へ', 'ぽ':'ほ'}
            normalized.append(mapping.get(c, c))
        elif c in HIRAGANA_BASE:
            normalized.append(c)
    
    seion_count = Counter(normalized)
    missing = HIRAGANA_BASE - set(seion_count.keys())
    
    return {
        'total_hiragana': len(all_hiragana),
        'base_hiragana': len(base_hiragana),
        'missing_chars': missing,
        'char_count': seion_count,
        'total_length': len(text)
    }

def find_shortest_replacements(text):
    """最短の置換を見つける"""
    replacements = []
    
    # ソート済みの置換候補（長い順）
    sorted_patterns = sorted(SHORTENING_DICT.keys(), key=len, reverse=True)
    
    for pattern in sorted_patterns:
        if pattern in text:
            candidates = SHORTENING_DICT[pattern]
            # 最短の候補を選択
            shortest = min(candidates, key=len)
            if len(shortest) < len(pattern):
                replacements.append((pattern, shortest, len(pattern) - len(shortest)))
    
    return sorted(replacements, key=lambda x: x[2], reverse=True)

def apply_replacements(text, replacements):
    """置換を適用"""
    result = text
    for pattern, replacement, _ in replacements:
        result = result.replace(pattern, replacement, 1)
    return result

def create_ultra_short():
    """超短縮パングラム作成"""
    
    # ベーステキスト
    base = "ゆめをみた。はるかぜ、さくらちる。なつうみへ。あきもみじ、ふゆゆき。ひとびとぬのきてやまにおり。ほしぞら。ねこなく、えきでけんか。むしとぶ。よろこびせけん。たのしさもつ。いきもの、そらした。すべてれいわ。"
    
    print("=== 短単語最適化 ===\n")
    print(f"ベース: {len([c for c in base if c in HIRAGANA_ALL])}文字")
    
    # 手動最適化版
    manual_versions = [
        # Version 1: 基本短縮
        "ゆめみた。はる、さく。なつ、うみへ。あき、もみじ。ふゆ、ゆき。ひと、ぬのきてやまへ。ほしぞら。ねこ、えきでけんか。むしとぶ。よろこび、せけん。たのし。もの、そらした。すれいわ。",
        
        # Version 2: さらに短縮
        "ゆめをみた。はる、さく。うみへ。あき、もみじ。ふゆ、ゆき。ひと、ぬのきてやま。ほし。ねこ、えきでけんか。むしとぶ。よろこび。たの。もの、そらした。すれいわ。なつぞら、せけん。",
        
        # Version 3: 極限短縮
        "ゆめをみた。はるさく。なつうみへ。あきもみじ。ふゆゆき。ひと、ぬのきてやま。ほしぞら。ねこ、えきでけんか。むしとぶ。よろこび。たの。いきもの、そらした。すれいわ。せけん。",
        
        # Version 4: 文構造も変更
        "ゆめをみた。はるさく。なつうみへ。あきもみじ。ふゆゆき。ひとぬのきてやま。ほしぞら。ねこえきでけんか。むしとぶ。よろこびせけん。たのし。いきものそらした。すべてれいわ。",
    ]
    
    best_text = None
    best_count = float('inf')
    
    for i, text in enumerate(manual_versions):
        analysis = analyze_text(text)
        print(f"\nVersion {i+1}:")
        print(f"  文字数: {analysis['total_hiragana']}")
        print(f"  不足: {''.join(sorted(analysis['missing_chars']))}")
        
        if not analysis['missing_chars'] and analysis['total_hiragana'] < best_count:
            best_text = text
            best_count = analysis['total_hiragana']
    
    # アルゴリズムによる最適化
    print("\n\n=== アルゴリズム最適化 ===")
    
    # 置換候補を見つける
    replacements = find_shortest_replacements(base)
    print("\n置換候補:")
    for pattern, replacement, saving in replacements[:10]:
        print(f"  {pattern} → {replacement} (-{saving}文字)")
    
    # 段階的に適用
    current = base
    for i in range(5):
        replacements = find_shortest_replacements(current)
        if replacements:
            # 最大の削減効果がある置換を適用
            pattern, replacement, _ = replacements[0]
            current = current.replace(pattern, replacement, 1)
            
            analysis = analyze_text(current)
            print(f"\nStep {i+1}: {pattern} → {replacement}")
            print(f"  文字数: {analysis['total_hiragana']}")
            print(f"  不足: {''.join(sorted(analysis['missing_chars']))}")
    
    if not analysis['missing_chars'] and analysis['total_hiragana'] < best_count:
        best_text = current
        best_count = analysis['total_hiragana']
    
    return best_text, best_count

if __name__ == "__main__":
    result_text, result_count = create_ultra_short()
    
    if result_text:
        print(f"\n\n=== 最良結果 ===")
        print(f"文字数: {result_count}文字")
        print(f"テキスト:\n{result_text}")
        
        # 詳細分析
        final_analysis = analyze_text(result_text)
        print(f"\n文字使用頻度（上位）:")
        for char, count in sorted(final_analysis['char_count'].items(), 
                                 key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {char}: {count}回")