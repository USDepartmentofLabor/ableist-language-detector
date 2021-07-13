"""Module with NLP utility functions."""

from typing import List

import spacy


def is_verb(token: spacy.tokens.Token) -> bool:
    """Return True if the token is a non-auxiliary verb, else return False.

    Parameters
    ----------
    token : spacy.tokens.Token
        spacy token

    Returns
    -------
    bool
        True if the token is a non-auxiliary verb, else False
    """
    if token.pos_ == "VERB" and token.dep_ not in {"aux", "auxpass", "neg"}:
        return True
    return False


def is_object(token: spacy.tokens.Token) -> bool:
    """Return True if the token is a noun object, else return False.

    Parameters
    ----------
    token : spacy.tokens.Token
        spacy token

    Returns
    -------
    bool
        True if the token is a noun object, else False
    """
    if token.pos_ == "NOUN" and token.dep_ == "dobj":  # direct object dependency tag
        return True
    return False


def get_verbs(spacy_doc: spacy.tokens.Doc) -> List[spacy.tokens.Token]:
    """Return a list of verb lemmas within a given document.

    Parameters
    ----------
    spacy_doc : spacy.tokens.Doc
        spaCy document to parse

    Returns
    -------
    List[spacy.tokens.Token]]
        A list of tokens
    """
    return [token for token in spacy_doc if is_verb(token)]


def get_objects(spacy_doc: spacy.tokens.Doc) -> List[spacy.tokens.Token]:
    """Return a list of noun objects within a given document.

    Parameters
    ----------
    spacy_doc : spacy.tokens.Doc
        spaCy document to parse

    Returns
    -------
    List[spacy.tokens.Token]
        A list of tokens
    """
    return [token for token in spacy_doc if is_object(token)]


def get_nouns(spacy_doc: spacy.tokens.Doc) -> List[spacy.tokens.Token]:
    """Return a list of noun tokens within a given document.

    Parameters
    ----------
    spacy_doc : spacy.tokens.Doc
        spaCy document to parse

    Returns
    -------
    List[spacy.tokens.Token]
        A list of tokens
    """
    return [token for token in spacy_doc if token.pos_ == "NOUN"]
