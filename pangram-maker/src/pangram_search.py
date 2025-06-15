#!/usr/bin/env python3
"""
パングラム探索アルゴリズム
最小重複を目指したパングラム生成
"""

import random
from collections import defaultdict, Counter
import time

# ひらがな46文字
HIRAGANA = list('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

# 文字連続可能性（簡易版）
CAN_FOLLOW = {
    'あ': 'いうえおかきくけこさしすせそたちつてとなにねのまみめもやらりるれわ',
    'い': 'うえおかきくけこしすせそちつてとぬのまもやらりるれろわ',
    'う': 'えおかきくけこしすたちでまみめもらりるれ',
    'え': 'いおかきくこさたてとにのばびまみもらりるん',
    'お': 'うかきくけこさしとにのもやらりれろん',
    'か': 'いえおきくけこさしぜぞなにのらりるれろわん',
    'き': 'えおくさしてとのはまみもゃゅょらりるれろん',
    'く': 'うきこしとのはむらりるれろわん',
    'け': 'いきさしたてとにのんらりるれろ',
    'こ': 'うえおくしそとのまみもらりるれろわん',
    'さ': 'いかきくけこしまらりるれわん',
    'し': 'あいうえおかきくけこたちてとなにのはまみむめもゃゅょらりるれろわん',
    'す': 'うえおぎくこずてとのべまみむらりるれん',
    'せ': 'いかきくつてとにのらりるれん',
    'そ': 'うおくこしのらりるれん',
    'た': 'いえおかきくけこしすちてとにのべまみもらりるれん',
    'ち': 'あいうえおかきくけさてとにのゃゅょらりるれん',
    'つ': 'うかきくけたてなのまみめもらりるれん',
    'て': 'いうおきくしとのもらりるれん',
    'と': 'うおかきくこしてにのもらりるれん',
    'な': 'いうえおかきくけこさしすせそたつどにのまみめもらりるれわん',
    'に': 'うえおかきくけこしちつてとなのほもゃゅょわん',
    'ぬ': 'うのらりるれ',
    'ね': 'うこつてとのん',
    'の': 'うえおかきくけこしせそちてとなにはひふへほまみめもらりるれん',
    'は': 'いうえおかきくけこしすたちつてとなにのらりるれん',
    'ひ': 'えおかきくけこさしたちつてとのらりるれろん',
    'ふ': 'うえおかきくけこたつとのらりるれん',
    'へ': 'いきくけこのん',
    'ほ': 'うかくけこしとのん',
    'ま': 'いうえおかきくけこさしすたちつてとなにのらりるれん',
    'み': 'うえおかきくけこちつてとなにのまゃゅょらりるれん',
    'む': 'うかきくけこしのらりるれん',
    'め': 'いうかきくけこしてとのらりるれん',
    'も': 'うえおかきくけこしちつてとのらりるれん',
    'や': 'かきくけこすまん',
    'ゆ': 'うきくめん',
    'よ': 'うかきくけこしりるん',
    'ら': 'いうえおかきくけこしすなにのれん',
    'り': 'えおかきくけこつてとのゃゅょん',
    'る': 'いうえおかきくけこしとのまん',
    'れ': 'いうかきくけこたてとのばん',
    'ろ': 'うかきくけこん',
    'わ': 'かきくけこたなにのらりるれん',
    'を': 'みるきくつあいうえおかきさしすせそたちてとなにぬねのはひふへほまめもやゆよらりれろわん',
    'ん': ''  # 文末のみ
}

def is_valid_sequence(path):
    """文字列が有効な連続かチェック"""
    for i in range(len(path) - 1):
        current = path[i]
        next_char = path[i + 1]
        if current not in CAN_FOLLOW:
            return False
        if next_char not in CAN_FOLLOW[current]:
            return False
    return True

def greedy_search(start_char='あ', max_iterations=10000):
    """貪欲法による探索"""
    best_path = []
    best_coverage = 0
    
    for _ in range(max_iterations):
        used = set()
        path = [start_char]
        used.add(start_char)
        current = start_char
        
        while len(used) < 46:
            # 使用可能な次の文字
            candidates = [c for c in CAN_FOLLOW.get(current, '') 
                         if c not in used]
            
            if not candidates:
                break
            
            # ランダムに選択（多様性のため）
            if random.random() < 0.3:
                next_char = random.choice(candidates)
            else:
                # 後続が多い文字を優先
                next_char = max(candidates, 
                              key=lambda x: len([c for c in CAN_FOLLOW.get(x, '') 
                                               if c not in used]))
            
            path.append(next_char)
            used.add(next_char)
            current = next_char
        
        # 最良の結果を保存
        if len(used) > best_coverage:
            best_coverage = len(used)
            best_path = path.copy()
            
            if best_coverage == 46:
                return ''.join(best_path), best_coverage
    
    return ''.join(best_path), best_coverage

def optimize_with_duplicates(target_length=80):
    """重複を許可した最適化"""
    # まず貪欲法で基本パスを生成
    base_path, coverage = greedy_search()
    
    if coverage < 46:
        # 不足文字を特定
        used = set(base_path)
        missing = [c for c in HIRAGANA if c not in used]
        
        # 不足文字を含む短い単語や句を挿入
        result = base_path
        for char in missing:
            # その文字を含む位置を探す
            inserted = False
            for i in range(len(result) - 1):
                if result[i] in CAN_FOLLOW and char in CAN_FOLLOW[result[i]]:
                    # 挿入可能
                    result = result[:i+1] + char + result[i+1:]
                    inserted = True
                    break
            
            if not inserted:
                # 末尾に追加を試みる
                if result[-1] in CAN_FOLLOW and char in CAN_FOLLOW[result[-1]]:
                    result += char
    else:
        result = base_path
    
    return result

def create_meaningful_pangram():
    """意味のあるパングラムを作成"""
    # 意味のある部分フレーズ
    phrases = [
        'はるかぜ', 'なつうみ', 'あきもみじ', 'ふゆゆき',
        'わかもの', 'としより', 'ぬのふく', 'やまへ',
        'ほんをよむ', 'そらをみる', 'とりがなく', 'かぜふく',
        'えきで', 'ねこ', 'いぬ', 'むし', 'はな',
        'つきよ', 'ほしぞら', 'あめのひ', 'はれ',
        'きせつ', 'ちがう', 'よろこび', 'しぜん'
    ]
    
    # 使用文字を追跡
    used_chars = set()
    result = []
    
    # フレーズを組み合わせ
    random.shuffle(phrases)
    for phrase in phrases:
        # このフレーズが新しい文字を含むか
        new_chars = set(phrase) - used_chars
        if new_chars:
            result.append(phrase)
            used_chars.update(phrase)
    
    # 不足文字を追加
    missing = set(HIRAGANA) - used_chars
    for char in missing:
        result.append(char)
    
    return ''.join(result), len(''.join(result))

if __name__ == "__main__":
    print("=== パングラム探索開始 ===\n")
    
    # 完全パングラムを目指す
    print("1. 完全パングラム探索（重複なし）")
    start = time.time()
    perfect, coverage = greedy_search(max_iterations=1000)
    elapsed = time.time() - start
    
    print(f"カバレッジ: {coverage}/46文字")
    print(f"生成文字列: {perfect}")
    print(f"文字数: {len(perfect)}")
    print(f"探索時間: {elapsed:.2f}秒")
    
    if coverage < 46:
        missing = [c for c in HIRAGANA if c not in perfect]
        print(f"不足文字: {''.join(missing)}")
    
    # 最小重複パングラム
    print("\n2. 最小重複パングラム探索")
    optimized = optimize_with_duplicates()
    print(f"生成文字列: {optimized}")
    print(f"文字数: {len(optimized)}")
    
    # 確認
    char_count = Counter(optimized)
    duplicates = {c: count for c, count in char_count.items() if count > 1}
    if duplicates:
        print(f"重複文字: {duplicates}")
    
    # 意味のあるパングラム
    print("\n3. 意味のあるパングラム生成")
    meaningful, length = create_meaningful_pangram()
    print(f"生成文字列: {meaningful}")
    print(f"文字数: {length}")
    
    # 不足文字チェック
    used = set(meaningful)
    if len(used) < 46:
        missing = [c for c in HIRAGANA if c not in used]
        print(f"不足文字: {''.join(missing)}")