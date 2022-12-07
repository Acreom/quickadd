from datetime import datetime

import pytest

from ctparse.corpus import (
    TimeParseEntry,
    load_timeparse_corpus,
    make_partial_rule_dataset,
    parse_nb_string,
    run_corpus,
)
from ctparse.scorer import DummyScorer
from ctparse.time.corpus import corpus
from ctparse.types import Interval, Time

CORPUS_JSON = """
[
 {
  "text": "Donnerstag, den 05.10. ca 6:55",
  "ref_time": "2017-09-25T16:06:55",
  "date_format": "EU",
  "gold_parse": "Time[]{2017-10-05 06:55 (X/X)}",
  "language": "de"
 },
 {
  "text": "22.05.2017 früh",
  "ref_time": "2017-05-16T05:42:09",
  "date_format": "EU",
  "gold_parse": "Time[]{2017-05-22 X:X (X/earlymorning)}",
  "language": "de"
 }
]
"""


def test_run_corpus() -> None:
    """The corpus passes if ctparse generates the desired
    solution for each test at least once. Otherwise it fails.
    """
    X, y = run_corpus(corpus)
    assert isinstance(y[0], bool)
    assert isinstance(X[0][0], str)


def test_run_corpus_failure() -> None:
    fail_corpus = [("never produced", "2015-12-12T12:30", ("today", "heute"))]
    with pytest.raises(Exception):
        run_corpus(fail_corpus)


def test_make_partial_rule_dataset() -> None:
    ts = datetime(year=2019, month=10, day=1)
    date_format = "EU"
    entries = [
        TimeParseEntry(
            "today at 5 pm", ts, date_format, Time(year=2019, month=10, day=1, hour=17, minute=0)
        )
    ]

    X, y = zip(
        *make_partial_rule_dataset(
            entries, timeout=0, max_stack_depth=0, scorer=DummyScorer()
        )
    )
    assert isinstance(y[0], bool)
    assert isinstance(X[0][0], str)


def test_parse_nb_string() -> None:
    t = Time(year=1, month=1, day=1, hour=1, minute=1, DOW=1, POD="pod")

    assert t == parse_nb_string("Time[]{0001-01-01 01:01 (1/pod)}")
    assert Interval(Time(), Time()) == parse_nb_string(
        "Interval[]{X-X-X X:X (X/X) - X-X-X X:X (X/X)}"
    )


def test_load_timeparse_corpus(tmp_path) -> None:
    path = tmp_path / "test.json"
    path.write_text(CORPUS_JSON, encoding="utf-8")

    result = load_timeparse_corpus(str(path))

    assert len(result) == 2
