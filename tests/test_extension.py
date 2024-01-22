import re

import bs4
import pytest
from markdown import Markdown

from markdown_callouts.callouts import CalloutsExtension
from markdown_callouts.github_callouts import GitHubCalloutsExtension

extension_styles = {
    "callouts": CalloutsExtension,
    "github": GitHubCalloutsExtension,
}


@pytest.mark.golden_test("callouts/**/*.yml", "github/**/*.yml", "all/**/*.yml")
def test_extension(request, golden):
    config = {k: golden[k] for k in ["strip_period"] if golden.get(k) is not None}
    extensions = [
        extension(**config)
        for key, extension in extension_styles.items()
        if f"{key}/" in request.node.name or "all/" in request.node.name
    ]
    md = Markdown(extensions=extensions)
    output = md.convert(golden["input"])
    soup = bs4.BeautifulSoup(output, features="html.parser")
    html = soup.prettify().rstrip("\n")
    html = re.sub(r"^( *)", r"\1\1", html, flags=re.M)
    assert html == golden.out["output"]
