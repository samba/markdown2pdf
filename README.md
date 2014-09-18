# Generate PDF Documents from Markdown files

Should be pretty self-explanatory.

Supports syntax highlighting via Pygments.


## Usage

From the command-line:

```shell
python -m markdown2pdf -i markdown_file.md -o output.pdf
```

As a Python module:

```python
import markdown2pdf

print markdown2pdf.prepare("./markdown_file.md")

```


## Thanks

- Rich Leland for <https://github.com/richleland/pygments-css>
- Chris Glass for <https://github.com/chrisglass/xhtml2pdf>
- Trent Mick for <https://github.com/trentm/python-markdown2>
