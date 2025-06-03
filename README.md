
# Trendylizer AI

**Overview**  
Trendylizer AI aggregates trends from 20+ public data sources and generates marketing products like e-books, ad copy, and infographics. It features a stub ML pipeline and full config, Docker, and CI/CD integration.

**Modules**
- `scrapers/`: API clients to fetch trending data
- `generators/`: Create marketing content
- `ml/`: Hypothesis-driven ML loop
- `trend_engine.py`: Aggregates data based on config
- `main.py`: CLI to run the system
- `tests/`: Unit tests

**Quick Start**
```bash
pip install -r requirements.txt
python main.py --product ebook
```

**Docker**
```bash
docker build . -t trendylizer
docker run trendylizer
```
