# 転文作成プロジェクト (Tenbun Maker)

## プロジェクト概要
転文（てんぶん）は、順方向と逆方向で異なる意味を持つ文章です。回文が同じ文字列になるのに対し、転文は異なる文字列・異なる意味になります。

## 転文の例

### 基本例
- 順方向：「いか」（烏賊）
- 逆方向：「かい」（貝）

### 文章例
- 順方向：「たこやき」（たこ焼き）
- 逆方向：「きやこた」（来や、こた）

### より複雑な例
- 順方向：「きのこたけ」（キノコ、竹）
- 逆方向：「けたこのき」（桁、この木）

## 転文の特徴

1. **双方向性**：両方向とも意味のある日本語
2. **非対称性**：回文とは異なり、文字列が異なる
3. **創造性**：2つの異なる意味を同時に表現

## プロジェクト目標

1. 高品質な転文の作成手法確立
2. 評価基準の明確化
3. 体系的なデータベース構築
4. 自動生成システムの開発

## ディレクトリ構造
```
tenbun-maker/
├── README.md          # このファイル
├── CLAUDE.md          # エージェント用ガイド
├── docs/              # ドキュメント
├── src/               # ソースコード
├── data/              # 生成データ
├── tests/             # テストケース
└── outputs/           # 出力結果
```

## 回文プロジェクトとの関係

転文は回文の発展形として位置づけられます：
- 回文：A→B = B→A（同じ）
- 転文：A→B ≠ B→A（異なるが両方意味あり）

両プロジェクトで得られた知見を相互に活用します。

---

*"言葉は前からも後ろからも、異なる物語を語る"*