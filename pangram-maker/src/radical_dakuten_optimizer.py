#!/usr/bin/env python3
"""
革新的濁音最適化
清音と濁音の完全互換性を活用した究極の短縮
"""

from collections import Counter
import itertools

# 基本ひらがな46文字
HIRAGANA_BASE = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

# 濁音・半濁音を含む全ひらがな
HIRAGANA_ALL = set('あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゆよらりるれろわをん')

# 清音→濁音の変換マップ（積極活用用）
SEION_TO_DAKUTEN = {
    'か': 'が', 'き': 'ぎ', 'く': 'ぐ', 'け': 'げ', 'こ': 'ご',
    'さ': 'ざ', 'し': 'じ', 'す': 'ず', 'せ': 'ぜ', 'そ': 'ぞ',
    'た': 'だ', 'ち': 'ぢ', 'つ': 'づ', 'て': 'で', 'と': 'ど',
    'は': 'ば', 'ひ': 'び', 'ふ': 'ぶ', 'へ': 'べ', 'ほ': 'ぼ'
}

# 濁音→清音
DAKUTEN_TO_SEION = {v: k for k, v in SEION_TO_DAKUTEN.items()}
DAKUTEN_TO_SEION.update({
    'ぱ': 'は', 'ぴ': 'ひ', 'ぷ': 'ふ', 'ぺ': 'へ', 'ぽ': 'ほ'
})

def normalize_to_seion(text):
    """清音に正規化"""
    normalized = []
    for char in text:
        if char in DAKUTEN_TO_SEION:
            normalized.append(DAKUTEN_TO_SEION[char])
        elif char in HIRAGANA_BASE:
            normalized.append(char)
    return normalized

def analyze_radical(text):
    """詳細分析"""
    all_hiragana = [c for c in text if c in HIRAGANA_ALL]
    seion_chars = normalize_to_seion(text)
    seion_count = Counter(seion_chars)
    
    return {
        'total_hiragana': len(all_hiragana),
        'seion_coverage': len(seion_count),
        'missing_seion': HIRAGANA_BASE - set(seion_count.keys()),
        'seion_count': seion_count,
        'max_duplication': max(seion_count.values()) if seion_count else 0
    }

def find_optimal_replacements(text):
    """最適な濁音置換を見つける"""
    analysis = analyze_radical(text)
    
    # 重複の多い清音を特定
    high_duplicates = [(char, count) for char, count in analysis['seion_count'].items() 
                      if count > 2 and char in SEION_TO_DAKUTEN]
    
    replacements = []
    for char, count in sorted(high_duplicates, key=lambda x: x[1], reverse=True):
        dakuten = SEION_TO_DAKUTEN[char]
        # テキスト中のその文字の位置を探す
        positions = []
        for i, c in enumerate(text):
            if c == char:
                positions.append(i)
        
        # 半分程度を濁音に置換する提案
        replace_count = count // 2
        if replace_count > 0:
            replacements.append((char, dakuten, replace_count))
    
    return replacements

def create_ultra_short_pangram():
    """究極の短縮パングラム作成"""
    
    # ベーステキスト
    base = "ゆめをみた。はるかぜ、さくらちる。なつうみへ。あきもみじ、ふゆゆき。ひとびとぬのきてやまにおり。ほしぞら。ねこなく、えきでけんか。むしとぶ。よろこびせけん。たのしさもつ。いきもの、そらした。すべてれいわ。"
    
    print("=== 革新的濁音最適化 ===\n")
    print(f"ベース: {len([c for c in base if c in HIRAGANA_ALL])}文字")
    
    # 手動最適化版
    versions = [
        # Version 1: 重複の多い文字を濁音化
        "ゆめをみだ。はるがぜ、さくらちる。なつうみへ。あぎもみじ、ふゆゆぎ。ひとびと、ぬのきてやまにおり。ほしぞら。ねごなく、えきでけんが。むしとぶ。よろごびせげん。たのしさもつ。いきもの、そらした。すべてれいわ。",
        
        # Version 2: さらに積極的
        "ゆめをみだ。はるがぜ、ざくらちる。なづうみへ。あぎもみじ、ふゆゆぎ。ひどびと、ぬのぎてやまにおり。ほじぞら。ねごなく、えぎでげんか。むじとぶ。よろごびぜけん。だのしさもつ。いぎもの、ぞらした。ずべてれいわ。",
        
        # Version 3: 文を短縮しつつ濁音活用
        "ゆめをみだ。がぜ、さくらちる。なづうみへ。あぎもみじ、ふゆゆぎ。ひと、ぬのぎてやまへ。ほじぞら。ねご、えぎでげんか。むじとぶ。よろごび、ぜげん。だのしさ。いぎもの、ぞらした。ずべてれいわ。",
        
        # Version 4: 極限短縮
        "ゆめをみだ。がぜふく、さくらちる。なづうみへ。あぎもみじ、ふゆ。ひと、ぬのぎてやまへ。ほじぞら。ねご、えぎでげんか。むじとぶ。よろごびある。だのしさ。いぎもの、ぞらした。ずべてれいわ。"
    ]
    
    best_text = None
    best_count = float('inf')
    
    for i, text in enumerate(versions):
        analysis = analyze_radical(text)
        hiragana_count = analysis['total_hiragana']
        
        print(f"\nVersion {i+1}:")
        print(f"  文字数: {hiragana_count}")
        print(f"  清音カバー: {analysis['seion_coverage']}/46")
        
        if analysis['missing_seion']:
            print(f"  不足: {''.join(sorted(analysis['missing_seion']))}")
        else:
            print("  ✓ 完全なパングラム")
            
        print(f"  最大重複: {analysis['max_duplication']}")
        
        if not analysis['missing_seion'] and hiragana_count < best_count:
            best_text = text
            best_count = hiragana_count
    
    # 最短版を手動で作成
    print("\n\n=== 極限短縮版 ===")
    
    extreme_versions = [
        # 文を極限まで短く
        "ゆめをみだ。がぜ、さくらちる。うみへ。もみじ、ゆぎ。ひと、ぬのぎてやまへ。ほじぞら。ねご、えぎでげんか。むじとぶ。よろごび。だのしさ。いぎもの、ぞらした。ずべてれいわ。なつあき、ふゆ。",
        
        # 別アプローチ
        "ゆめをみた。がぜ、はなちる。うみへ。もみじ、ゆぎ。ひと、ぬのぎてやま。ほじぞら。ねご、えぎでげんか。むじとぶ。よろごび、せけん。だのしさ。いぎもの、そらした。ずべてれいわ。なづあぎ、ふゆ。",
    ]
    
    for i, text in enumerate(extreme_versions):
        analysis = analyze_radical(text)
        print(f"\n極限版{i+1}:")
        print(f"  文字数: {analysis['total_hiragana']}")
        print(f"  不足: {''.join(sorted(analysis['missing_seion']))}")
        
        if not analysis['missing_seion'] and analysis['total_hiragana'] < best_count:
            best_text = text
            best_count = analysis['total_hiragana']
    
    return best_text, best_count

if __name__ == "__main__":
    result_text, result_count = create_ultra_short_pangram()
    
    if result_text:
        print(f"\n\n=== 最良結果 ===")
        print(f"文字数: {result_count}文字")
        print(f"テキスト:\n{result_text}")
        
        # 詳細分析
        final_analysis = analyze_radical(result_text)
        print(f"\n清音使用頻度:")
        for char, count in sorted(final_analysis['seion_count'].items(), 
                                 key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {char}: {count}回")