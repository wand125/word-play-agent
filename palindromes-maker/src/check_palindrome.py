#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回文チェックスクリプト
指定された文字列が回文かどうかを判定します。
"""

def is_palindrome(text):
    """
    文字列が回文かどうかを判定する
    
    Args:
        text (str): 判定する文字列
        
    Returns:
        bool: 回文の場合True、そうでない場合False
    """
    # 文字のリストに変換
    chars = list(text)
    
    # 逆順のリストを作成
    reversed_chars = chars[::-1]
    
    # 比較結果を返す
    return chars == reversed_chars

def check_palindrome_with_details(text):
    """
    回文チェックの詳細を表示する
    
    Args:
        text (str): 判定する文字列
        
    Returns:
        dict: 判定結果の詳細
    """
    chars = list(text)
    reversed_chars = chars[::-1]
    
    forward = '・'.join(chars)
    backward = '・'.join(reversed_chars)
    
    is_valid = chars == reversed_chars
    
    result = {
        'text': text,
        'length': len(text),
        'forward': forward,
        'backward': backward,
        'is_palindrome': is_valid,
        'forward_list': chars,
        'backward_list': reversed_chars
    }
    
    return result

def print_check_result(text):
    """
    回文チェック結果を見やすく表示する
    
    Args:
        text (str): 判定する文字列
    """
    result = check_palindrome_with_details(text)
    
    print(f"\n回文チェック: 「{result['text']}」")
    print(f"文字数: {result['length']}文字")
    print(f"前から: {result['forward']}")
    print(f"後から: {result['backward']}")
    print(f"判定: {'✓ 回文です' if result['is_palindrome'] else '✗ 回文ではありません'}")
    
    if not result['is_palindrome']:
        # 不一致箇所を特定
        for i, (f, b) in enumerate(zip(result['forward_list'], result['backward_list'])):
            if f != b:
                print(f"  → 位置{i+1}: '{f}' ≠ '{b}'")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # コマンドライン引数から文字列を取得
        text = sys.argv[1]
        print_check_result(text)
    else:
        # テスト用の例
        test_cases = [
            "しんぶんし",
            "たけやぶやけた",
            "ああなつよなつああ",
            "なつつな",
            "よるもよ"
        ]
        
        print("=== 回文チェックテスト ===")
        for text in test_cases:
            print_check_result(text)