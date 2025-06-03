import os
import importlib
import traceback

SCRAPER_DIR = "scrapers"
VALID_ENTRY_FUNCS = ["ingest", "run", "main"]

def run_scraper(module_name):
    try:
        mod = importlib.import_module(f"{SCRAPER_DIR}.{module_name}")
        for func_name in VALID_ENTRY_FUNCS:
            if hasattr(mod, func_name):
                print(f"▶️ Running {module_name}.{func_name}()")
                getattr(mod, func_name)()
                return "✅"
        return "⚠️ No valid entry function found"
    except Exception as e:
        print(f"❌ {module_name} failed:", e)
        traceback.print_exc()
        return "❌"

def main():
    print("🚀 Running all available scrapers...")
    results = {}
    for filename in os.listdir(SCRAPER_DIR):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            results[module_name] = run_scraper(module_name)
    print("\n📊 Scraper Results:")
    for mod, status in results.items():
        print(f" - {mod}: {status}")

if __name__ == "__main__":
    main()
