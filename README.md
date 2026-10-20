# TokyoTennisCourtReservation

江戸川区「えどねっと」のテニスコート空き監視・通知ツール（骨組み）。詳細は [docs/overview.md](docs/overview.md)。

```bash
uv sync --extra dev
cp .env.example .env            # 通知先などを記入（コミットしない）
uv run pytest
uv run tennis-reserve check --force
```

監視対象は `config/facilities.yaml` で設定します。現状 `sites/edogawa.py` は未実装のため、
`check` は NotImplementedError で止まります（次のステップ参照）。
