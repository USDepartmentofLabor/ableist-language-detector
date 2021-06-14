"""Main module for identifying ableist language in job descriptions."""

from typing import Iterable, List, Union

import click
import spacy

from ability_skills_decoder import utils
from ability_skills_decoder.ableist_word_list import (
    ABLEIST_OBJECTS,
    ABLEIST_VERBS,
    ABLEIST_VERBS_OBJECT_DEPENDENT,
)

nlp = spacy.load("en_core_web_sm")


def match_dependent_ableist_verbs(
    spacy_doc: spacy.tokens.Doc,
    ableist_verbs_object_dependent: Iterable[str],
    ableist_objects: Iterable[str],
) -> List[spacy.tokens.Span]:
    """Given a document and a list of verbs and objects, return the verb phrase spans
    that match any combination of the verb and the object.

    Parameters
    ----------
    spacy_doc : spacy.tokens.Doc
        spacy doc
    ableist_verbs_object_dependent : Iterable[str]
        List of verbs to search for
    ableist_objects : Iterable[str]
        List of objects to search for

    Returns
    -------
    Iterable[spacy.tokens.Span]
        Matched spans
    """
    matched_phrases = []
    # reference on parsing spacy dependency trees:
    #  https://spacy.io/usage/linguistic-features#navigating
    for token in spacy_doc:
        # iterate through tokens in the doc and look for matched objects; if an object
        # matches, check its head verb and see if it matches
        if token.dep_ == "dobj" and token.lemma_ in ableist_objects:
            if (
                utils.is_verb(token.head)  # each object has a head verb
                and token.head.lemma_ in ableist_verbs_object_dependent
            ):
                # if a match, return the full verb phrase.
                # right_edge is the rightmost edge of the token's syntactic descendants
                # could also get the head token's right edge via token.head.right_edge
                # (i.e. the right edge of the verb phrase, but this may be too expansive
                # and include modifiers that we don't need -
                # "move your hands repeatedly" instead of "move your hands")
                matched_phrase = spacy_doc[
                    token.head.i : token.right_edge.i + 1
                ]  # probably the best one to return the verb + object
                matched_phrases.append(matched_phrase)
    return matched_phrases


def find_ableist_language(
    job_description_text: str,
) -> List[Union[spacy.tokens.Span, spacy.tokens.Token]]:
    """For a given job description document, return a list of the matched ableist
    verbs and verb phrases as spacy objects.

    Parameters
    ----------
    job_description_text : str
        Job description text

    Returns
    -------
    List[Union[spacy.tokens.Span, spacy.tokens.Token]]
        List of matched ableist verbs and verb phrases as spacy objects; each contains
        data on the text form, lemma, and position of the verb/phrase in the document
    """
    # Read in jd and convert to spacy doc
    job_description_doc = nlp(job_description_text)

    # Match verbs in ableist verb list
    # TODO: this might be faster if we use a matcher object?
    jd_verbs = utils.get_verbs(job_description_doc)
    matched_verbs = [verb for verb in jd_verbs if verb.lemma_ in ABLEIST_VERBS]

    # Match verb + object in ableist verb + object list
    matched_verb_phrases = match_dependent_ableist_verbs(
        job_description_doc, ABLEIST_VERBS_OBJECT_DEPENDENT, ABLEIST_OBJECTS
    )

    # Return the ableist tokens & spans
    # TODO: look up suggested alternatives and return that as well?
    return matched_verbs + matched_verb_phrases


@click.command()
@click.option(
    "--job_description_file",
    "-j",
    type=str,
    required=True,
    help="Path to file containing the job description text.",
)
def main(job_description_file):
    """Extract ableist terms from a job description."""
    with open(job_description_file, "r") as jd_file:
        job_description_text = jd_file.read()

    result = find_ableist_language(job_description_text)
    for ableist_term in result:
        if isinstance(ableist_term, spacy.tokens.Span):
            print(
                f"PHRASE: {ableist_term} | LEMMA: {ableist_term.lemma_} | "
                f"POSITION: {ableist_term.start}:{ableist_term.end}"
            )
        else:
            print(
                f"PHRASE: {ableist_term} | LEMMA: {ableist_term.lemma_} | "
                f"POSITION: {ableist_term.i}"
            )


if __name__ == "__main__":
    main()
