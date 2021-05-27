"""Module with NLP utility functions."""

from typing import List, Union
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


def get_verbs(
    spacy_doc: spacy.tokens.Doc, return_lemma: bool = True
) -> List[Union[str, spacy.tokens.Token]]:
    """Return a list of verb lemmas within a given document.

    Parameters
    ----------
    spacy_doc : spacy.tokens.Doc
        spaCy document to parse
    return_lemma : bool, optional
        If true, return the string lemmas instead of the spaCy token objects,
        by default True

    Returns
    -------
    List[Union[str, spacy.tokens.Token]]
        A list of tokens or string lemmas
    """
    verbs = [token for token in spacy_doc if is_verb(token)]
    if return_lemma:
        return [token.lemma_ for token in verbs]
    return verbs


def get_objects(
    spacy_doc: spacy.tokens.Doc, return_lemma: bool = True
) -> List[Union[str, spacy.tokens.Token]]:
    """Return a list of noun objects within a given document.

    Parameters
    ----------
    spacy_doc : spacy.tokens.Doc
        spaCy document to parse
    return_lemma : bool, optional
        If true, return the string lemmas instead of the spaCy token objects,
        by default True

    Returns
    -------
    List[Union[str, spacy.tokens.Token]]
        A list of tokens or string lemmas
    """
    noun_objects = [token for token in spacy_doc if is_object(token)]
    if return_lemma:
        return [token.lemma_ for token in noun_objects]
    return noun_objects


def get_nouns(
    spacy_doc: spacy.tokens.Doc, return_lemma: bool = True
) -> List[Union[str, spacy.tokens.Token]]:
    """Return a list of nouns within a given document.

    Parameters
    ----------
    spacy_doc : spacy.tokens.Doc
        spaCy document to parse
    return_lemma : bool, optional
        If true, return the string lemmas instead of the spaCy token objects,
        by default True

    Returns
    -------
    List[Union[str, spacy.tokens.Token]]
        A list of tokens or string lemmas
    """
    nouns = [token for token in spacy_doc if token.pos_ == "NOUN"]
    if return_lemma:
        return [token.lemma_ for token in nouns]
    return nouns
