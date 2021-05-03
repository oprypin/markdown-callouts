import re
import xml.etree.ElementTree as etree

from markdown import Markdown, util
from markdown.blockprocessors import BlockQuoteProcessor
from markdown.extensions import Extension


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


class CalloutsExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        parser = md.parser  # type: ignore
        parser.blockprocessors.register(
            _CalloutsBlockProcessor(parser), "callouts", 21  # Right before blockquote
        )


makeExtension = CalloutsExtension
