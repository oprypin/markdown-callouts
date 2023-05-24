import re

import bs4
import pytest
from markdown import Markdown

from markdown_callouts import CalloutsExtension

styles = {"callouts", "github"}


@pytest.mark.golden_test("callouts/**/*.yml", "github/**/*.yml", "all/**/*.yml")
def test_extension(request, golden):
    config = {k: golden[k] for k in ["strip_period"] if golden.get(k) is not None}
    main_styles = {s for s in styles if f"{s}/" in request.node.name or "all/" in request.node.name}
    for other_style in [set()] + [{s} for s in styles - main_styles]:
        config["syntax"] = main_styles | other_style
        md = Markdown(extensions=[CalloutsExtension(**config)])
        output = md.convert(golden["input"])
        soup = bs4.BeautifulSoup(output, features="html.parser")
        html = soup.prettify().rstrip("\n")
        html = re.sub(r"^( *)", r"\1\1", html, flags=re.M)
        assert html == golden.out["output"]
