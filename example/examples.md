# Usage Examples

Prepare the configuration:

```yaml
book:
  title: Generating PDFs from Markdown
  author: Sam Briesemeister
  subject: Making beautiful, packaged publications from technical text-based formats
  parts:
    - summary.md
    - README.md
    - how_it_works.md
```

Compile the document

```bash
python -m markdown2pdf -c example.yaml -o output.pdf
```

