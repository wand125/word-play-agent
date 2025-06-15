#!/usr/bin/env python3
"""
濁音活用による最適化
清音の重複を濁音で置き換えて文字数削減
"""

import random
from collections import Counter

# 基本ひらがな46文字
HIRAGANA_BASE = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

# 濁音・半濁音を含む全ひらがな
HIRAGANA_ALL = set('あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゆよらりるれろわをん')

# 濁音→清音の変換マップ
DAKUTEN_TO_SEION = {
    'が': 'か', 'ぎ': 'き', 'ぐ': 'く', 'げ': 'け', 'ご': 'こ',
    'ざ': 'さ', 'じ': 'し', 'ず': 'す', 'ぜ': 'せ', 'ぞ': 'そ',
    'だ': 'た', 'ぢ': 'ち', 'づ': 'つ', 'で': 'て', 'ど': 'と',
    'ば': 'は', 'び': 'ひ', 'ぶ': 'ふ', 'べ': 'へ', 'ぼ': 'ほ',
    'ぱ': 'は', 'ぴ': 'ひ', 'ぷ': 'ふ', 'ぺ': 'へ', 'ぽ': 'ほ'
}

def normalize_to_seion(text):
    """テキストを清音に正規化"""
    normalized = []
    for char in text:
        if char in DAKUTEN_TO_SEION:
            normalized.append(DAKUTEN_TO_SEION[char])
        elif char in HIRAGANA_BASE:
            normalized.append(char)
    return ''.join(normalized)

def analyze_with_dakuten(text):
    """濁音を考慮した分析"""
    # 全ひらがなを抽出
    all_hiragana = [c for c in text if c in HIRAGANA_ALL]
    
    # 清音に正規化
    normalized = normalize_to_seion(text)
    seion_chars = [c for c in normalized if c in HIRAGANA_BASE]
    seion_count = Counter(seion_chars)
    
    # 濁音の使用状況
    dakuten_chars = [c for c in all_hiragana if c in DAKUTEN_TO_SEION]
    
    return {
        'total_hiragana': len(all_hiragana),
        'dakuten_count': len(dakuten_chars),
        'seion_count': seion_count,
        'seion_coverage': len(seion_count),
        'missing_seion': HIRAGANA_BASE - set(seion_count.keys()),
        'max_seion_duplication': max(seion_count.values()) if seion_count else 0,
        'total_length': len(text)
    }

# 自然な濁音置換パターン
NATURAL_DAKUTEN_PATTERNS = {
    # 助詞の濁音化
    'かぜふく': ['かぜがふく', 'かぜふく'],
    'むしとぶ': ['むしがとぶ', 'むしとぶ'],
    'ねこなく': ['ねこがなく', 'ねこなく'],
    'あきもみじ': ['あきのもみじ', 'あきもみじ'],
    'はるかぜ': ['はるのかぜ', 'はるかぜ'],
    
    # 自然な濁音語
    'ほしぞら': ['ほしぞら', 'ほしそら'],
    'いきもの': ['いきもの', 'いきもの'],
    'よろこび': ['よろこび', 'よろこひ'],
    
    # 動詞の濁音形
    'さくらちる': ['さくらちる', 'さくらがちる'],
    'ゆきふる': ['ゆきがふる', 'ゆきふる'],
    
    # 複合語の濁音
    'すべて': ['すべて', 'すへて'],
    'せけん': ['せけん', 'せげん'],
}

def optimize_with_dakuten(base_text):
    """濁音を活用した最適化"""
    current_text = base_text
    best_text = base_text
    best_score = float('inf')
    
    # 現状分析
    initial_analysis = analyze_with_dakuten(base_text)
    print(f"初期状態:")
    print(f"  総ひらがな: {initial_analysis['total_hiragana']}")
    print(f"  濁音使用: {initial_analysis['dakuten_count']}")
    print(f"  清音カバー: {initial_analysis['seion_coverage']}/46")
    print(f"  最大重複: {initial_analysis['max_seion_duplication']}")
    
    # 最適化ループ
    for iteration in range(1000):
        # ランダムに置換を試みる
        for pattern, replacements in NATURAL_DAKUTEN_PATTERNS.items():
            if pattern in current_text and len(replacements) > 1:
                # 濁音版を優先的に選択
                if random.random() < 0.7:  # 70%の確率で濁音版
                    replacement = replacements[0]  # 通常は濁音版が最初
                else:
                    replacement = replacements[1]
                
                new_text = current_text.replace(pattern, replacement, 1)
                analysis = analyze_with_dakuten(new_text)
                
                # スコア計算（総文字数 + 清音重複ペナルティ）
                score = analysis['total_hiragana'] + analysis['max_seion_duplication'] * 5
                
                # 不足文字があれば大きなペナルティ
                if analysis['missing_seion']:
                    score += 1000
                
                if score < best_score:
                    best_text = new_text
                    best_score = score
                    current_text = new_text
                    
                    if iteration % 100 == 0:
                        print(f"\n改善 (iteration {iteration}):")
                        print(f"  総ひらがな: {analysis['total_hiragana']}")
                        print(f"  濁音使用: {analysis['dakuten_count']}")
                        print(f"  最大重複: {analysis['max_seion_duplication']}")
    
    return best_text

def create_dakuten_optimized():
    """濁音最適化パングラムの作成"""
    
    # ベーステキスト（try05の成果）
    base_text = """ゆめをみた。はるかぜ、さくらちる。なつうみへ。あきもみじ、ふゆゆき。ひとびとぬのきてやまにおり。ほしぞら。ねこなく、えきでけんか。むしとぶ。よろこびせけん。たのしさもつ。いきもの、そらした。すべてれいわ。"""
    
    print("=== 濁音活用最適化 ===\n")
    
    # 手動で作成した改善版
    manual_versions = [
        # 助詞「が」の活用
        "ゆめをみた。はるかぜがふく、さくらちる。なつうみへ。あきがきて、もみじ。ふゆにゆき。ひとびと、ぬのきてやまへ。ほしぞら。ねこがなく、えきでけんか。むしがとぶ。よろこび、せけんにある。たのしさもつ。いきもの、そらのした。すべてれいわ。",
        
        # 濁音語の活用
        "ゆめをみた。かぜがさくらちらす。なつうみへ。あきもみじ、ふゆゆき。ひとびと、ぬのきてやまへ。ほしぞら。ねこなく、えきでけんか。むしとぶ。よろこびがせけんにある。たのしさもつ。いきもの、そらのした。すべてれいわ。",
        
        # 更なる濁音化
        "ゆめをみた。かぜ、さくらちる。なつうみへ。あきもみじ、ふゆゆき。ひとびと、ぬのぎてやまへ。ほしぞら。ねこなく、えぎでけんか。むしとぶ。よろこび、せげんにある。たのしさもつ。いぎもの、そらした。すべてれいわ。",
    ]
    
    best_result = None
    best_analysis = None
    best_hiragana_count = float('inf')
    
    # 各バージョンを評価
    for i, text in enumerate(manual_versions):
        print(f"\n手動版{i+1}:")
        analysis = analyze_with_dakuten(text)
        print(f"  総ひらがな: {analysis['total_hiragana']}")
        print(f"  濁音使用: {analysis['dakuten_count']}")
        print(f"  清音カバー: {analysis['seion_coverage']}/46")
        print(f"  不足: {''.join(sorted(analysis['missing_seion']))}")
        print(f"  最大重複: {analysis['max_seion_duplication']}")
        
        if not analysis['missing_seion'] and analysis['total_hiragana'] < best_hiragana_count:
            best_result = text
            best_analysis = analysis
            best_hiragana_count = analysis['total_hiragana']
    
    # アルゴリズムによる最適化も試す
    print("\n\n=== アルゴリズム最適化 ===")
    algo_result = optimize_with_dakuten(base_text)
    algo_analysis = analyze_with_dakuten(algo_result)
    
    if not algo_analysis['missing_seion'] and algo_analysis['total_hiragana'] < best_hiragana_count:
        best_result = algo_result
        best_analysis = algo_analysis
    
    return best_result, best_analysis

if __name__ == "__main__":
    final_text, final_analysis = create_dakuten_optimized()
    
    if final_text:
        print("\n\n=== 最終結果 ===")
        print(f"テキスト: {final_text}")
        print(f"\n分析結果:")
        print(f"  総ひらがな: {final_analysis['total_hiragana']}文字")
        print(f"  濁音使用: {final_analysis['dakuten_count']}文字")
        print(f"  清音カバー: {final_analysis['seion_coverage']}/46")
        print(f"  最大重複（清音）: {final_analysis['max_seion_duplication']}回")
        
        # 詳細な文字使用状況
        print(f"\n清音使用頻度（上位）:")
        for char, count in sorted(final_analysis['seion_count'].items(), 
                                 key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {char}: {count}回")