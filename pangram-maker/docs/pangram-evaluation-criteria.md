# パングラムの評価基準

## 目次
1. [評価の重要性](#評価の重要性)
2. [主要な評価基準](#主要な評価基準)
3. [評価スコアリングシステム](#評価スコアリングシステム)
4. [言語別の評価特性](#言語別の評価特性)
5. [評価ツールの実装](#評価ツールの実装)

## 評価の重要性

パングラムの品質を客観的に評価することは、以下の理由から重要です：

1. **比較可能性**：異なるパングラムを公平に比較
2. **改善の指針**：どの側面を改善すべきか明確化
3. **用途適合性**：特定の用途に最適なパングラムの選択
4. **自動生成の最適化**：アルゴリズムの改善目標設定

## 主要な評価基準

### 1. 文字数（Length）

最も基本的な評価基準。短いほど優れているとされる。

#### 評価方法
- **総文字数**：スペースを含む/含まない
- **単語数**：文章の複雑さの指標
- **完全性**：すべての必要文字を含んでいるか

#### スコアリング例
```python
def length_score(pangram, target_chars):
    # 基本スコア（短いほど高得点）
    base_length = len(target_chars)
    actual_length = len(pangram.replace(' ', ''))
    
    if actual_length == base_length:
        return 100  # 完全パングラム
    else:
        return max(0, 100 - (actual_length - base_length) * 2)
```

### 2. 自然さ（Naturalness）

文章として自然で意味が通るかどうか。

#### 評価要素
- **文法的正確性**：文法規則への準拠
- **意味的一貫性**：文章の意味が通るか
- **流暢性**：読みやすさ、リズム
- **一般性**：日常的に使われる表現か

#### 評価方法
```python
def naturalness_score(pangram, language_model):
    # 言語モデルによる確率計算
    probability = language_model.sentence_probability(pangram)
    
    # n-gramスコア
    ngram_score = calculate_ngram_score(pangram)
    
    # 品詞パターンの自然さ
    pos_pattern_score = evaluate_pos_pattern(pangram)
    
    return (probability * 0.5 + 
            ngram_score * 0.3 + 
            pos_pattern_score * 0.2) * 100
```

### 3. 記憶しやすさ（Memorability）

タイピング練習などで使用する場合に重要。

#### 評価要素
- **リズム**：音節のパターン
- **韻律**：韻を踏んでいるか
- **イメージ性**：視覚的にイメージしやすいか
- **ストーリー性**：物語として成立しているか

### 4. 文字分布（Character Distribution）

各文字の使用回数のバランス。

#### 評価方法
```python
def distribution_score(pangram):
    char_counts = Counter(pangram.lower())
    
    # 各文字の出現回数の標準偏差
    counts = list(char_counts.values())
    mean_count = np.mean(counts)
    std_dev = np.std(counts)
    
    # 標準偏差が小さいほど高得点
    return max(0, 100 - std_dev * 10)
```

### 5. 実用性（Practicality）

特定の用途における使いやすさ。

#### 用途別評価
- **タイピング練習**：頻出キーの組み合わせ
- **フォント表示**：文字の視認性
- **暗記教材**：教育的価値

## 評価スコアリングシステム

### 総合スコアの計算

```python
class PangramEvaluator:
    def __init__(self, weights=None):
        self.weights = weights or {
            'length': 0.3,
            'naturalness': 0.3,
            'memorability': 0.2,
            'distribution': 0.1,
            'practicality': 0.1
        }
    
    def evaluate(self, pangram, target_chars):
        scores = {
            'length': self.length_score(pangram, target_chars),
            'naturalness': self.naturalness_score(pangram),
            'memorability': self.memorability_score(pangram),
            'distribution': self.distribution_score(pangram),
            'practicality': self.practicality_score(pangram)
        }
        
        # 重み付き平均
        total_score = sum(
            scores[criterion] * self.weights[criterion]
            for criterion in scores
        )
        
        return {
            'total': total_score,
            'breakdown': scores,
            'grade': self.get_grade(total_score)
        }
    
    def get_grade(self, score):
        if score >= 90:
            return 'S'  # 優秀
        elif score >= 80:
            return 'A'  # 優良
        elif score >= 70:
            return 'B'  # 良好
        elif score >= 60:
            return 'C'  # 可
        else:
            return 'D'  # 要改善
```

### 用途別重み付け

```python
# タイピング練習用
typing_weights = {
    'length': 0.2,
    'naturalness': 0.2,
    'memorability': 0.3,
    'distribution': 0.1,
    'practicality': 0.2
}

# フォント表示用
font_weights = {
    'length': 0.4,
    'naturalness': 0.1,
    'memorability': 0.1,
    'distribution': 0.3,
    'practicality': 0.1
}

# 教育用
education_weights = {
    'length': 0.1,
    'naturalness': 0.4,
    'memorability': 0.3,
    'distribution': 0.1,
    'practicality': 0.1
}
```

## 言語別の評価特性

### 英語パングラムの評価

#### 特有の評価項目
1. **母音バランス**：a, e, i, o, u の分布
2. **頻出文字ペア**：th, er, on, an など
3. **単語の一般性**：辞書での使用頻度

#### 評価例
```
"The quick brown fox jumps over the lazy dog"
- 長さスコア: 65/100（35文字）
- 自然さスコア: 95/100（文法的に完璧）
- 記憶しやすさ: 90/100（視覚的イメージ豊富）
- 総合評価: A（優良）
```

### 日本語パングラムの評価

#### 特有の評価項目
1. **かな使いの自然さ**：現代仮名遣いへの準拠
2. **音の響き**：日本語としての音韻的美しさ
3. **漢字の使用**：適切な漢字かな混じり文
4. **文体の統一**：敬語レベルの一貫性

#### 評価例
```
いろは歌
- 長さスコア: 100/100（完全パングラム）
- 自然さスコア: 70/100（古語のため現代では不自然）
- 記憶しやすさ: 85/100（七五調のリズム）
- 文化的価値: 100/100（歴史的重要性）
- 総合評価: S（優秀）※歴史的価値を考慮
```

### 評価の可視化

```python
import matplotlib.pyplot as plt
import numpy as np

def visualize_pangram_scores(pangram_scores):
    """レーダーチャートで評価を可視化"""
    categories = list(pangram_scores['breakdown'].keys())
    values = list(pangram_scores['breakdown'].values())
    
    # 角度を計算
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    
    # プロット
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 100)
    ax.set_title(f"Pangram Evaluation (Total: {pangram_scores['total']:.1f})")
    
    return fig
```

## 評価ツールの実装

### 完全な評価システム

```python
class ComprehensivePangramEvaluator:
    def __init__(self, language='en'):
        self.language = language
        self.load_language_resources()
    
    def load_language_resources(self):
        """言語固有のリソースを読み込み"""
        if self.language == 'en':
            self.target_chars = set('abcdefghijklmnopqrstuvwxyz')
            self.load_english_resources()
        elif self.language == 'ja':
            self.target_chars = set('あいうえお...')  # 全ひらがな
            self.load_japanese_resources()
    
    def comprehensive_evaluation(self, pangram):
        """包括的な評価を実施"""
        results = {
            'pangram': pangram,
            'is_valid': self.validate_pangram(pangram),
            'scores': self.calculate_all_scores(pangram),
            'suggestions': self.generate_suggestions(pangram),
            'comparison': self.compare_with_benchmarks(pangram)
        }
        
        return results
    
    def validate_pangram(self, pangram):
        """パングラムの妥当性を検証"""
        pangram_chars = set(pangram.lower())
        missing_chars = self.target_chars - pangram_chars
        
        return {
            'is_complete': len(missing_chars) == 0,
            'missing_chars': list(missing_chars),
            'extra_chars': list(pangram_chars - self.target_chars),
            'is_perfect': self.is_perfect_pangram(pangram)
        }
    
    def is_perfect_pangram(self, pangram):
        """完全パングラムかどうかを判定"""
        char_counts = Counter(pangram.lower())
        return all(
            char_counts.get(char, 0) == 1 
            for char in self.target_chars
        )
    
    def generate_suggestions(self, pangram):
        """改善提案を生成"""
        suggestions = []
        
        # 長さの改善
        if len(pangram) > len(self.target_chars) * 1.5:
            suggestions.append("文章が長すぎます。より簡潔な表現を検討してください。")
        
        # 文字分布の改善
        char_counts = Counter(pangram.lower())
        max_count = max(char_counts.values())
        if max_count > 3:
            frequent_chars = [
                char for char, count in char_counts.items() 
                if count == max_count
            ]
            suggestions.append(
                f"文字 {', '.join(frequent_chars)} の使用頻度が高すぎます。"
            )
        
        return suggestions
    
    def compare_with_benchmarks(self, pangram):
        """ベンチマークとの比較"""
        benchmarks = self.get_benchmark_pangrams()
        comparisons = []
        
        for benchmark in benchmarks:
            comparison = {
                'benchmark': benchmark['text'],
                'length_diff': len(pangram) - len(benchmark['text']),
                'score_diff': self.evaluate(pangram)['total'] - benchmark['score']
            }
            comparisons.append(comparison)
        
        return comparisons
```

### 評価レポートの生成

```python
def generate_evaluation_report(pangram, language='en'):
    """評価レポートを生成"""
    evaluator = ComprehensivePangramEvaluator(language)
    results = evaluator.comprehensive_evaluation(pangram)
    
    report = f"""
# パングラム評価レポート

## 評価対象
{pangram}

## 妥当性検証
- 完全性: {'✓' if results['is_valid']['is_complete'] else '✗'}
- 完全パングラム: {'✓' if results['is_valid']['is_perfect'] else '✗'}
{f"- 不足文字: {', '.join(results['is_valid']['missing_chars'])}" if results['is_valid']['missing_chars'] else ""}

## スコア詳細
- 総合スコア: {results['scores']['total']:.1f}/100 ({results['scores']['grade']})
- 長さ: {results['scores']['breakdown']['length']:.1f}
- 自然さ: {results['scores']['breakdown']['naturalness']:.1f}
- 記憶しやすさ: {results['scores']['breakdown']['memorability']:.1f}
- 文字分布: {results['scores']['breakdown']['distribution']:.1f}
- 実用性: {results['scores']['breakdown']['practicality']:.1f}

## 改善提案
{chr(10).join(f"- {suggestion}" for suggestion in results['suggestions'])}

## ベンチマーク比較
{format_benchmark_comparison(results['comparison'])}
"""
    
    return report
```

## まとめ

パングラムの評価は多面的な観点から行う必要があり、用途に応じて評価基準の重要度が変わります。客観的な評価システムを構築することで、より良いパングラムの作成と選択が可能になります。

## 関連リンク

- [戻る：パングラム作成戦略とアルゴリズム](pangram-creation-strategies.md)
- [パングラム総合ガイド](pangram-overview.md)
- [日本語パングラムの特徴と課題](japanese-pangram-characteristics.md)