
from python.ace_llm_logic.__main__ import (
    llm_rewrite_to_ace_english,
    llm_adjust_logic,
    process_sentence,
)

def test_rewrite_mockable():
    sentence = "The report was written by Alice after she reviewed the data."
    rewritten = llm_rewrite_to_ace_english(sentence)
    assert "writes" in rewritten.lower() or "write" in rewritten.lower()

def test_adjust_logic_mockable():
    original = "The report was written by Alice after she reviewed the data."
    dummy_logic = "write(alice, report1). review(alice, data1)."
    adjusted = llm_adjust_logic(original, dummy_logic)
    assert "past" in adjusted.lower() or "passive" in adjusted.lower()

def test_end_to_end_mock():
    sentence = "The report was written by Alice after she reviewed the data."
    logic = process_sentence(sentence, endpoint="localhost:0", mock=True)
    assert "write" in logic and "report" in logic
