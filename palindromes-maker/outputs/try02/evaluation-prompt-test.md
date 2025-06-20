# evaluation-prompts.mdを使用した再評価例

## 双方向評価プロンプトの使用例

### 評価対象：「ゆめのなかかなのめゆ」

以下の回文候補を両方向から評価してください。

回文候補：「ゆめのなかかなのめゆ」
前から読み：「夢の中、かなの目ゆ」
後から読み：「ゆめのなか、かなのめゆ」

#### 前方向評価：
- 成立：はい
- 意味：はい
- 文法：はい
- 実在性：はい
- 自然さ：10/10
- 具体例：「夢の中で見た光景」という日常的な表現

#### 後方向評価：
- 成立：いいえ
- 意味：いいえ
- 文法：いいえ（「目ゆ」は動詞として不成立）
- 実在性：いいえ（「目ゆ」は造語）
- 自然さ：1/10
- 具体例：使用例なし（造語のため）

#### 採用基準チェック：
- 両方向とも5点以上：✗（後方向1点）
- 片方でも3点以下：✓（後方向1点で却下）
- 造語が含まれる：✓（「目ゆ」が造語）

#### 総合判定：**却下**
判定理由：後方向が完全な造語で、日本語として成立していない。評価基準の「片方でも3点以下は却下」に該当。

## プロンプト使用の効果

1. **明確な評価基準**
   - 実在性のチェックが追加
   - 造語の明確な排除
   - 具体例の要求

2. **客観的な判定**
   - 感覚的な「詩的」という評価を排除
   - 数値基準での明確な判定
   - 却下理由の明確化

3. **改善点の発見**
   - evaluation-prompts.mdは適切に機能
   - 今後はこのプロンプトを確実に使用
   - 評価の一貫性が向上

---
*このテストにより、evaluation-prompts.mdの有効性を確認*