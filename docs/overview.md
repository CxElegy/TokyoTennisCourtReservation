# 概要

江戸川区の公共施設予約システム「えどねっと」でテニスコートの空きを監視し、
新しく空いた枠を通知するツール。他区のサイトも `sites/` に追加できる構成。

## フェーズ
1. **空き監視と通知**（ログイン不要）← 骨組みはここまで
2. ログインして予約・抽選結果の確認（アカウントは後日提供、Secrets / `.env` で渡す）
3. 予約・抽選申込の補助（最終確認は人が行う。要利用規約の確認）

## 構成
- `sites/` 予約サイト別の取得処理（`edogawa.py` は未実装のスタブ）
- `diff.py` 監視条件での絞り込みと、前回との差分
- `notifiers/` console / Discord / LINE（Messaging API）/ メール
- `storage.py` 前回結果を `data/state.json` に保存（Actions では cache で引き継ぐ）
- `cli.py` `tennis-reserve check`

## ログインの確認
```bash
# .env または環境変数に EDOGAWA_USER_ID / EDOGAWA_PASSWORD を設定してから
uv sync --extra browser
uv run playwright install chromium   # Claude Code クラウド環境では不要（PLAYWRIGHT_CHROMIUM_PATH を使う）
uv run tennis-reserve login           # 結果を表示し、data/login.png に画面を保存
```

## 注意
- えどねっとの robots.txt は `/user/Home` と `*.html` 以外を Disallow。アクセスは低頻度に抑える。
- 利用規約の本文が未確認。自動操作の可否を確認してから、フェーズ2以降に進む。
- 認証情報は絶対にコミットしない（`.env` は gitignore、Actions は Secrets）。
- 祝日（`holiday`）の判定は未実装。

## 次にやること
1. えどねっとの空き照会フローの通信を調べ、`sites/edogawa.py` を実装
2. 実サイトのレスポンスをフィクスチャにしてパーサのテストを追加
3. 通知先を決めて Secrets を設定
