# 回文拡張戦略ガイド

## 概要
既存の回文を目標文字数に拡張するための体系的な方法論。

## 基本的な拡張パターン

### 1. 両端追加法
```
構造: X + [既存回文] + X
例: よ + きことこき + よ = よきことこきよ
```

### 2. 中央挿入法
```
構造: [前半] + X + [後半]
例: よきこ + と + こきよ = よきことこきよ
```

### 3. 複合拡張法
```
構造: 両端追加 + 中央挿入の組み合わせ
例: み + よきこ + と + こきよ + み
```

## 拡張時の分割パターン

### 奇数文字の回文（例：7文字）
```
パターンA: 3 + 1 + 3
パターンB: 2 + 3 + 2
パターンC: 1 + 5 + 1
```

### 偶数文字の回文（例：8文字）
```
パターンA: 4 + 4
パターンB: 3 + 2 + 3
パターンC: 2 + 4 + 2
```

## 具体的な拡張手順

### Step 1: 現在の文字数と目標の差を計算
```
例: 7文字 → 10文字（3文字追加必要）
```

### Step 2: 拡張パターンの選択
```
3文字追加の場合：
- 両端に1.5文字ずつ → 困難
- 片側に3文字 → 非対称
- 両端に1文字、中央に1文字 → 可能
```

### Step 3: 挿入候補の生成
```
両端候補: あ、い、う、え、お、か、が...
中央候補: の、と、に、は、を、も...
```

### Step 4: 組み合わせテスト
```
各組み合わせで：
1. 回文性チェック
2. 日本語自然さ評価
3. 意味の確認
```

## 中央挿入の詳細戦略

### 挿入位置の特定
1. **意味の切れ目を探す**
   - 単語の境界
   - 助詞の位置
   - 文節の区切り

2. **音韻的な切れ目**
   - 母音の連続
   - 子音の連続
   - リズムの変化点

### 挿入文字の選び方
1. **助詞の活用**
   - の、と、に、へ、を、は、が、も
   - 意味をつなぐ役割

2. **接続詞**
   - でも、しか、また
   - 文の流れを作る

3. **感嘆詞**
   - ああ、おお、まあ
   - 自然な間を作る

## 実践例

### 例1: 「よきことこきよ」（7文字）→ 10文字

#### 試行1: 両端追加のみ
```
お + よきことこきよ + お = およきことこきよお（9文字）
→ まだ1文字不足
```

#### 試行2: 中央挿入を追加
```
よきこ + と + こきよ
↓
よきこ + もと も + こきよ = よきこもともこきよ（9文字）
```

#### 試行3: 複合アプローチ
```
み + よきこ + と + こきよ + み = みよきことこきよみ（9文字）
↓
み + よきこ + のと の + こきよ + み = みよきこのとのこきよみ（11文字）
→ 1文字超過
```

## 文字数調整のテクニック

### 微調整が必要な場合
1. **促音（っ）の活用**
   - 1文字として数えられる
   - 音の切れ目を作る

2. **長音（ー）の使用**
   - カタカナ語で有効
   - リズムを整える

3. **拗音（ゃゅょ）**
   - 1文字として扱う
   - 音の変化を作る

## 注意点

1. **意味の保持**
   - 拡張後も意味が通ること
   - 不自然な挿入を避ける

2. **音の流れ**
   - 読みやすさを維持
   - リズムを崩さない

3. **文法的整合性**
   - 助詞の適切な使用
   - 語順の自然さ

## まとめ

効果的な拡張のポイント：
- 複数のパターンを試す
- 中央挿入を積極的に活用
- 意味と音の両方を考慮
- 段階的に調整する