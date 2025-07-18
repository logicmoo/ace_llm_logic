
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "python"))

from ace_llm_logic.__main__ import (
    llm_rewrite_to_ace_english,
    llm_adjust_logic,
    process_sentence,
    start_ape_http_server,
    stop_ape_http_server,
    parse_with_ace,
)

import time
import pytest


@pytest.fixture
def ape_server():
    """Spin up a temporary APE HTTP server for tests."""
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    ape_script = repo_root / "APE" / "ape.sh"
    proc, port = start_ape_http_server(str(ape_script))
    time.sleep(3)  # allow server to start
    endpoint = f"localhost:{port}"
    try:
        yield endpoint
    finally:
        stop_ape_http_server(proc)

def test_rewrite_live():
    sentence = "The report was written by Alice after she reviewed the data."
    rewritten = llm_rewrite_to_ace_english(sentence)
    assert "writes" in rewritten.lower() or "write" in rewritten.lower()

def test_adjust_logic_live():
    original = "The report was written by Alice after she reviewed the data."
    dummy_logic = "write(alice, report1). review(alice, data1)."
    adjusted = llm_adjust_logic(original, dummy_logic)
    assert "past" in adjusted.lower() or "passive" in adjusted.lower()

def test_end_to_end_real(ape_server):
    sentence = "The report was written by Alice after she reviewed the data."
    logic = process_sentence(sentence, endpoint=ape_server, mock=False)
    assert "write" in logic.lower() and "report" in logic.lower()


def test_bad_sentence_error_known(ape_server):
    result = parse_with_ace("Blah.", endpoint=ape_server)
    assert "<messages>" in result and "error" in result.lower()
