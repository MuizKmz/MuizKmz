# Profile assets

All SVGs in `assets/` are generated — edit the content here, not the SVGs.

| Script | Renders | When |
|---|---|---|
| `gen_assets.py` | hero, section headers, skills, projects, gate, contact, buttons, divider, footer | by hand, after editing the lists at the top of the file |
| `gen_stats.py` | `stats.svg` (live STATUS window: level, contributions, streaks, languages) | daily by `.github/workflows/stats.yml` |

```bash
pip install fonttools brotli
python scripts/gen_assets.py
python scripts/gen_stats.py --demo   # mock data; CI runs it for real with GH_TOKEN
```

`hud.py` holds the shared palette (from the eportfolio) and drawing helpers. Each SVG embeds only the glyphs it uses from Orbitron and JetBrains Mono (`fonts/`, SIL Open Font License).
