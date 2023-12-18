from __future__ import annotations

import re
import xml.etree.ElementTree as etree

from markdown import Markdown, util
from markdown.blockprocessors import BlockQuoteProcessor
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


# Based on https://github.com/Python-Markdown/markdown/blob/4acb949256adc535d6e6cd84c4fb47db8dda2f46/markdown/blockprocessors.py#L277
class _CalloutsBlockProcessor(BlockQuoteProcessor):
    REGEX = re.compile(r"(^ {0,3}>([!?])? ?|\A)([A-Z]{2,}):([ \n])(.*)", flags=re.M)

    def test(self, parent: etree.Element, block: str) -> bool:
        m = self.REGEX.search(block)
        return (
            m is not None
            and (m[1] or not self.parser.state.isstate("blockquote"))
            and not util.nearing_recursion_limit()  # type: ignore
        )

    def run(self, parent: etree.Element, blocks: list[str]) -> None:
        block = blocks.pop(0)
        m = self.REGEX.search(block)
        if not m:
            return

        before = block[: m.start()]
        self.parser.parseBlocks(parent, [before])
        block = block[m.start(5) :]
        if m[1]:
            block = "\n".join(self.clean(line) for line in block.split("\n"))
        kind = m[3]

        if m[2]:
            admon = etree.SubElement(parent, "details", {"class": kind.lower()})
            if m[2] == "!":
                admon.set("open", "open")
        else:
            admon = etree.SubElement(parent, "details", {"class": "admonition " + kind.lower()})
        title = etree.SubElement(admon, "summary", {"class": "admonition-title"})
        title.text = kind.title()

        self.parser.state.set("blockquote")
        self.parser.parseChunk(admon, block)
        self.parser.state.reset()

        if m[4] == "\n":
            admon[1].text = "\n" + (admon[1].text or "")


class _CalloutsTreeprocessor(Treeprocessor):
    def __init__(self, strip_period: bool) -> None:
        super().__init__()
        self.strip_period = strip_period

    def run(self, doc: etree.Element):
        for root in doc.iter("details"):
            # Expecting this:
            #     <details class="admonition note">
            #       <summary class="admonition-title">Note</summary>
            #       <p><strong>Custom title.</strong> Body</p>
            #     </details>
            # And turning it into this:
            #     <details class="note">
            #       <summary>Custom title</summary>
            #       <p>Body</p>
            #     </div>
            # Or this:
            #     <div class="admonition note">
            #       <p class="admonition-title">Custom title</p>
            #       <p>Body</p>
            #     </div>
            if not root.get("class"):
                continue
            title = root[0]
            if title.tag != "summary" or title.get("class") != "admonition-title":
                continue

            # Change <details> back to <div> if it was a normal admonition.
            if root.get("class", "").startswith("admonition "):
                root.tag = "div"
                title.tag = "p"
            else:
                title.attrib.pop("class", None)

            # Find the first paragraph and a <strong> element in it.
            if len(root) < 2:
                continue
            paragraph = root[1]
            if (
                paragraph.tag != "p"
                or not len(paragraph)
                or (paragraph.text and paragraph.text.strip())
            ):
                continue
            strong = paragraph[0]
            if strong.tag != "strong":
                continue
            if paragraph.text == "\n":
                continue

            # Move everything from the bold element into the title.
            title.text = strong.text and strong.text.lstrip()
            title[:] = strong
            # Remove last dot at the end of the text (which might instead be the last child's tail).
            if len(title):  # Has any child elements
                last = title[-1]
                if last.tail:
                    last.tail = last.tail.rstrip()
                    if self.strip_period and last.tail.endswith("."):
                        last.tail = last.tail[:-1]
            else:
                if title.text:
                    title.text = title.text.rstrip()
                    if self.strip_period and title.text.endswith("."):
                        title.text = title.text[:-1]
            # Make sure any text immediately following the bold element isn't lost.
            if strong.tail:
                paragraph.text = (paragraph.text or "") + strong.tail
            # Finally, remove the original element, also drop a possible linebreak afterwards.
            paragraph.remove(strong)
            if len(paragraph) and not paragraph.text:
                br = paragraph[0]
                if br.tag == "br":
                    paragraph.text = br.tail
                    paragraph.remove(br)
            if not len(paragraph) and not paragraph.text and not paragraph.tail:
                root.remove(paragraph)


class CalloutsExtension(Extension):
    def __init__(self, **kwargs) -> None:
        self.config = {
            "strip_period": [
                True,
                "Remove the period (dot '.') at the end of custom titles - Default: True",
            ],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        parser = md.parser  # type: ignore
        parser.blockprocessors.register(
            _CalloutsBlockProcessor(parser),
            "callouts",
            21,  # Right before blockquote
        )
        md.treeprocessors.register(
            _CalloutsTreeprocessor(self.getConfig("strip_period")),
            "callouts",
            19,  # Right after inline
        )


makeExtension = CalloutsExtension
