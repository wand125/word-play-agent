# パングラム作成プロジェクト（Pangram Maker）

## プロジェクト概要

パングラム（Pangram）は、アルファベットのすべての文字を少なくとも1回ずつ含む文章です。このプロジェクトでは、日本語（ひらがな）のパングラムを体系的に作成・研究します。

## パングラムとは

### 定義
- **語源**：ギリシャ語の「pan（すべて）」＋「gramma（文字）」
- **目的**：フォント表示、タイピング練習、暗号学などで使用
- **挑戦**：最小文字数で自然な文章を作ること

### 種類
1. **通常のパングラム**：すべての文字を含む（重複可）
2. **完全パングラム**：各文字を1回ずつのみ使用
3. **自己列挙パングラム**：文字の使用回数を文中で述べる

## 日本語パングラムの特徴

### 対象文字
- **基本セット**：ひらがな46文字
- **拡張セット**：濁点・半濁点含む71文字
- **歴史的仮名**：「ゐ」「ゑ」を含む場合も

### 課題
1. **文字数の多さ**：英語26文字に対し、ひらがなは46文字
2. **文字の独立性**：単独で意味を持たない文字が多い
3. **文法的制約**：助詞や活用語尾の必要性
4. **自然さの困難**：すべての文字を含みつつ意味の通る文章

## 有名な例

### 日本語
- **いろは歌**（歴史的完全パングラム）
  ```
  いろはにほへと ちりぬるを
  わかよたれそ つねならむ
  うゐのおくやま けふこえて
  あさきゆめみし ゑひもせす
  ```

### 英語
- "The quick brown fox jumps over the lazy dog"（35文字）
- 最も実用的で広く使われるパングラム

## プロジェクト構造

```
pangram-maker/
├── CLAUDE.md         # エージェント専用ガイド
├── README.md         # このファイル
├── docs/             # 詳細ドキュメント
│   ├── pangram-overview.md
│   ├── japanese-pangram-characteristics.md
│   ├── pangram-creation-strategies.md
│   └── pangram-evaluation-criteria.md
├── src/              # プログラム・スクリプト
│   └── check_pangram.py（作成予定）
├── data/             # 作成したパングラム
│   └── pangrams/
└── outputs/          # 試行錯誤の記録
    └── tryXX/        # 各試行の5文書
```

## 作成戦略

### 基本アプローチ
1. **希少文字優先**：使用頻度の低い文字から配置
2. **複合語活用**：複数の未使用文字を含む単語
3. **文法的構築**：助詞や活用で不足文字を補完

### アルゴリズム的手法
- A*探索による最適化
- ビットマスクでの文字管理
- 枝刈りによる効率化

## 評価基準

### 主要指標
1. **文字数**：総文字数の少なさ（最重要）
2. **自然さ**：日本語としての流暢さ
3. **記憶性**：覚えやすさ
4. **実用性**：タイピング練習等での使いやすさ

### スコアリング
- 総合評価 = 文字数(40%) + 自然さ(30%) + 記憶性(20%) + 実用性(10%)

## 現在の目標

1. **基本パングラム作成**：ひらがな46文字を含む自然な文章
2. **文字数最適化**：100文字以下を目指す
3. **完全パングラムへの挑戦**：各文字1回ずつ（46文字）

## 関連プロジェクト

- **palindromes-maker**：回文作成
- **tenbun-maker**：転文作成
- **lipogram-maker**：リポグラム作成（予定）

## 参考文献

- [docs/README.md](docs/README.md) - ドキュメント一覧
- [docs/pangram-overview.md](docs/pangram-overview.md) - パングラム総合ガイド
- [docs/pangram-creation-strategies.md](docs/pangram-creation-strategies.md) - 作成戦略

---

*パングラムは、言語の全体性を一文に凝縮する芸術です。*