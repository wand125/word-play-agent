#!/usr/bin/env python3
"""
意味のあるパングラム最適化ツール
日本語として自然な文章を保ちながら文字数を最小化
"""

import re
from collections import Counter

# ひらがな46文字
HIRAGANA = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

def analyze_pangram(text):
    """パングラムの詳細分析"""
    # ひらがなのみ抽出
    hiragana_only = ''.join([c for c in text if c in HIRAGANA])
    
    # 文字カウント
    char_count = Counter(hiragana_only)
    
    # 統計情報
    total_chars = sum(char_count.values())
    unique_chars = len(char_count)
    max_count = max(char_count.values()) if char_count else 0
    
    # 不足文字
    missing_chars = HIRAGANA - set(char_count.keys())
    
    # 重複文字
    duplicates = {c: count for c, count in char_count.items() if count > 1}
    
    return {
        'total_length': len(text),
        'hiragana_count': total_chars,
        'unique_chars': unique_chars,
        'missing_chars': missing_chars,
        'duplicates': duplicates,
        'max_duplication': max_count,
        'efficiency': unique_chars / total_chars if total_chars > 0 else 0
    }

def suggest_optimizations(text, analysis):
    """最適化の提案"""
    suggestions = []
    
    # 最も重複している文字
    if analysis['duplicates']:
        most_duplicated = max(analysis['duplicates'].items(), key=lambda x: x[1])
        suggestions.append(f"「{most_duplicated[0]}」が{most_duplicated[1]}回使用されています。")
        
        # その文字を含む部分を特定
        char = most_duplicated[0]
        positions = [i for i, c in enumerate(text) if c == char]
        
        # 削減可能な箇所を提案
        if len(positions) > 2:
            suggestions.append(f"位置{positions[2]}以降の「{char}」を削減できる可能性があります。")
    
    # 句読点の削減
    punctuation_count = text.count('。') + text.count('、')
    if punctuation_count > 5:
        suggestions.append(f"句読点が{punctuation_count}個あります。削減で{punctuation_count}文字短縮可能です。")
    
    # 助詞の最適化
    particles = ['が', 'の', 'に', 'を', 'へ', 'で', 'と', 'も', 'は']
    particle_usage = {}
    for p in particles:
        count = text.count(p)
        if count > 2:
            particle_usage[p] = count
    
    if particle_usage:
        suggestions.append(f"頻出助詞: {particle_usage}")
    
    return suggestions

def evaluate_naturalness(text):
    """日本語としての自然さを評価（簡易版）"""
    score = 100
    
    # 文の長さチェック
    sentences = re.split('[。！？]', text)
    for sent in sentences:
        if sent and len(sent) > 40:
            score -= 5  # 長すぎる文
        elif sent and len(sent) < 3:
            score -= 3  # 短すぎる文
    
    # 助詞の連続チェック
    if 'のの' in text or 'がが' in text:
        score -= 10
    
    # ひらがなの比率
    hiragana_ratio = sum(1 for c in text if c in HIRAGANA) / len(text) if text else 0
    if hiragana_ratio > 0.9:
        score -= 5  # ひらがなが多すぎる
    
    return max(0, score)

def optimize_pangram(text):
    """パングラムの最適化試行"""
    # 現在の分析
    analysis = analyze_pangram(text)
    
    if analysis['missing_chars']:
        print("❌ パングラムではありません")
        print(f"不足文字: {''.join(sorted(analysis['missing_chars']))}")
        return None
    
    print("✅ パングラムです！")
    print(f"\n【現在の統計】")
    print(f"総文字数: {analysis['total_length']}文字")
    print(f"ひらがな数: {analysis['hiragana_count']}文字")
    print(f"効率性: {analysis['efficiency']:.2%}")
    print(f"最大重複: {analysis['max_duplication']}回")
    
    # 自然さ評価
    naturalness = evaluate_naturalness(text)
    print(f"自然さスコア: {naturalness}/100")
    
    # 最適化提案
    suggestions = suggest_optimizations(text, analysis)
    if suggestions:
        print("\n【最適化の提案】")
        for i, sug in enumerate(suggestions, 1):
            print(f"{i}. {sug}")
    
    # 重複文字の詳細
    if analysis['duplicates']:
        print("\n【重複文字の詳細】")
        for char, count in sorted(analysis['duplicates'].items(), 
                                 key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {char}: {count}回")
    
    return analysis

# テスト用の短縮版生成関数
def create_shortened_versions(base_text):
    """ベーステキストから短縮版を生成"""
    versions = []
    
    # 句読点除去版
    no_punct = base_text.replace('。', '').replace('、', '')
    versions.append(("句読点なし", no_punct))
    
    # 助詞削減版
    reduced = base_text
    for particle in ['も', 'が', 'に', 'の']:
        # 最初の1つは残して削減
        first_pos = reduced.find(particle)
        if first_pos >= 0:
            before = reduced[:first_pos+1]
            after = reduced[first_pos+1:].replace(particle, '')
            reduced = before + after
    versions.append(("助詞削減", reduced))
    
    return versions

if __name__ == "__main__":
    # try03の最良版を分析
    pangrams = [
        # 131文字版（現在の最良）
        """はるかぜふきさくらちる。なつうみへいく。あきもみじめで、ふゆゆきこんこん。わかものとしより、ぬのきてやまへ。ほしぞらにつきでる。ねこがなく。えきでけんか、むしとぶ。それぞれちがうよろこび、せけんにはある。ひとがたのしさをもつ。すべてのいきもの、おなじそらのした。""",
        
        # 132文字版（ゆめを含む）
        """ゆめをみた。はるかぜふき、さくらちる。なつうみへいく。あきもみじめでる。ふゆゆきこんこん。わかものも、としよりも、ぬのきてやまへ。ほしぞらに、つきひかる。ねこがなく。えきでけんか。むしとぶ。それぞれちがうよろこびが、せけんにはある。すべてのひと、おなじそらのした。"""
    ]
    
    for i, pangram in enumerate(pangrams, 1):
        print(f"\n{'='*60}")
        print(f"【バージョン{i}】")
        print(pangram)
        print('='*60)
        
        # 最適化分析
        optimize_pangram(pangram)
        
        # 短縮版の生成と分析
        print("\n【短縮版の試作】")
        versions = create_shortened_versions(pangram)
        for name, version in versions:
            print(f"\n{name}:")
            print(version)
            analysis = analyze_pangram(version)
            print(f"文字数: {analysis['total_length']}文字")
            if analysis['missing_chars']:
                print(f"不足: {''.join(sorted(analysis['missing_chars']))}")