import re

import bs4
import pytest
from markdown import Markdown

from markdown_callouts import CalloutsExtension


@pytest.mark.golden_test("extension/**/*.yml")
def test_extension(golden):
    md = Markdown(extensions=[CalloutsExtension()])
    output = md.convert(golden["input"])
    soup = bs4.BeautifulSoup(output, features="html.parser")
    html = soup.prettify()
    html = re.sub(r"^( *)", r"\1\1", html, flags=re.M)
    assert html == golden.out["output"]
