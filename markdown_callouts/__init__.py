import re
import xml.etree.ElementTree as etree

from markdown import Markdown, util
from markdown.blockprocessors import BlockQuoteProcessor
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


# Based on https://github.com/Python-Markdown/markdown/blob/4acb949256adc535d6e6cd84c4fb47db8dda2f46/markdown/blockprocessors.py#L277
class _CalloutsBlockProcessor(BlockQuoteProcessor):
    REGEX = re.compile(r"(^ {0,3}> ?|\A)([A-Z]{2,}): (.*)", flags=re.M)

    def test(self, parent, block):
        m = self.REGEX.search(block)
        return (
            bool(m)
            and (m[1] or not self.parser.state.isstate("blockquote"))
            and not util.nearing_recursion_limit()
        )

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.REGEX.search(block)
        if m:
            before = block[: m.start()]
            self.parser.parseBlocks(parent, [before])
            block = block[m.start(3) :]
            if m[1]:
                block = "\n".join(self.clean(line) for line in block.split("\n"))

        admon = etree.SubElement(parent, "div", {"class": "admonition " + m[2].lower()})
        title = etree.SubElement(admon, "p", {"class": "admonition-title"})
        title.text = m[2].title()

        self.parser.state.set("blockquote")
        self.parser.parseChunk(admon, block)
        self.parser.state.reset()


class _CalloutsTreeprocessor(Treeprocessor):
    def run(self, doc):
        for div in doc:
            # <div class="admonition note">
            #   <p class="admonition-title">Note</p>
            #   <p><strong>Custom title.</strong> Body</p>
            # </div>
            if (
                div.tag != "div"
                or not div.get("class", "").startswith("admonition ")
                or len(div) < 2
            ):
                continue
            title, paragraph, *_ = div
            if title.tag != "p" or title.get("class") != "admonition-title":
                continue
            if paragraph.tag != "p" or len(paragraph) < 1:
                continue
            strong, *_ = paragraph
            if strong.tag != "strong":
                continue

            title.text = strong.text.strip().rstrip(".")
            if strong.tail:
                paragraph.text = (paragraph.text or "") + strong.tail
            paragraph.remove(strong)
            # <div class="admonition note">
            #   <p class="admonition-title">Custom title</p>
            #   <p> Body</p>
            # </div>


class CalloutsExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        parser = md.parser  # type: ignore
        parser.blockprocessors.register(
            _CalloutsBlockProcessor(parser), "callouts", 21  # Right before blockquote
        )
        md.treeprocessors.register(_CalloutsTreeprocessor(), "callouts", 19)  # Right after inline


makeExtension = CalloutsExtension
