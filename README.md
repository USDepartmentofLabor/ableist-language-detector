# [wip] ability-skills-decoder
Tool to identify ableist language in job descriptions.

**What is ableist language?**

> Ableist language is language that is offensive to people with disability. It can also refer to language that is derogatory, abusive or negative about disability. Ableism is the systemic exclusion and oppression of people with disability, often expressed and reinforced through language. [[source]](https://pwd.org.au/resources/disability-info/language-guide/ableist-language/)

**Why is this tool important?**

Ableist language in job descriptions can cause people with disabilities to feel excluded from jobs that they are qualified for. This typically occurs when a description includes requirements that describe physical abilities or demands instead of the outcome of the task that must be accomplished. By identifying ableist language and suggesting alternatives, this tool will support more inclusive hiring practices.

## Installation

Clone the repo and install the package in edit mode (preferably in a virtual environment).
```
git clone git@github.com:inclusive-ai/ability-skills-decoder.git
cd ability-skills-decoder
pip install -e .
```

Download spaCy dependencies.
```
python -m spacy download en_core_web_sm
```

**Developer Installation**

If you plan on contributing to the repo, complete these additional steps:

Install the dev requirements.

```
pip install -r requirements_dev.txt
```

## Features

* [`extract_onet_terms.py`](ability_skills_decoder/extract_terms.py): Extract representative terms for abilities and skills from O*Net data. Used as a source for our ableist lexicon.
* [`decoder.py`](ability_skills_decoder/decoder.py): Main module that identifies ableist language in a job description.

## Basic Usage

To identify ableist language in a job description, pass a `.txt` file containing the job description text to the `deocder.py` script:

```
python decoder.py -j /path/to/job_description.txt
```

The script will print out any ableist language that was detected in the job description, along with the location of the language (index position in the text) and the root form of the terms.

The main functionality is also available as a function via `decoder.find_ableist_language()`:

```python
>>> import spacy
>>> from ability_skills_decoder import decoder

>>> sample_job_description = """
    requirements
    - must be able to move your hands repeatedly
    - type on a computer
    - comfortable with lifting heavy boxes
    - excellent communication skills
    - move your wrists in circles and bend your arms
"""
>>> ableist_language = decoder.find_ableist_language(sample_job_description)
>>> print(albeist_language)
[lifting, bend, move your hands, move your wrists]

# We can also access the location of the language in the text and its root form
def print_results(results):
    for ableist_term in results:
        if isinstance(ableist_term, spacy.tokens.Span):
            print(
                f"PHRASE: {ableist_term} | LEMMA: {ableist_term.lemma_} | POSITION: {ableist_term.start}:{ableist_term.end}"
            )
        else:
            print(
                f"PHRASE: {ableist_term} | LEMMA: {ableist_term.lemma_} | POSITION: {ableist_term.i}"
            )
>>> print_results(ableist_language)
PHRASE: lifting | LEMMA: lift | POSITION: 22
PHRASE: bend | LEMMA: bend | POSITION: 38
PHRASE: move your hands | LEMMA: move your hand | POSITION: 8:11
PHRASE: move your wrists | LEMMA: move your wrist | POSITION: 32:35
```

## Data
* [O*NET Content Model Reference](https://www.onetcenter.org/dictionary/25.2/text/content_model_reference.html)