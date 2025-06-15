#!/usr/bin/env python3
"""
焼きなまし法によるパングラム最適化
重複の多い単語を置き換えて文字数を削減
"""

import random
import math
from collections import Counter
import copy

# ひらがな46文字
HIRAGANA = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

# 置換候補辞書（同じ意味や似た意味を持つ短い表現）
REPLACEMENTS = {
    # 季節関連
    'はるかぜふき': ['はるかぜ', 'かぜふく'],
    'さくらちる': ['さくら', 'はなちる'],
    'なつうみへいく': ['なつうみ', 'うみへ'],
    'あきもみじめで': ['もみじみ', 'あきのは'],
    'ふゆゆきこんこん': ['ゆきふる', 'ふゆゆき'],
    
    # 人物関連
    'わかものとしより': ['わかもの', 'ひとびと', 'みんな'],
    'ぬのきてやまへ': ['ぬのきて', 'やまいく'],
    
    # 場所・動作
    'ほしぞらにつきでる': ['つきでる', 'ほしぞら', 'よぞら'],
    'えきでけんか': ['えきで', 'けんか'],
    'むしとぶ': ['むしなく', 'とぶ'],
    
    # 抽象概念
    'それぞれちがうよろこび': ['よろこび', 'ちがいが'],
    'せけんにはある': ['せけんに', 'ある'],
    'ひとがたのしさをもつ': ['たのしむ', 'ひとみな'],
    'すべてのいきもの': ['いきもの', 'みんな'],
    'おなじそらのした': ['そらした', 'このよで'],
    
    # 単語レベルの置換
    'ねこがなく': ['ねこなく', 'ねこ'],
    'つきひかる': ['つきでる', 'ひかる'],
}

# 必須構造（これらは残す）
REQUIRED_PATTERNS = [
    'を',  # 助詞「を」は必須
    'ん',  # 語末の「ん」も必要
    'ぬの', # 「ぬ」を含む重要な単語
]

def analyze_text(text):
    """テキストの文字使用状況を分析"""
    hiragana_only = [c for c in text if c in HIRAGANA]
    char_count = Counter(hiragana_only)
    
    # 統計情報
    total_chars = sum(char_count.values())
    unique_chars = len(char_count)
    missing_chars = HIRAGANA - set(char_count.keys())
    max_duplication = max(char_count.values()) if char_count else 0
    
    # 重複スコア（重複が多いほど高い）
    duplication_score = sum(count - 1 for count in char_count.values() if count > 1)
    
    return {
        'char_count': char_count,
        'total_chars': total_chars,
        'unique_chars': unique_chars,
        'missing_chars': missing_chars,
        'max_duplication': max_duplication,
        'duplication_score': duplication_score,
        'text_length': len(text)
    }

def evaluate_pangram(text):
    """パングラムの評価値を計算（低いほど良い）"""
    analysis = analyze_text(text)
    
    # ペナルティ計算
    penalty = 0
    
    # 1. 文字数ペナルティ（100文字を超えると増加）
    if analysis['text_length'] > 100:
        penalty += (analysis['text_length'] - 100) * 10
    
    # 2. 不足文字ペナルティ（非常に重い）
    penalty += len(analysis['missing_chars']) * 1000
    
    # 3. 重複ペナルティ
    penalty += analysis['duplication_score'] * 5
    
    # 4. 最大重複ペナルティ
    if analysis['max_duplication'] > 5:
        penalty += (analysis['max_duplication'] - 5) * 20
    
    return penalty, analysis

def apply_replacement(text, pattern, replacement):
    """テキスト内のパターンを置換"""
    return text.replace(pattern, replacement)

def get_neighbor_solution(current_text):
    """近傍解を生成（ランダムに1つの置換を適用）"""
    # 置換可能なパターンを探す
    possible_replacements = []
    
    for pattern, replacements in REPLACEMENTS.items():
        if pattern in current_text:
            for replacement in replacements:
                # 置換後も必須パターンが残ることを確認
                test_text = current_text.replace(pattern, replacement)
                if all(req in test_text for req in REQUIRED_PATTERNS):
                    possible_replacements.append((pattern, replacement))
    
    if not possible_replacements:
        return current_text
    
    # ランダムに1つ選んで適用
    pattern, replacement = random.choice(possible_replacements)
    return apply_replacement(current_text, pattern, replacement)

def simulated_annealing(initial_text, max_iterations=10000, initial_temp=100.0, cooling_rate=0.995):
    """焼きなまし法によるパングラム最適化"""
    current_text = initial_text
    current_penalty, current_analysis = evaluate_pangram(current_text)
    
    best_text = current_text
    best_penalty = current_penalty
    best_analysis = current_analysis
    
    temperature = initial_temp
    
    print(f"初期状態:")
    print(f"文字数: {len(initial_text)}")
    print(f"ペナルティ: {current_penalty}")
    print(f"不足文字: {''.join(sorted(current_analysis['missing_chars']))}")
    print("-" * 60)
    
    for iteration in range(max_iterations):
        # 近傍解を生成
        neighbor_text = get_neighbor_solution(current_text)
        neighbor_penalty, neighbor_analysis = evaluate_pangram(neighbor_text)
        
        # 改善量を計算
        delta = neighbor_penalty - current_penalty
        
        # 受理判定
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current_text = neighbor_text
            current_penalty = neighbor_penalty
            current_analysis = neighbor_analysis
            
            # ベスト解の更新
            if current_penalty < best_penalty:
                best_text = current_text
                best_penalty = current_penalty
                best_analysis = current_analysis
                
                # 改善があったら表示
                if iteration % 100 == 0 or len(best_text) <= 100:
                    print(f"\n改善! (iteration {iteration})")
                    print(f"文字数: {len(best_text)}")
                    print(f"ペナルティ: {best_penalty}")
                    print(f"最大重複: {best_analysis['max_duplication']}")
                    if best_analysis['missing_chars']:
                        print(f"不足文字: {''.join(sorted(best_analysis['missing_chars']))}")
                    print(f"テキスト: {best_text}")
        
        # 温度を下げる
        temperature *= cooling_rate
        
        # 100文字達成したら詳細表示
        if len(best_text) <= 100 and not best_analysis['missing_chars']:
            print("\n★ 100文字以下のパングラム達成！")
            break
    
    return best_text, best_analysis

def incremental_optimization(initial_text, target_length=100):
    """段階的な最適化（複数回の焼きなまし）"""
    current_text = initial_text
    
    print("=== 段階的最適化開始 ===\n")
    
    for round_num in range(5):
        print(f"\n--- ラウンド {round_num + 1} ---")
        
        # 焼きなましを実行
        optimized_text, analysis = simulated_annealing(
            current_text,
            max_iterations=5000,
            initial_temp=50.0 * (0.8 ** round_num),  # 徐々に温度を下げる
            cooling_rate=0.998
        )
        
        # 結果を更新
        current_text = optimized_text
        
        # 目標達成したら終了
        if len(current_text) <= target_length and not analysis['missing_chars']:
            print(f"\n目標達成！ {len(current_text)}文字のパングラム")
            break
    
    return current_text, analysis

if __name__ == "__main__":
    # try03の最良版（131文字）をベースに最適化
    base_text = """はるかぜふきさくらちる。なつうみへいく。あきもみじめで、ふゆゆきこんこん。わかものとしより、ぬのきてやまへ。ほしぞらにつきでる。ねこがなく。えきでけんか、むしとぶ。それぞれちがうよろこび、せけんにはある。ひとがたのしさをもつ。すべてのいきもの、おなじそらのした。"""
    
    # 句読点なし版（125文字）も試す
    base_text_no_punct = """はるかぜふきさくらちる。なつうみへいく。あきもみじめでふゆゆきこんこん。わかものとしよりぬのきてやまへ。ほしぞらにつきでる。ねこがなくえきでけんかむしとぶ。それぞれちがうよろこびせけんにはある。ひとがたのしさをもつ。すべてのいきものおなじそらのした。"""
    
    print("基準テキスト分析:")
    base_analysis = analyze_text(base_text)
    print(f"文字数: {len(base_text)}")
    print(f"最大重複: {base_analysis['max_duplication']}")
    print(f"重複スコア: {base_analysis['duplication_score']}")
    
    # 重複の多い文字を表示
    print("\n重複の多い文字:")
    for char, count in sorted(base_analysis['char_count'].items(), key=lambda x: x[1], reverse=True)[:10]:
        if count > 2:
            print(f"  {char}: {count}回")
    
    print("\n" + "="*60 + "\n")
    
    # 最適化実行
    final_text, final_analysis = incremental_optimization(base_text_no_punct, target_length=100)
    
    print("\n\n=== 最終結果 ===")
    print(f"最終テキスト: {final_text}")
    print(f"文字数: {len(final_text)}")
    print(f"最大重複: {final_analysis['max_duplication']}")
    print(f"不足文字: {''.join(sorted(final_analysis['missing_chars']))}")
    
    # 文字使用頻度
    print("\n文字使用頻度（上位10文字）:")
    for char, count in sorted(final_analysis['char_count'].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {char}: {count}回")