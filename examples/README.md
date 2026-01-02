# Examples

Example scripts and notebooks demonstrating how to use `espn-sports-api`.

## Notebooks

Interactive notebooks to explore the API:

| Platform | Link |
|----------|------|
| **Deepnote** | [Open in Deepnote](https://deepnote.com/launch?url=https://github.com/fenneh/espn-sports-api/blob/main/examples/notebooks/explore_sports_data.ipynb) |
| **Google Colab** | [Open in Colab](https://colab.research.google.com/github/fenneh/espn-sports-api/blob/main/examples/notebooks/explore_sports_data.ipynb) |
| **Local Jupyter** | `jupyter notebook examples/notebooks/explore_sports_data.ipynb` |

## Scripts

First, install the package:

```bash
pip install espn-sports-api
```

Then run any example:

```bash
python examples/scripts/nfl_example.py
python examples/scripts/soccer_epl_example.py
```

## Contents

```
examples/
├── notebooks/
│   └── explore_sports_data.ipynb   # Interactive API explorer
└── scripts/
    ├── nfl_example.py              # NFL: scores, teams, rosters, odds
    └── soccer_epl_example.py       # Premier League: table, fixtures
```

Feel free to copy and modify these for your own projects.
