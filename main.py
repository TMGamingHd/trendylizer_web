import argparse
import pathlib
from generators.ebook import generate_ebook
from generators.ad_copy import generate_ad_copy

def _ensure_dir(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def _slug(text):
    return "".join(c.lower() if c.isalnum() else "_" for c in text).strip("_")

def markdown_to_html(md_text):
    import markdown
    return markdown.markdown(md_text, extensions=['extra'])

def html_to_pdf(html, pdf_path):
    from weasyprint import HTML
    HTML(string=html).write_pdf(pdf_path)

def save_markdown_and_pdf(md, out_prefix):
    # Markdown
    md_path = out_prefix + ".md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    # PDF
    html = markdown_to_html(md)
    pdf_path = out_prefix + ".pdf"
    html_to_pdf(html, pdf_path)
    return md_path, pdf_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--product", choices=["ebook", "ad_copy", "both"], default="ebook")
    parser.add_argument("--keywords", nargs="+", required=True)
    parser.add_argument("--save", type=str, required=True)
    args = parser.parse_args()

    keywords = args.keywords
    for trend in keywords:
        trend_slug = _slug(trend)
        save_dir = pathlib.Path(args.save)
        if save_dir.suffix in (".md", ".pdf"):
            save_dir = save_dir.parent
        _ensure_dir(save_dir)
        out_prefix_ebook = str(save_dir / f"ebook_{trend_slug}")
        out_prefix_ad = str(save_dir / f"ad_copy_{trend_slug}")

        if args.product == "ebook":
            ebook_md, _ = generate_ebook(trend)
            save_markdown_and_pdf(ebook_md, out_prefix_ebook)

        elif args.product == "ad_copy":
            print("You must generate the eBook first or supply a product concept for proper ad copy alignment.")
            continue

        elif args.product == "both":
            ebook_md, product_concept = generate_ebook(trend)
            ad_copy_md = generate_ad_copy(trend, product_concept)
            save_markdown_and_pdf(ebook_md, out_prefix_ebook)
            save_markdown_and_pdf(ad_copy_md, out_prefix_ad)

if __name__ == "__main__":
    main()
