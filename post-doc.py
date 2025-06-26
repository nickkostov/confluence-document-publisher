import requests
from datetime import date
import click
import json
import subprocess
import sys
import os

@click.command()
@click.option('--pat', required=True, help='Personal Access Token for Confluence')
@click.option('--base-url', required=True, help='Base URL of the Confluence instance')
@click.option('--space-key', required=True, help='Space key in Confluence')
@click.option('--page-title', required=True, help='Title prefix for the Confluence page')
@click.option('--input-md-file', required=True, type=click.Path(exists=True), help='Input Markdown file')
@click.option('--html-file', required=True, type=str, help='Path for the output HTML file (will be generated and uploaded)')
@click.option('--parent-page-id', required=True, type=int, help='ID of the parent page in Confluence')
def create_document(pat, base_url, space_key, page_title, input_md_file, html_file, parent_page_id):
    """Converts Markdown to HTML (using the given html-file name) and uploads to Confluence."""

    # === Step 1: Convert Markdown to HTML ===
    click.echo(f"Converting: {input_md_file} → {html_file} using pandoc")
    try:
        subprocess.run([
            "pandoc", input_md_file,
            "-f", "markdown", "-t", "html",
            "-o", html_file
        ], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Error while running pandoc: {e}", err=True)
        sys.exit(1)

    if not os.path.exists(html_file):
        click.echo(f"❌ HTML file '{html_file}' not found after conversion", err=True)
        sys.exit(1)

    # === Step 2: Build page title ===
    run_date = date.today()
    document_name = f"{page_title} - {run_date}"
    click.echo(f"Generated Confluence page title: {document_name}")

    # === Step 3: Read HTML content ===
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception as e:
        click.echo(f"❌ Failed to read HTML file: {e}", err=True)
        sys.exit(1)

    # === Step 4: Prepare and send API request ===
    payload = {
        "type": "page",
        "title": document_name,
        "space": {"key": space_key},
        "ancestors": [{"id": parent_page_id}],
        "body": {
            "storage": {
                "value": html_content,
                "representation": "storage"
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {pat}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    click.echo("Uploading page to Confluence...")
    response = requests.post(
        f"{base_url}/rest/api/content",
        headers=headers,
        json=payload
    )

    click.echo(f"Status: {response.status_code}")
    try:
        click.echo("Response:")
        click.echo(json.dumps(response.json(), indent=2))
    except Exception:
        click.echo("⚠️ Response not in JSON format:")
        click.echo(response.text)

if __name__ == '__main__':
    create_document()
