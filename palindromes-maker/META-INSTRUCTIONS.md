# メタ命令書 - 回文作成プロジェクト

## プロジェクト運営ルール

### 1. 試行（Try）の管理

#### 新しい戦略を試す場合
1. **新しいtryフォルダを作成**
   ```
   outputs/try01/ → 初回試行
   outputs/try02/ → 戦略変更時
   outputs/try03/ → さらなる改善時
   ```

2. **各tryフォルダの必須ファイル**
   - `CLAUDE.md` - その試行の方針と戦略
   - `process.md` - 実施過程の詳細記録
   - `result.md` - 最終結果と評価

3. **戦略変更の基準**
   - 現在の方法で行き詰まった場合
   - 新しいアイデアを試す場合
   - 大幅な方針転換が必要な場合

### 2. ドキュメント管理

#### 階層構造
```
palindromes-maker/
├── META-INSTRUCTIONS.md    # このファイル（メタレベルの指示）
├── CLAUDE.md               # プロジェクト全体の指針
├── docs/                   # 恒久的なドキュメント
│   ├── 理論・方法論
│   └── 評価基準
└── outputs/                # 実行結果
    ├── try01/             # 各試行
    ├── try02/
    └── generation-log-*.md # 日次ログ
```

#### 文書の種類と役割
1. **恒久的文書**（/docs）
   - 理論、方法論、ツール
   - 試行を超えて有効な知識

2. **試行別文書**（/outputs/tryXX）
   - その試行特有の戦略
   - 実施記録と結果

3. **ログ文書**（generation-log）
   - 日々の進捗記録
   - 学習事項の蓄積

### 3. 作業フロー

#### 標準的な進行
1. **計画フェーズ**
   - tryXX/CLAUDE.md に戦略を記述
   - 明確な目標設定

2. **実行フェーズ**
   - tryXX/process.md に過程を記録
   - すべての試行を文書化

3. **評価フェーズ**
   - tryXX/result.md に結果をまとめる
   - 次の戦略への示唆を含める

### 4. メタレベルの原則

1. **反復的改善**
   - 各tryから学ぶ
   - 知識を蓄積する
   - 方法論を洗練する

2. **透明性**
   - すべての決定を記録
   - 失敗も成功も文書化
   - 理由を明確にする

3. **体系性**
   - 一貫した構造を維持
   - 命名規則を守る
   - 相互参照を活用

### 5. 戦略変更の手順

1. **現状評価**
   - 現在のtryの成果確認
   - 問題点の特定
   - 改善可能性の検討

2. **新戦略の立案**
   - 新しいtryフォルダ作成
   - CLAUDE.mdに方針記載
   - 前回からの変更点明記

3. **移行**
   - 有用な知見は/docsへ
   - 新tryで実践開始
   - generation-logに記録

### 6. 品質管理

#### チェックリスト
- [ ] 各文書は役割に従っているか
- [ ] プロセスは追跡可能か
- [ ] 知見は適切に保存されているか
- [ ] 次の人が理解できるか

#### 継続的改善
- 定期的にメタレベルで振り返り
- プロセス自体の改善
- より効率的な方法の探求

---

*このメタ命令書は、プロジェクトの運営方法そのものを定義し、継続的に更新される*