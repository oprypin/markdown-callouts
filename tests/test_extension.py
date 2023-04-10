import re

import bs4
import pytest
from markdown import Markdown

from markdown_callouts import CalloutsExtension


@pytest.mark.golden_test("extension/**/*.yml")
def test_extension(golden):
    config = {k: golden[k] for k in ["strip_period"] if golden.get(k) is not None}
    md = Markdown(extensions=[CalloutsExtension(**config)])
    output = md.convert(golden["input"])
    soup = bs4.BeautifulSoup(output, features="html.parser")
    html = soup.prettify().rstrip("\n")
    html = re.sub(r"^( *)", r"\1\1", html, flags=re.M)
    assert html == golden.out["output"]
