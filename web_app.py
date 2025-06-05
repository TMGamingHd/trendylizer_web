
from flask import Flask, request, render_template_string, send_file
from generators.ebook import generate_ebook
from generators.ad_copy import generate_ad_copy
from main import save_markdown_and_pdf  # Assuming it's defined in main.py
import os
import traceback

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<title>Trendylizer Generator</title>
<h1>Generate eBook</h1>
<form action="/generate-ebook" method="post">
  Trend: <input type="text" name="trend"><br>
  <input type="submit" value="Generate eBook">
</form>

<h1>Generate Ad Copy</h1>
<form action="/generate-ad-copy" method="post">
  Trend: <input type="text" name="trend"><br>
  Product Idea: <input type="text" name="product_idea"><br>
  <input type="submit" value="Generate Ad Copy">
</form>
'''

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_FORM)

@app.route("/generate-ebook", methods=["POST"])
def ebook():
    try:
        trend = request.form.get("trend", "")
        result = generate_ebook(trend)

        # If it's a tuple, extract first part as markdown
        markdown = result[0] if isinstance(result, tuple) else result

        # Ensure output directory exists
        os.makedirs("outputs", exist_ok=True)

        _, pdf_path = save_markdown_and_pdf(markdown, os.path.join("outputs", trend.replace(" ", "_")))

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"{trend}_ebook.pdf",
            mimetype="application/pdf"
        )
    except Exception as e:
        return f"<h2>Error Generating eBook</h2><pre>{traceback.format_exc()}</pre>"


@app.route("/generate-ad-copy", methods=["POST"])
def ad_copy():
    try:
        trend = request.form.get("trend", "")
        product_idea = request.form.get("product_idea", "")
        result = generate_ad_copy(trend, product_idea)

        # Make sure outputs directory exists
        os.makedirs("outputs", exist_ok=True)

        # Save ad copy as PDF
        _, pdf_path = save_markdown_and_pdf(result, os.path.join("outputs", f"ad_copy_{trend.replace(' ', '_')}"))

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"{trend}_ad_copy.pdf",
            mimetype="application/pdf"
        )
    except Exception as e:
        return f"<h2>Error Generating Ad Copy</h2><pre>{traceback.format_exc()}</pre>"
    except Exception as e:
        return f"<h2>Error Generating Ad Copy</h2><pre>{traceback.format_exc()}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

