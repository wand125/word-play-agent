#!/usr/bin/env python3
"""季節をテーマにした転文（reversible words）の検証スクリプト"""

def check_reversible(word1, word2, description=""):
    """転文が正しいかチェックする"""
    reversed_word1 = word1[::-1]
    is_valid = reversed_word1 == word2
    status = "✓" if is_valid else "✗"
    
    print(f"{status} {word1}（{description}）→ {reversed_word1} {'=' if is_valid else '≠'} {word2}")
    return is_valid

def main():
    print("季節をテーマにした転文の検証\n")
    
    seasonal_words = {
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
    
    total_valid = 0
    total_checked = 0
    
    for season, words in seasonal_words.items():
        print(f"\n【{season}】")
        season_valid = 0
        for word1, word2, desc in words:
            if check_reversible(word1, word2, desc):
                season_valid += 1
            total_checked += 1
        total_valid += season_valid
        print(f"  {season}の転文: {season_valid}/{len(words)}個が有効")
    
    print(f"\n総計: {total_valid}/{total_checked}個の転文が有効")
    print(f"成功率: {total_valid/total_checked*100:.1f}%")
    
    # 文字数別の統計
    print("\n【文字数別統計】")
    length_stats = {}
    for season, words in seasonal_words.items():
        for word1, word2, desc in words:
            length = len(word1)
            if length not in length_stats:
                length_stats[length] = {"valid": 0, "total": 0}
            length_stats[length]["total"] += 1
            if word1[::-1] == word2:
                length_stats[length]["valid"] += 1
    
    for length in sorted(length_stats.keys()):
        stats = length_stats[length]
        print(f"{length}文字: {stats['valid']}/{stats['total']}個 ({stats['valid']/stats['total']*100:.1f}%)")

if __name__ == "__main__":
    main()