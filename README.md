# 📰 Confluence Document Publisher

GitHub Action to **convert Markdown to HTML using Pandoc** and **publish it to Atlassian Confluence** under a specified parent page.

---

## 📦 Repository

- **Owner**: [nickkostov](https://github.com/nickkostov)  
- **Repo**: [`confluence-document-publisher`](https://github.com/nickkostov/confluence-document-publisher)

---

## 🚀 Features

- ✅ Converts `.md` to `.html` using Pandoc  
- ✅ Uploads to Confluence via REST API  
- ✅ Cross-platform: Ubuntu, RHEL, macOS runners  
- ✅ Validates required inputs  
- ✅ Supports strict and automated publishing flow  

---

## 🛠 Inputs

| Input               | Required | Description                                                                 |
|---------------------|----------|-----------------------------------------------------------------------------|
| `input-md-file`     | ✅        | Path to the source Markdown file                                            |
| `output-html-file`  | ✅        | Path where the converted HTML should be saved                               |
| `space-key`         | ✅        | Confluence space key                                                        |
| `page-title`        | ✅        | Page title prefix (the date will be appended automatically)                 |
| `pat`               | ✅        | Personal Access Token for Confluence (must be secret)                       |
| `base-url`          | ✅        | Base URL of the Confluence instance (e.g. `https://yoursite.atlassian.net`)|
| `parent-page-id`    | ✅        | Numeric ID of the Confluence parent page                                    |

---

## 🧪 Example Usage

```yaml
name: Publish to Confluence

on:
  workflow_dispatch:

jobs:
  publish-doc:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Publish Markdown Document to Confluence
        uses: nickkostov/confluence-document-publisher@main
        with:
          input-md-file: docs/weekly-report.md
          output-html-file: docs/weekly-report.html
          space-key: DOCS
          page-title: "Weekly Report"
          pat: ${{ secrets.CONFLUENCE_PAT }}
          base-url: https://your-domain.atlassian.net/wiki
          parent-page-id: 123456
```

---

## 📥 Installation

You can use the Action directly from this repository:

```yaml
uses: nickkostov/confluence-document-publisher@main
```

---

## 🧱 Requirements

- Python ≥ 3.7 (checked automatically)
- [Pandoc](https://pandoc.org/)
- Python packages: `click`, `requests` (auto-installed)

> ✅ The action installs dependencies automatically on Ubuntu, RHEL, and macOS runners.

---

## 💡 Notes

- `page-title` is combined with the current date for uniqueness:  
  e.g. `"Weekly Report - 2025-06-26"`
- Make sure your `PAT` has permissions to create pages in the target space.
- If your Markdown includes images or attachments, ensure they are accessible or embedded.

---

## 👤 Author

**GitHub:** [nickkostov](https://github.com/nickkostov)

---

## 🪪 License

MIT © [nickkostov](https://github.com/nickkostov)
