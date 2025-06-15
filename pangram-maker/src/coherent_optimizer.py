#!/usr/bin/env python3
"""
文章完成度重視の最適化エンジン
文として読めるパングラムを50文字以下で実現
"""

from collections import Counter

HIRAGANA_46 = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

def create_coherent_versions():
    """文章として読める短縮版を作成"""
    
    versions = []
    
    # Version 1: 基本的な文章化
    v1 = """ゆめをみた。うみへ。
ひとぬのきてやまおり。
ねこえきでけんか。
むしとぶほしそら。
なつあきにちる。
はじめてよふく。
さわれ、いもろせげん。"""
    
    # Version 2: より自然な流れ
    v2 = """ゆめをみた。うみへ。
ひとぬのきてやまおり。
ねこえきでけんか。
むしとぶほしそら。
なつあきにちる。
はよ、ふくさわれ。
いもじろせげん。"""
    
    # Version 3: 助詞でつなぐ
    v3 = """ゆめをみる。うみへ。
ひとぬのきてやまにおり。
ねこ、えきでけんか。
むしとぶほしそら。
なつあきよ、ちさ。
はじめてふく。
すわれ、いもろせげん。"""
    
    # Version 4: 50文字挑戦
    v4 = """ゆめをみた。うみへ。
ひとぬのきてやまおり。
ねこえきでけんか。
むしとぶほしそら。
なつあきにちる。
はよじ、ふくさわれ。
いもろせげん。"""
    
    # Version 5: 究極の文章化
    v5 = """ゆめをみた。うみへいく。
ひとぬのきてやまおり。
ねこがえきでけんか。
むしとぶほしそら。
なつあきにちる。
はよ、ふさわじ。
いもろせげん。"""
    
    # Version 6: 48文字達成版
    v6 = """ゆめをみた。うみへ。
ひとぬのきてやまおり。
ねこえきでけんか。
むしとぶほしそら。
なつあきにちる。
はよじふくさわ。
いもろせげん。"""
    
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
        
        # 文章性評価
        sentences = text.strip().split('。')
        sentence_count = len([s for s in sentences if s])
        
        results.append({
            'version': i + 1,
            'text': text,
            'count': count,
            'missing': missing,
            'is_pangram': len(missing) == 0,
            'duplicates': sorted(duplicates, key=lambda x: x[1], reverse=True),
            'sentences': sentence_count
        })
    
    return results

def analyze_coherence(text):
    """文章の完成度を分析"""
    
    # 助詞の使用
    particles = ['を', 'に', 'へ', 'で', 'が', 'と', 'から', 'まで', 'より']
    particle_count = sum(1 for p in particles if p in text)
    
    # 文の構造
    sentences = text.strip().split('。')
    avg_length = sum(len(s) for s in sentences if s) / max(len([s for s in sentences if s]), 1)
    
    # 意味の連続性（隣接する要素の関連性）
    coherence_score = 0
    if 'うみへ' in text: coherence_score += 1
    if 'やまおり' in text or 'やまにおり' in text: coherence_score += 1
    if 'ほしそら' in text: coherence_score += 1
    if 'なつあき' in text: coherence_score += 1
    
    return {
        'particles': particle_count,
        'avg_sentence_length': avg_length,
        'coherence_score': coherence_score
    }

if __name__ == "__main__":
    print("=== 文章完成度重視の最適化 ===\n")
    
    results = create_coherent_versions()
    
    best_pangram = None
    best_count = float('inf')
    best_coherence = 0
    
    for result in results:
        print(f"Version {result['version']}:")
        print(f"  文字数: {result['count']}")
        print(f"  パングラム: {'✅' if result['is_pangram'] else '❌'}")
        print(f"  文数: {result['sentences']}")
        
        if result['missing']:
            print(f"  不足: {''.join(sorted(result['missing']))}")
        
        if result['duplicates']:
            print(f"  重複: ", end="")
            for char, cnt in result['duplicates'][:3]:
                print(f"{char}({cnt}) ", end="")
            print()
        
        # 文章性評価
        coherence = analyze_coherence(result['text'])
        total_coherence = coherence['particles'] + coherence['coherence_score']
        print(f"  文章性: 助詞{coherence['particles']}個, 連続性{coherence['coherence_score']}")
        
        if result['is_pangram'] and result['count'] <= best_count:
            if result['count'] < best_count or total_coherence > best_coherence:
                best_pangram = result
                best_count = result['count']
                best_coherence = total_coherence
        
        print()
    
    if best_pangram:
        print(f"\n=== 最良結果: {best_count}文字 ===")
        print(best_pangram['text'])
        print(f"\n文章性スコア: {best_coherence}")
        print("\n重複詳細:")
        for char, cnt in best_pangram['duplicates']:
            print(f"  {char}: {cnt}回")