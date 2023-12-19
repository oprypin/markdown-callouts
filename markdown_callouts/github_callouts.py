from __future__ import annotations

import re
import xml.etree.ElementTree as etree

from markdown import Markdown, util
from markdown.blockprocessors import BlockQuoteProcessor
from markdown.extensions import Extension


# Based on https://github.com/Python-Markdown/markdown/blob/4acb949256adc535d6e6cd84c4fb47db8dda2f46/markdown/blockprocessors.py#L277
class _GitHubCalloutsBlockProcessor(BlockQuoteProcessor):
    REGEX = re.compile(
        r"((?:^|\n) *(?:[^>].*)?(?:^|\n)) {0,3}> *\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\] *\n(?: *> *\n)*() *(?:> *[^\s\n]|[^\s\n>])",
        flags=re.IGNORECASE,
    )

    def test(self, parent, block):
        return (
            bool(self.REGEX.search(block))
            and not self.parser.state.isstate("blockquote")
            and not util.nearing_recursion_limit()
        )

    def run(self, parent: etree.Element, blocks: list[str]) -> None:
        block = blocks.pop(0)
        m = self.REGEX.search(block)
        assert m

        before = block[: m.end(1)]
        block = "\n".join(self.clean(line) for line in block[m.end(3) :].split("\n"))
        self.parser.parseBlocks(parent, [before])
        kind = m[2]

        css_class = kind.lower()
        if css_class == "caution":
            css_class = "danger"
        admon = etree.SubElement(parent, "div", {"class": "admonition " + css_class})
        title = etree.SubElement(admon, "p", {"class": "admonition-title"})
        title.text = kind.title()

        self.parser.state.set("blockquote")
        self.parser.parseChunk(admon, block)
        self.parser.state.reset()


class GitHubCalloutsExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        parser = md.parser  # type: ignore
        parser.blockprocessors.register(
            _GitHubCalloutsBlockProcessor(parser),
            "github-callouts",
            21.1,  # Right before blockquote
        )


makeExtension = GitHubCalloutsExtension
