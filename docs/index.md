# markdown-callouts

**Extension for [Python-Markdown][]: a classier syntax for [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#usage) and [collapsible blocks](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#collapsible-blocks)**

[python-markdown]: https://python-markdown.github.io/
[admonition]: https://python-markdown.github.io/extensions/admonition/
[details]: https://facelessuser.github.io/pymdown-extensions/extensions/details/
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

The extension is configurable as such:

* `strip_period` (default `true`) - whether to strip the final period from [custom titles](#custom-titles) syntax.

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

### Custom titles

If you don't like the deduced title text, you can specify a title of your own, after the all-caps word. For purposes of [graceful degradation](#project-goals), the syntax is exactly as if you wrote one sentence emphasized in bold at the start of the callout.

For example, to get this:

TIP: **Writing custom titles.**
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
massa, nec semper lorem quam in massa.

<table markdown="1">
<tr><td>
Write this Markdown with the "callouts" extension:
</td><td>

```markdown
TIP: **Writing custom titles.**
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
massa, nec semper lorem quam in massa.
```

</td></tr>
<tr><td>
Rather than this (with the "admonition" extension):
</td><td>

```markdown
!!! tip "Writing custom titles"
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
```

</td></tr>
</table>

The linebreak after the title is optional. And it can be an actual linebreak with two spaces at the end of the line as well -- that has no effect on the output, but again can be relevant for [graceful degradation](#project-goals).

??? note "About the period at the end of the sentence"
    The period at the end of the sentence is always dropped from the final title. You are encouraged to write those periods anyway, because when using a "vanilla" renderer, the output will look weird.

    === "Markdown"
        ```markdown
        NOTE: **A few more thoughts** Lorem ipsum dolor sit amet, consectetur adipiscing elit.

        NOTE: **A few more thoughts.** Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        ```

    === "Intended result"
        NOTE: **A few more thoughts** Lorem ipsum dolor sit amet, consectetur adipiscing elit.

        NOTE: **A few more thoughts.** Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    === "Result with vanilla Markdown"
        NOTE:  **A few more thoughts**  Lorem ipsum dolor sit amet, consectetur adipiscing elit.

        NOTE:  **A few more thoughts.**  Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    If you want to keep the period in the title, you can escape it with a backslash.
    And to *always* keep periods in the titles, configure the extension with `strip_period: false`.

### Collapsible blocks

(See first: [Block-level syntax](#block-level-syntax))

To get the following collapsed `<details>` block, just add a question mark right after the blockquote symbol:

??? tip "Click me to read more"
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.

    Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa, nec
    semper lorem quam in massa.

<table markdown="1">
<tr><td>
Write this Markdown with the "callouts" extension:
</td><td>

```markdown
>? TIP: **Click me to read more.**
>
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.
>
> Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa, nec
> semper lorem quam in massa.
```

</td></tr>
<tr><td>
Rather than this (with the "details" extension):
</td><td>

```markdown
??? tip "Click me to read more"
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.

    Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa, nec
    semper lorem quam in massa.
```

</td></tr>
</table>

The block can alternatively be initially open. Just write `>!` instead of `>?`.

### Output

The produced HTML is the same with [both][admonition] [extensions][details] that this replaces:

=== "Same as 'admonition'"

    ```html
    <div class="admonition note">
    <p class="admonition-title">Note</p>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.</p>
    </div>
    ```

=== "Same as 'details'"

    ```html
    <details class="note">
    <summary>Note</summary>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.</p>
    </details>
    ```

You may notice that the HTML contains no explicit styling whatsoever. That is because that's supposed to be handled through CSS that accompanies it. In case of MkDocs, that's handled by themes -- if they choose to support styling for the classes `.admonition`, `.admonition-title` or the tags `details`, `summary`.

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

The space after the colon can instead be a newline as well.

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

However... if you'll also be viewing the same Markdown through a renderer that doesn't support this special syntax, it will indeed be a blockquote -- that is also [graceful degradation](#project-goals).

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

#### Collapsible block syntax

Collapsible block syntax is a simple extension of the block syntax.  
Instead of opening the blockquote with `>`:

* write `>?` to get a `<details>` tag;
* write `>!` to get a `<details open>` tag.

To allow putting multiple paragraphs into the same callout and enable all of Markdown features, use the block-level syntax, which works the same as a [blockquote](https://daringfireball.net/projects/markdown/syntax#blockquote), but with the mandatory all-caps word at the beginning of it:

=== "Markdown"
    ```markdown
    >? EXAMPLE: Hello world!
    >
    > * Item 1
    > * Item 2
    >
    > Still going...

    Next block will not be picked up.
    ```

=== "Result"
    >? EXAMPLE: Hello world!
    >
    > * Item 1
    > * Item 2
    >
    > Still going...

    Next block will not be picked up.

=== "HTML"
    ```html
    <details class="example">
    <summary>Example</summary>
    <p>Hello world!</p>
    <ul>
    <li>Item 1</li>
    <li>Item 2</li>
    </ul>
    <p>Still going...</p>
    </details>
    ```

You can find more examples (particularly how edge cases are handled) in the [test cases directory](https://github.com/oprypin/markdown-callouts/tree/master/tests/details).

#### Custom titles

A callout block with a custom title is just an extension of the base syntax, where after the capital word and a colon, the first item of the main body must be in bold. This `**strong emphasis**` syntax (or also with `__`) is directly used as the delimitation for the title, according to normal rules of how Markdown handles it. The actual `<strong>` tag will be excluded from the output and its contents will be moved from the paragraph and become the title instead. You can use any inline Markdown formatting within that main delimiter, and *that* will be preserved. Single newlines are allowed within the delimited title part, again as per normal Markdown rules.

You can find more examples (particularly how edge cases are handled) in the [test cases directory](https://github.com/oprypin/markdown-callouts/tree/master/tests/extension/title).

#### Avoiding callouts syntax

There are several ways of avoiding triggering the "callouts" syntax, in case you actually want to just write a word in all-capital letters followed by a colon.

In that case, precede the line with one space (which will not be represented in the final HTML):

```markdown
 EXAMPLE: Hi.
```

And if you happen to need to start your callout with a sentence in bold (without picking it up as the title), make sure to put a newline first:

=== "Markdown"
    ```markdown
    NOTE: **This is a title.** Body.

    NOTE:
    **Not a title actually.** Body.
    ```

=== "Result"
    NOTE: **This is a title.** Body.

    NOTE:
    **Not a title actually.** Body.

## Further features

### Custom look

As [mentioned](#output), styling is handled through CSS, not from the extension itself. And in CSS, you can indeed completely re-define the look for each particular keyword. Adding a new keyword requires no action, other than possibly adding CSS for it.

This is well documented [for *mkdocs-material* theme](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#custom-admonitions).
And see another example for inspiration: [Source](https://github.com/mkdocstrings/crystal/commit/53db1592e771eb0d918b1aafbd52eb7111479f75#diff-607e5fcb5247b2ab8b856864d7dc86fa66f24d82cb5b7ef2269a522344b650e2) &rarr; [Result](https://mkdocstrings.github.io/crystal/extras.html#callouts-extension)

## Project goals

The goal of this project is to support the same features as the [admonition][] extension, under an alternate syntax that allows for **graceful degradation** (you can search for mentions of that on this page). That means that the page can be previewed in a "vanilla" Markdown renderer and still look fully legible, though missing some styling. That can be useful to keep your documents nicely viewable on Web source hosting such as GitHub even if that won't be your primary hosting.
