# [wip] ability-skills-decoder
Tool to identify ableist language in job descriptions.

**What is ableist language?**

> Ableist language is language that is offensive to people with disability. It can also refer to language that is derogatory, abusive or negative about disability. Ableism is the systemic exclusion and oppression of people with disability, often expressed and reinforced through language. [[source]](https://pwd.org.au/resources/disability-info/language-guide/ableist-language/)

**Why is this tool important?**

Ableist language in job descriptions can cause people with disabilities to feel excluded from jobs that they are qualified for. This typically occurs when a description references [*abilities*](https://www.onetonline.org/find/descriptor/browse/Abilities/) or enduring attributes of an individual that are unnecessary for the job or for which [accommodations](https://askjan.org/) can be proactively offered instead of focusing on developed [*skills*](https://www.onetonline.org/skills/) that can be acquired to succeed in the role. By identifying ableist language and suggesting alternatives, this tool will support more inclusive hiring practices.

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

To identify ableist language in a job description, pass a `.txt` file containing the job description text to the `decoder.py` script:

```
python decoder.py -j /path/to/job_description.txt
```

The script will print out any ableist language that was detected in the job description, along with the location of the language (index position in the text), the root form of the terms, suggested alternative verbs, and an example of how to use the alternative phrasing.

The main functionality is also available as a function via `decoder.find_ableist_language()`. This function returns a collection of `AbleistLanguageMatch` objects, which contain the same information listed above as attributes.

Example usage:

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
>>> print(ableist_language)
[lifting, bend, move your hands, move your wrists]

# Accessing attributes
def print_results(result):
    """Convenience function to print attributes."""
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
>>> print_results(ableist_language)
Found 4 instances of ableist language.

Match #1
PHRASE: lifting | LEMMA: lift | POSITION: 22:23 | ALTERNATIVES: ['move', 'install', 'operate', 'manage', 'put', 'place', 'transfer', 'transport'] | EXAMPLE: Transport boxes from shipping dock to truck

Match #2
PHRASE: bend | LEMMA: bend | POSITION: 38:39 | ALTERNATIVES: ['lower oneself', 'drop', 'move to', 'turn'] | EXAMPLE: Install new ethernet cables under floor rugs

Match #3
PHRASE: move your hands | LEMMA: move your hand | POSITION: 8:11 | ALTERNATIVES: ['observe', 'operate', 'transport', 'transfer', 'activate'] | EXAMPLE: Operates a machine using a lever

Match #4
PHRASE: move your wrists | LEMMA: move your wrist | POSITION: 32:35 | ALTERNATIVES: ['observe', 'operate', 'transport', 'transfer', 'activate'] | EXAMPLE: Operates a machine using a lever
```
