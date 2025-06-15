#!/usr/bin/env python3
"""
パングラムチェッカー
ひらがなのすべての文字が含まれているかを確認するスクリプト
"""

import sys
from collections import Counter

# 現代仮名遣いのひらがな46文字
HIRAGANA_46 = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん')

# 濁音・半濁音を含む71文字
HIRAGANA_71 = set('あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゆよらりるれろわをん')

def check_pangram(text, target_set=HIRAGANA_46):
    """
    テキストがパングラムかどうかをチェック
    
    Args:
        text: チェックする文字列
        target_set: 対象文字セット（デフォルトは46文字）
    
    Returns:
        tuple: (is_pangram, used_chars, missing_chars, char_count)
    """
    # テキストからひらがなのみを抽出
    hiragana_in_text = set(char for char in text if char in target_set)
    
    # 不足文字
    missing_chars = target_set - hiragana_in_text
    
    # パングラムかどうか
    is_pangram = len(missing_chars) == 0
    
    # 文字の使用回数をカウント
    char_count = Counter(char for char in text if char in target_set)
    
    return is_pangram, hiragana_in_text, missing_chars, char_count

def print_result(text, target_name="ひらがな46文字"):
    """結果を見やすく表示"""
    target_set = HIRAGANA_46 if "46" in target_name else HIRAGANA_71
    is_pangram, used_chars, missing_chars, char_count = check_pangram(text, target_set)
    
    print(f"\n{'='*50}")
    print(f"テキスト: {text[:50]}{'...' if len(text) > 50 else ''}")
    print(f"文字数: {len(text)}文字")
    print(f"対象: {target_name}")
    print(f"{'='*50}")
    
    if is_pangram:
        print("✅ パングラムです！")
        print(f"使用文字数: {len(used_chars)}/{len(target_set)}")
        print("\n文字使用回数（多い順）:")
        for char, count in char_count.most_common(10):
            print(f"  {char}: {count}回")
        if len(char_count) > 10:
            print(f"  ... 他{len(char_count)-10}文字")
    else:
        print("❌ パングラムではありません")
        print(f"使用文字数: {len(used_chars)}/{len(target_set)}")
        print(f"\n不足文字 ({len(missing_chars)}文字):")
        missing_sorted = sorted(missing_chars)
        for i in range(0, len(missing_sorted), 10):
            print(f"  {''.join(missing_sorted[i:i+10])}")
    
    # 最小使用回数の文字を表示
    if char_count:
        min_count = min(char_count.values())
        min_chars = [char for char, count in char_count.items() if count == min_count]
        print(f"\n最少使用文字 ({min_count}回): {''.join(sorted(min_chars))}")
    
    return is_pangram

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # コマンドライン引数から
        text = ' '.join(sys.argv[1:])
    else:
        # 標準入力から
        print("チェックするテキストを入力してください:")
        text = input().strip()
    
    if text:
        # 46文字でチェック
        result_46 = print_result(text, "ひらがな46文字")
        
        # 濁音・半濁音を含む場合は71文字でもチェック
        if any(char in text for char in HIRAGANA_71 - HIRAGANA_46):
            print("\n" + "="*50)
            result_71 = print_result(text, "ひらがな71文字（濁音・半濁音含む）")