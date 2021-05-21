# markdown-callouts

**Extension for [Python-Markdown][]: a classier syntax for [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#usage)**

[python-markdown]: https://python-markdown.github.io/
[admonition]: https://python-markdown.github.io/extensions/admonition/
[mkdocs]: https://www.mkdocs.org/

## Installation

```shell
pip install markdown-callouts
```

 *  If using MkDocs, [enable the extension in **mkdocs.yml**](https://www.mkdocs.org/user-guide/configuration/#markdown_extensions):

    ```yaml
    markdown_extensions:
      - callouts
    ```

 *  If using [Python-Markdown][] in some other way, [see its reference](https://python-markdown.github.io/extensions/). You can add this extension to the list of plugins:

     *  as a string: `'callouts'`
     *  as an object: `from markdown_callouts import CalloutsExtension`

The extension has no configuration options.

## Usage

This adds a new block-level syntax to Markdown, to put a paragraph of text into a block that's specially highlighted and set apart from the rest of the text.

The syntax is: as the start of a paragraph, write a word in all capital letters, followed by a colon and a space. Then the rest of the text in that block will be used as the body of the "callout".

For example, to get this ([using *mkdocs-material* theme](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#usage)):

NOTE: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
massa, nec semper lorem quam in massa.

<table markdown="1">
<tr><td>
Write this Markdown with the "callouts" extension:
</td><td>

```markdown
NOTE: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
massa, nec semper lorem quam in massa.
```

</td></tr>
<tr><td>
Rather than this (with the "admonition" extension):
</td><td>

```markdown
!!! note
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
```

</td></tr>
</table>

The titular word of the callout, transformed from all-caps to just capitalized, becomes the title for the set-apart text.

#### Output

The produced HTML is the same with both extensions:

```html
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
massa, nec semper lorem quam in massa.</p>
</div>
```

You may notice that the HTML contains no explicit styling whatsoever. That is because that's supposed to be handled through CSS that accompanies it. In case of MkDocs, that's handled by themes -- if they choose to support styling for the classes `.admonition`, `.admonition-title`, etc.

In addition to the always-present class `admonition`, another CSS class will be added that is equal to the title of the "callout", in lowercase. The stylesheet can then choose to specially distinguish the style for a few select identifiers out of those. ([Example theme](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types))

### Syntax details

At the start of a block, there needs to be a word in all English capital letters, followed by a colon, space, then other text.

=== "Markdown"
    ```markdown
    Previous block will not be picked up.

    EXAMPLE: This text
    is all part of a single
    *admonition* block.

    Next block will not be picked up.
    ```

=== "Result"
    Previous block will not be picked up.

    EXAMPLE: This text
    is all part of a single
    *admonition* block.

    Next block will not be picked up.

=== "HTML"
    ```html
    <p>Previous block will not be picked up.</p>
    <div class="admonition example">
    <p class="admonition-title">Example</p>
    <p>This text
    is all part of a single
    <em>admonition</em> block.</p>
    </div>
    <p>Next block will not be picked up.</p>
    ```

Inline Markdown (links, italics, etc.) is handled normally for the rest of the text. Block-level Markdown (lists, quotes, etc.) is not allowed.

#### Block-level syntax

To allow putting multiple paragraphs into the same callout and enable all of Markdown features, use the block-level syntax, which works the same as a [blockquote](https://daringfireball.net/projects/markdown/syntax#blockquote), but with the mandatory all-caps word at the beginning of it:

=== "Markdown"
    ```markdown
    > EXAMPLE: Hello world!
    >
    > * Item 1
    > * Item 2
    >
    > Still going...

    Next block will not be picked up.
    ```

=== "Result"
    > EXAMPLE: Hello world!
    >
    > * Item 1
    > * Item 2
    >
    > Still going...

    Next block will not be picked up.

=== "HTML"
    ```html
    <div class="admonition example">
    <p class="admonition-title">Example</p>
    <p>Hello world!</p>
    <ul>
    <li>Item 1</li>
    <li>Item 2</li>
    </ul>
    <p>Still going...</p>
    </div>
    <p>Next block will not be picked up.</p>
    ```

The fact that we used blockquote syntax doesn't mean any actual blockquote is involved, this is still just an admonition. We are just making a clear delineation for the block, but otherwise the angle quotes are discarded.

However... if you'll also be viewing the same Markdown through a renderer that doesn't support this special syntax, it will indeed be a blockquote -- that is [graceful degradation](#project-goals).

??? "Compare this to the [Admonition][] extension"

    === "Markdown"
        ```markdown
        !!! example
            Hello world!

            * Item 1
            * Item 2

            Still going...

        Next block will not be picked up.
        ```

    === "Result without extensions"
        !!! example
            Hello world!

            * Item 1
            * Item 2

            Still going...

        Next block will not be picked up.

You can find more examples (particularly how edge cases are handled) in the [test cases directory](https://github.com/oprypin/markdown-callouts/tree/master/tests/extension).

## Further features

Actually that's all! See also: [Project goals](#project-goals).

### Custom titles

Not supported at the moment, mainly because the syntax choice for it can be controversial. Currently the title of the admonition will always be the titular word of the callout as written. If you need a custom title, you can still use the *[admonition][]*   extension alongside.

### Custom look

As [mentioned](#output), styling is handled through CSS, not from the extension itself. And in CSS, you can indeed completely re-define the look for each particular keyword. Adding a new keyword requires no action, other than possibly adding CSS for it.

This is well documented [for *mkdocs-material* theme](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#custom-admonitions).
And see another example for inspiration: [Source](https://github.com/mkdocstrings/crystal/commit/53db1592e771eb0d918b1aafbd52eb7111479f75#diff-607e5fcb5247b2ab8b856864d7dc86fa66f24d82cb5b7ef2269a522344b650e2) &rarr; [Result](https://mkdocstrings.github.io/crystal/extras.html#callouts-extension)

## Project goals

The goal of this project is to have a **subset** of features of the [admonition][] extension, under an alternate syntax that allows for **graceful degradation**.
