# markdown-callouts

**Extension for [Python-Markdown][]: a classier syntax for [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#usage)**

[![PyPI](https://img.shields.io/pypi/v/markdown-callouts)](https://pypi.org/project/markdown-callouts/)
[![License](https://img.shields.io/github/license/oprypin/markdown-callouts)](https://github.com/oprypin/markdown-callouts/blob/master/LICENSE.md)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/oprypin/markdown-callouts/ci.yml.svg)](https://github.com/oprypin/markdown-callouts/actions?query=event%3Apush+branch%3Amaster)

[python-markdown]: https://python-markdown.github.io/
[admonition]: https://python-markdown.github.io/extensions/admonition/
[mkdocs]: https://www.mkdocs.org/
[documentation site]: https://oprypin.github.io/markdown-callouts/

## Installation

```shell
pip install markdown-callouts
```

If using MkDocs, [enable the extension in **mkdocs.yml**](https://www.mkdocs.org/user-guide/configuration/#markdown_extensions):

```yaml
markdown_extensions:
  - callouts
```

**Continue to the [documentation site][].**

## Usage

This adds a new block-level syntax to Markdown, to put a paragraph of text into a block that's specially highlighted and set apart from the rest of the text.

**Example:**

```markdown
NOTE: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
massa, nec semper lorem quam in massa.
```

**Result**, [using *mkdocs-material*](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#usage):

![Screenshot](https://user-images.githubusercontent.com/371383/119063216-dc001700-b9d8-11eb-8092-763e5d02d9f4.png)

Collapsible blocks also have a syntax for them:

```markdown
>? NOTE: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
> nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
> massa, nec semper lorem quam in massa.
```

This instead shows up as an initially-closed `<details>` block.

### Graceful degradation

This extension produces the same results as the *[admonition][]* extension, but with a syntax that is much less intrusive and has a very reasonable fallback look for "vanilla" renderers.

E.g. compare what you would've seen above if we actually wrote that Markdown and fed it to GitHub's Markdown parser:

<table markdown="1">
<tr><th>"Callouts" syntax</th></tr>
<tr><td>

NOTE: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
massa, nec semper lorem quam in massa.

</td></tr>
<tr><th>"Admonition" syntax</th></tr>
<tr><td>

!!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

</td></tr>
</table>

---

**Continue to the [documentation site][].**
