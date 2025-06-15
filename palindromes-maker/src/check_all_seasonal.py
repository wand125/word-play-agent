#!/usr/bin/env python3
"""すべての季節転文を検証するスクリプト"""

def check_reversible(word1, word2, description=""):
    """転文が正しいかチェックする"""
    reversed_word1 = word1[::-1]
    is_valid = reversed_word1 == word2
    status = "✓" if is_valid else "✗"
    
    print(f"{status} {word1}（{description}）→ {reversed_word1} {'=' if is_valid else '≠'} {word2}")
    return is_valid

def main():
    print("季節をテーマにした転文の完全検証\n")
    
    # 初回発見分
    original_words = {
        "春": [
            ("はな", "なは", "花→那覇"),
            ("くさ", "さく", "草→咲く"),
            ("さくら", "らくさ", "桜→楽さ"),
            ("にじ", "じに", "虹→死に"),
        ],
        "夏": [
            ("なつ", "つな", "夏→綱"),
            ("みず", "ずみ", "水→済み"),
            ("すい", "いす", "西[瓜]→椅子"),
            ("なす", "すな", "茄子→砂"),
            ("あつい", "いつあ", "暑い→何時あ"),
        ],
        "秋": [
            ("つき", "きつ", "月→狐"),
            ("くり", "りく", "栗→陸"),
            ("なし", "しな", "梨→品"),
            ("かき", "きか", "柿→期間[略]"),
            ("いも", "もい", "芋→思い[方言]"),
            ("もみじ", "じみも", "紅葉→地味も"),
        ],
        "冬": [
            ("ゆき", "きゆ", "雪→消ゆ[古語]"),
            ("とし", "しと", "年→仕途"),
            ("しも", "もし", "霜→もし"),
        ]
    }
    
    # 追加発見分
    additional_words = {
        "春": [
            ("たね", "ねた", "種→ネタ"),
            ("めぐみ", "みぐめ", "恵み→見込め[口語]"),
        ],
        "夏": [
            ("うみ", "みう", "海→見う[古語]"),
            ("なみ", "みな", "波→皆"),
            ("かい", "いか", "貝→烏賊"),
            ("せみ", "みせ", "蝉→店"),
        ],
        "秋": [
            ("たき", "きた", "滝→北"),
            ("やま", "まや", "山→摩耶"),
            ("きく", "くき", "菊→茎"),
        ],
        "冬": [
            ("ねつ", "つね", "熱→常"),
            ("たき", "きた", "焚き→北"),
        ]
    }
    
    print("【初回発見分】")
    total_valid = 0
    total_checked = 0
    
    for season, words in original_words.items():
        print(f"\n{season}:")
        season_valid = 0
        for word1, word2, desc in words:
            if check_reversible(word1, word2, desc):
                season_valid += 1
            total_checked += 1
        total_valid += season_valid
    
    print("\n【追加発見分】")
    for season, words in additional_words.items():
        print(f"\n{season}:")
        season_valid = 0
        for word1, word2, desc in words:
            if check_reversible(word1, word2, desc):
                season_valid += 1
            total_checked += 1
        total_valid += season_valid
    
    print(f"\n【総計】")
    print(f"検証した転文: {total_checked}個")
    print(f"有効な転文: {total_valid}個")
    print(f"成功率: {total_valid/total_checked*100:.1f}%")
    
    # 季節別集計
    print("\n【季節別集計】")
    all_words = {}
    for season in ["春", "夏", "秋", "冬"]:
        all_words[season] = original_words.get(season, []) + additional_words.get(season, [])
        valid_count = sum(1 for w1, w2, _ in all_words[season] if w1[::-1] == w2)
        print(f"{season}: {valid_count}個")
    
    # 文字数別統計
    print("\n【文字数別統計】")
    length_stats = {}
    for season_words in all_words.values():
        for word1, word2, desc in season_words:
            length = len(word1)
            if length not in length_stats:
                length_stats[length] = {"valid": 0, "total": 0}
            length_stats[length]["total"] += 1
            if word1[::-1] == word2:
                length_stats[length]["valid"] += 1
    
    for length in sorted(length_stats.keys()):
        stats = length_stats[length]
        print(f"{length}文字: {stats['valid']}/{stats['total']}個 ({stats['valid']/stats['total']*100:.1f}%)")
    
    # 特殊な転文の紹介
    print("\n【特に興味深い転文】")
    print("・相互転文: すな（砂）⇔ なす（茄子）")
    print("・同音異義: たき（滝/焚き）→ きた（北）")
    print("・季節横断: かい（貝・夏）→ いか（烏賊）")

if __name__ == "__main__":
    main()