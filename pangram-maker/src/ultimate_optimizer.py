#!/usr/bin/env python3
"""
究極最適化エンジン
50文字への限界挑戦
"""

from collections import Counter

HIRAGANA_46 = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

def create_ultimate_versions():
    """究極の短縮版を作成"""
    
    # 現在の55文字版の問題
    # 不足：く、さ、も、れ
    
    versions = []
    
    # Version 1: 不足文字を補完
    v1 = """ゆめをみた。うみへ。ひとぬのきて。
ねこえきでけんか。むしとぶ。ほし。
やまにおり、ちる。なつあき。
よ。はじ。ふそら。すわ。いろ。
くも。されせげん。"""
    
    # Version 2: より効率的に
    v2 = """ゆめをみた。うみへ。ひとぬのきて。
ねこえきでけんか。むしとぶ。ほし。
やまおり、ちる。なつあきそら。
よはじ。ふく。すわれ。いも。せげん。"""
    
    # Version 3: 極限圧縮
    v3 = """ゆめをみた。うみへ。ひとぬのきて。
ねこえきでけんか。むしとぶ。ほしそら。
やまおり、ちる。なつあき。
よ。はじ。ふく。すわれ。いも。せげん。"""
    
    # Version 4: 50文字挑戦
    v4 = """ゆめをみた。うみへ。ひとぬのきて。
ねこえきでけんか。むしとぶほし。
やまおり、ちなつ。あきそら。
よはじ。ふく。すわれ。いも。せげん。"""
    
    # Version 5: 究極版
    v5 = """ゆめをみた。うみへ。ひとぬのきて。
ねこえきでけんか。むしとぶ。
ほしそら。やまおりちる。
なつあき。よはじ。ふく。
すわれ。いも。せげん。"""
    
    # Version 6: 文字配置最適化
    v6 = """ゆめをみる。うみへ。ひとぬのきて。
ねこえきでけんか。むしとぶ。
ほしそら。やまにおりちた。
なつあき。よはじ。ふく。
すわれ。いも。せげん。"""
    
    versions = [v1, v2, v3, v4, v5, v6]
    
    # 各バージョンを検証
    results = []
    for i, text in enumerate(versions):
        hiragana = [c for c in text if c in HIRAGANA_46]
        used = set(hiragana)
        missing = HIRAGANA_46 - used
        count = len(hiragana)
        
        # 重複分析
        counter = Counter(hiragana)
        duplicates = [(char, cnt) for char, cnt in counter.items() if cnt > 1]
        
        results.append({
            'version': i + 1,
            'text': text,
            'count': count,
            'missing': missing,
            'is_pangram': len(missing) == 0,
            'duplicates': sorted(duplicates, key=lambda x: x[1], reverse=True)
        })
    
    return results

def find_optimal_arrangement():
    """最適な文字配置を探索"""
    
    # 必須要素（削除不可）
    essential = {
        'を': 'ゆめを',  # 3文字
        'へ': 'うみへ',  # 3文字
        'ぬの': 'ぬのきて',  # 4文字
        'けんか': 'けんか',  # 3文字
    }
    
    # 効率的な組み合わせ
    efficient_words = {
        'われ': set('われ'),
        'よる': set('よる'),
        'ふく': set('ふく'),
        'さく': set('さく'),
        'もり': set('もり'),
        'すわ': set('すわ'),
        'いも': set('いも'),
        'ほしそら': set('ほしそら'),
    }
    
    print("\n=== 効率的な単語分析 ===")
    for word, chars in efficient_words.items():
        print(f"{word}: {len(chars)}文字をカバー")

if __name__ == "__main__":
    print("=== 究極最適化への挑戦 ===\n")
    
    results = create_ultimate_versions()
    
    best_pangram = None
    best_count = float('inf')
    
    for result in results:
        print(f"Version {result['version']}:")
        print(f"  文字数: {result['count']}")
        print(f"  パングラム: {'✅' if result['is_pangram'] else '❌'}")
        
        if result['missing']:
            print(f"  不足: {''.join(sorted(result['missing']))}")
        
        if result['duplicates']:
            print(f"  重複: ", end="")
            for char, cnt in result['duplicates'][:5]:  # 上位5つ
                print(f"{char}({cnt}) ", end="")
            print()
        
        if result['is_pangram'] and result['count'] < best_count:
            best_pangram = result
            best_count = result['count']
        
        print()
    
    if best_pangram:
        print(f"\n=== 最良結果: {best_count}文字 ===")
        print(best_pangram['text'])
        print("\n重複詳細:")
        for char, cnt in best_pangram['duplicates']:
            print(f"  {char}: {cnt}回")
    
    find_optimal_arrangement()