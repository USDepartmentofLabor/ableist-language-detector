"""Main module for identifying ableist language in job descriptions."""

from dataclasses import dataclass
from typing import List, Union

import click
import spacy

from ableist_language_detector.ableist_word_list import ABLEIST_VERBS, AbleistLanguage

nlp = spacy.load("en_core_web_sm")


@dataclass
class AbleistLanguageMatch:
    """Dataclass to store match results and associated wordlist data."""

    text: str
    lemma: str
    start: int
    end: int
    data: AbleistLanguage

    def __repr__(self):
        return self.text


def match_ableist_verbs(
    spacy_doc: spacy.tokens.Doc,
    ableist_verbs: dict[str, AbleistLanguage],
) -> List[spacy.tokens.Span]:
    """Given a document and a collection of ableist verb data objects, return the
    doc spans that match any of the ableist verbs. Do not check for grammatical
    objects.

    Parameters
    ----------
    spacy_doc : spacy.tokens.Doc
        spacy doc
    ableist_verbs : dict[str, AbleistLanguage]
        Collection of ableist verbs to search for, where the key is the string
        representation of the verb and the value is the dataclass object containing
        the verb's data

    Returns
    -------
    List[spacy.tokens.Span]
        Matched spans
    """
    matcher = spacy.matcher.Matcher(nlp.vocab)
    matcher.add(
        "verb_rule",
        [
            [
                {
                    "LEMMA": {"IN": list(ableist_verbs.keys())},
                    "POS": "VERB",
                    "DEP": {"NOT_IN": ["aux", "auxpass", "neg"]},
                },
            ]
        ],
    )
    verb_matches = [spacy_doc[start:end] for _, start, end in matcher(spacy_doc)]
    return verb_matches


def match_dependent_ableist_verbs(
    spacy_doc: spacy.tokens.Doc,
    ableist_verbs: dict[str, AbleistLanguage],
    return_search_verbs: bool = False,
) -> Union[List[spacy.tokens.Span], List[tuple[spacy.tokens.Span, spacy.tokens.Span]]]:
    """Given a document and a collection of ableist verb data objects that are
    dependent on the verb-object relationship, return the doc spans that match any of
    the ableist verbs and their grammatical objects.

    Parameters
    ----------
    spacy_doc : spacy.tokens.Doc
        spacy doc
    ableist_verbs : dict[str, AbleistLanguage]
        Collection of ableist verbs to search for, where the key is the string
        representation of the verb and the value is the dataclass object containing
        the verb's data
    return_search_verbs : bool, optional
        If true, return a tuple where the first element is the original search term
        and the second is the matched results. If false, return the matched results
        only, by default False

    Returns
    -------
    Union[List[spacy.tokens.Span], List[tuple[spacy.tokens.Span, spacy.tokens.Span]]]
        Matched spans or tuple containing the search term and matched spans
    """
    matcher = spacy.matcher.DependencyMatcher(nlp.vocab)
    dep_obj_pattern = []
    for verb, verb_data in ableist_verbs.items():
        # dependencymatcher docs: https://spacy.io/api/dependencymatcher
        pattern = [
            # pattern always starts with a "right_id" anchor, which is the verb
            {"RIGHT_ID": f"anchor_{verb}", "RIGHT_ATTRS": {"LEMMA": verb}},
            # match direct objects of the verb
            {
                "LEFT_ID": f"anchor_{verb}",
                "REL_OP": ">",  # looks for the head relationship
                "RIGHT_ID": f"{verb}_object",
                "RIGHT_ATTRS": {"DEP": "dobj", "LEMMA": {"IN": verb_data.objects}},
            },
        ]
        dep_obj_pattern.append(pattern)
    matcher.add("dep_verb_rule", dep_obj_pattern)
    # return the entire span from verb to object, which includes any interim modifiers
    matches = matcher(spacy_doc)
    if return_search_verbs:
        return [
            (spacy_doc[token_ids[0]], spacy_doc[min(token_ids) : max(token_ids) + 1])
            for _, token_ids in matches
        ]
    else:
        return [
            spacy_doc[min(token_ids) : max(token_ids) + 1] for _, token_ids in matches
        ]


def find_ableist_language(
    job_description_text: str,
) -> List[AbleistLanguageMatch]:
    """For a given job description document, return a list of the matched ableist
    language phrases.

    Parameters
    ----------
    job_description_text : str
        Job description text

    Returns
    -------
    List[AbleistLanguageMatch]
        List of matched ableist language in the form of AbleistLanguageMatch dataclass
        instances
    """
    # Read in jd and convert to spacy doc
    job_description_doc = nlp(job_description_text)

    matched_results = []

    # Match verbs in ableist verb list
    ableist_verbs_non_obj_dep = {
        verb: verb_data
        for verb, verb_data in ABLEIST_VERBS.items()
        if not verb_data.object_dependent
    }
    for match in match_ableist_verbs(job_description_doc, ableist_verbs_non_obj_dep):
        matched_results.append(
            AbleistLanguageMatch(
                lemma=match.lemma_,
                text=match.text,
                start=match.start,
                end=match.end,
                data=ABLEIST_VERBS[match.lemma_],
            )
        )

    # Match verbs that depend on objects, if present in the word list
    # A little repetitive, but need to use the original search term to access the data
    # in AbleistLanguage since these are phrases and not just exact matches
    ableist_verbs_obj_dep = {
        verb: verb_data
        for verb, verb_data in ABLEIST_VERBS.items()
        if verb_data.object_dependent
    }
    if len(ableist_verbs_obj_dep) > 0:
        for search_verb, match in match_dependent_ableist_verbs(
            job_description_doc, ableist_verbs_obj_dep, return_search_verbs=True
        ):
            matched_results.append(
                AbleistLanguageMatch(
                    lemma=match.lemma_,
                    text=match.text,
                    start=match.start,
                    end=match.end,
                    data=ABLEIST_VERBS[search_verb.lemma_],
                )
            )
    return matched_results


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
    print(f"Found {len(result)} instances of ableist language.\n")
    if len(result) > 0:
        for i, ableist_term in enumerate(result):
            print(
                f"Match #{i+1}\n"
                f"PHRASE: {ableist_term} | LEMMA: {ableist_term.lemma} | "
                f"POSITION: {ableist_term.start}:{ableist_term.end} | "
                f"ALTERNATIVES: {ableist_term.data.alternative_verbs} | "
                f"EXAMPLE: {ableist_term.data.example}\n"
            )


if __name__ == "__main__":
    main()
