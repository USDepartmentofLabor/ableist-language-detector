#!/usr/bin/env python

"""Tests for detector functions."""

import spacy

from ableist_language_detector import detector
from ableist_language_detector.ableist_word_list import AbleistLanguage

nlp = spacy.load("en_core_web_sm")


def test_match_dependent_ableist_verbs():
    """Test verb phrase (dependent verb + object) matching."""
    doc = nlp("must be able to move your hands repeatedly")
    ableist_verbs = {
        "move": AbleistLanguage(
            verb="move",
            object_dependent=True,
            alternative_verbs=["alt", "verbs"],
            example="",
            objects=["hand", "foot"],
        )
    }
    str_result = detector.match_dependent_ableist_verbs(doc, ableist_verbs)[0].text
    assert str_result == "move your hands"


def test_find_ableist_language():
    """Test verb and verb phrase matching.

    Note: This may fail if the sentences are too short because the parser won't be able
    to successfully recognize part of speech without context. For example, "lift heavy
    boxes" may not result in a match because "lift" can be both a verb and noun, and
    without enough context, the parser is not able to distinguish it as a verb.
    """
    doc = """
    requirements
    - must be able to move your hands repeatedly
    - type on a computer
    - comfortable with lifting heavy boxes
    - excellent communication skills
    - move your wrists in circles and bend your arms
    """
    matched_results = detector.find_ableist_language(doc)
    str_matched_results = [phrase.text for phrase in matched_results]
    expected_results = ["move your hands", "lifting", "move your wrists", "bend"]
    assert sorted(str_matched_results) == sorted(expected_results)
