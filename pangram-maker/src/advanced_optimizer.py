#!/usr/bin/env python3
"""
高度な最適化アルゴリズム
句読点を除外した文字数カウントと革新的な最適化手法
"""

import random
import math
from collections import Counter
import itertools
import re

# ひらがな46文字
HIRAGANA = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

def count_hiragana_only(text):
    """ひらがなのみをカウント（句読点除外）"""
    return len([c for c in text if c in HIRAGANA])

def analyze_text_advanced(text):
    """高度なテキスト分析"""
    hiragana_only = [c for c in text if c in HIRAGANA]
    char_count = Counter(hiragana_only)
    
    return {
        'char_count': char_count,
        'hiragana_count': len(hiragana_only),
        'total_length': len(text),
        'unique_chars': len(char_count),
        'missing_chars': HIRAGANA - set(char_count.keys()),
        'max_duplication': max(char_count.values()) if char_count else 0,
        'duplication_score': sum(count - 1 for count in char_count.values() if count > 1),
        'punctuation_count': len(text) - len(hiragana_only)
    }

# 革新的な置換辞書
INNOVATIVE_REPLACEMENTS = {
    # 極限短縮
    'はるかぜふきさくらちる': ['春風桜', 'はるさく'],
    'なつうみへいく': ['夏海', 'なつみ'],
    'あきもみじめで': ['秋紅葉', 'あきは'],
    'ふゆゆきこんこん': ['冬雪', 'ふゆ'],
    
    # 人物の極限短縮
    'わかものとしより': ['人々', 'みな'],
    'ひとびと': ['人', 'みな'],
    'すべてのひと': ['みな', '皆'],
    
    # 動作の圧縮
    'ぬのきてやまへ': ['山行く', 'やまへ'],
    'ねこがなく': ['猫鳴く', 'ねこ'],
    'むしとぶ': ['虫飛ぶ', 'むし'],
    'えきでけんか': ['駅喧嘩', 'えき'],
    
    # 概念の革新的短縮
    'それぞれちがうよろこび': ['各喜び', 'よろこび'],
    'せけんにはある': ['世にある', 'ある'],
    'ひとがたのしさをもつ': ['楽しむ', 'たのし'],
    'すべてのいきもの': ['生き物', 'いきもの'],
    'おなじそらのした': ['空下', 'した'],
    
    # 文末表現
    'そらのした': ['下界', 'した'],
    'いきものおなじそらした': ['皆空下', 'みなした'],
}

# 文節単位の革新的パターン
INNOVATIVE_PATTERNS = [
    # 季節の圧縮表現
    "春風、夏海、秋葉、冬雪。",
    "四季巡り、",
    
    # 人物動作の圧縮
    "人々山へ。",
    "皆歩く。",
    
    # 場所と動作
    "駅、喧嘩。虫飛ぶ。",
    "猫鳴く、鳥飛ぶ。",
    
    # 抽象概念
    "喜び世に。",
    "皆楽し。",
]

class GeneticOptimizer:
    """遺伝的アルゴリズムによる最適化"""
    
    def __init__(self, population_size=50):
        self.population_size = population_size
        self.elite_size = 10
        self.mutation_rate = 0.2
        
    def create_individual(self, base_text):
        """個体の生成（ランダムな置換を適用）"""
        text = base_text
        num_replacements = random.randint(1, 5)
        
        for _ in range(num_replacements):
            patterns = [p for p in INNOVATIVE_REPLACEMENTS.keys() if p in text]
            if patterns:
                pattern = random.choice(patterns)
                replacement = random.choice(INNOVATIVE_REPLACEMENTS[pattern])
                text = text.replace(pattern, replacement, 1)
        
        return text
    
    def fitness(self, text):
        """適応度関数"""
        analysis = analyze_text_advanced(text)
        
        # ペナルティ計算
        penalty = 0
        
        # 不足文字は致命的
        penalty += len(analysis['missing_chars']) * 10000
        
        # ひらがな文字数（少ないほど良い）
        penalty += analysis['hiragana_count']
        
        # 重複ペナルティ
        penalty += analysis['duplication_score'] * 2
        
        # 意味の通らない文章へのペナルティ（簡易チェック）
        if len(text) < 50:  # 極端に短い
            penalty += 1000
        
        return -penalty  # 高いほど良い
    
    def crossover(self, parent1, parent2):
        """交叉：文節単位での組み換え"""
        # 句点で分割
        segments1 = parent1.split('。')
        segments2 = parent2.split('。')
        
        # ランダムに組み合わせ
        child_segments = []
        for i in range(max(len(segments1), len(segments2))):
            if i < len(segments1) and i < len(segments2):
                child_segments.append(random.choice([segments1[i], segments2[i]]))
            elif i < len(segments1):
                child_segments.append(segments1[i])
            else:
                child_segments.append(segments2[i])
        
        return '。'.join(child_segments)
    
    def mutate(self, text):
        """突然変異：ランダムな置換"""
        if random.random() < self.mutation_rate:
            return self.create_individual(text)
        return text
    
    def optimize(self, initial_texts, generations=100):
        """遺伝的アルゴリズムによる最適化"""
        # 初期集団の生成
        population = []
        for base in initial_texts:
            for _ in range(self.population_size // len(initial_texts)):
                population.append(self.create_individual(base))
        
        best_ever = None
        best_fitness = float('-inf')
        
        for gen in range(generations):
            # 適応度でソート
            population_fitness = [(ind, self.fitness(ind)) for ind in population]
            population_fitness.sort(key=lambda x: x[1], reverse=True)
            
            # エリート選択
            elites = [ind for ind, _ in population_fitness[:self.elite_size]]
            
            # 最良個体の更新
            if population_fitness[0][1] > best_fitness:
                best_ever = population_fitness[0][0]
                best_fitness = population_fitness[0][1]
                
                analysis = analyze_text_advanced(best_ever)
                if not analysis['missing_chars']:
                    print(f"\n世代{gen}: {analysis['hiragana_count']}文字")
                    print(f"テキスト: {best_ever[:50]}...")
            
            # 次世代の生成
            new_population = elites[:]
            
            while len(new_population) < self.population_size:
                # 親選択（トーナメント選択）
                parent1 = random.choice(elites)
                parent2 = random.choice(elites)
                
                # 交叉
                child = self.crossover(parent1, parent2)
                
                # 突然変異
                child = self.mutate(child)
                
                new_population.append(child)
            
            population = new_population
            
            if gen % 10 == 0:
                print(".", end="", flush=True)
        
        return best_ever

def revolutionary_optimization():
    """革新的な最適化の統合実行"""
    
    # ベーステキスト（既存の成果）
    base_texts = [
        # try04の102文字版（句読点込み）
        "かぜふくはなちる。うみへ。あきもみじめでふゆゆき。わかものとしよりぬのきてやまへ。ほしぞら。ねこなくえきでむしなく。それぞれちがうよろこびせけんに。ひとがたのしさをもつ。すべてのいきものおなじそらのした。",
        
        # try03の131文字版
        "はるかぜふきさくらちる。なつうみへいく。あきもみじめで、ふゆゆきこんこん。わかものとしより、ぬのきてやまへ。ほしぞらにつきでる。ねこがなく。えきでけんか、むしとぶ。それぞれちがうよろこび、せけんにはある。ひとがたのしさをもつ。すべてのいきもの、おなじそらのした。",
    ]
    
    print("=== 革新的パングラム最適化 ===\n")
    
    # 現状分析
    print("現在のベストを分析:")
    for i, text in enumerate(base_texts):
        analysis = analyze_text_advanced(text)
        print(f"\nテキスト{i+1}:")
        print(f"  総文字数: {analysis['total_length']}")
        print(f"  ひらがなのみ: {analysis['hiragana_count']}文字")
        print(f"  句読点: {analysis['punctuation_count']}文字")
        print(f"  不足: {''.join(sorted(analysis['missing_chars']))}")
    
    print("\n\n=== 遺伝的アルゴリズム開始 ===")
    
    # 遺伝的アルゴリズム
    genetic = GeneticOptimizer(population_size=100)
    best_genetic = genetic.optimize(base_texts, generations=200)
    
    print("\n\n=== 最終結果 ===")
    
    if best_genetic:
        final_analysis = analyze_text_advanced(best_genetic)
        print(f"\nテキスト: {best_genetic}")
        print(f"ひらがなのみ: {final_analysis['hiragana_count']}文字")
        print(f"総文字数: {final_analysis['total_length']}文字")
        print(f"不足文字: {''.join(sorted(final_analysis['missing_chars']))}")
        print(f"最大重複: {final_analysis['max_duplication']}回")
        
        return best_genetic
    
    return None

if __name__ == "__main__":
    result = revolutionary_optimization()
    
    if result:
        print("\n\n完全なテキスト:")
        print(result)