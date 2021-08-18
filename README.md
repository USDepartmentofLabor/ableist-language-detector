# ableist-language-detector
Tool to identify ableist language in job descriptions.

Developed jointly by the [Department of Labor Office of Disability Employment Policy](https://www.dol.gov/agencies/odep) ("DOL ODEP"), [xD | U.S. Census Bureau](https://www.xd.gov/), and the [Presidential Innovation Fellows](https://presidentialinnovationfellows.gov/).

**What is ableist language?**

> Ableist language is language that is offensive to people with disability. It can also refer to language that is derogatory, abusive or negative about disability. Ableism is the systemic exclusion and oppression of people with disability, often expressed and reinforced through language. [[source]](https://pwd.org.au/resources/disability-info/language-guide/ableist-language/)

**Why is this tool important?**

Ableist language in job descriptions can cause people with disabilities to feel excluded from jobs that they are qualified for. This typically occurs when a description references [*abilities*](https://www.onetonline.org/find/descriptor/browse/Abilities/) or enduring attributes of an individual that are unnecessary for the job or for which [accommodations](https://askjan.org/) can be proactively offered instead of focusing on developed [*skills*](https://www.onetonline.org/skills/) that can be acquired to succeed in the role. By identifying ableist language and suggesting alternatives, this tool will support more inclusive hiring practices.

## Installation

This package requires Python >= 3.8.

Clone the repo and install the package (preferably in a virtual environment):
```
git clone git@github.com:USDepartmentofLabor/ableist-language-detector.git
python -m pip install ableist-language-detector/
```

Download spaCy dependencies.
```
python -m spacy download en_core_web_sm
```

**Developer Installation**

If you plan on contributing to the repo, complete these additional steps:

Install the dev requirements.

```
python -m pip install -r requirements_dev.txt
```

## Features

* [`extract_onet_terms.py`](ableist_language_detector/extract_terms.py): Extract representative terms for abilities and skills from O*Net data. Used as one of our sources for our ableist lexicon.
* [`detector.py`](ableist_language_detector/detector.py): Main module that identifies ableist language in a job description.

## Usage

There are three ways to access the tool.

### 1. Web Application

To run a local instance of the tool as a web application, see the instructions in [this respository](https://github.com/lujamie/dol-web).

![img](assets/ableist-ui-demo-fullsize.gif)

### 2. Command Line Tool

The command line tool allows you to check a single job description for ableist language by passing a `.txt` file containing the job description text to the main `detector.py` script.

The script will print out any ableist language that was detected in the job description, along with the location of the language (token index position in the text), the root form of the terms, suggested alternative verbs, and an example of how to use the alternative phrasing.

```
Usage: detector.py [OPTIONS]

  Extract ableist terms from a job description.

Options:
  -j, --job_description_file TEXT
                                  Path to file containing the job description
                                  text.  [required]
  --help                          Show this message and exit.
```

**Example usage:**

```
>>> python ableist_language_detector/detector.py -j sample_job_descriptions/short_job_description.txt
Found 4 instances of ableist language.

Match #1
PHRASE: lifting | LEMMA: lift | POSITION: 21:22 | ALTERNATIVES: ['move', 'install', 'operate', 'manage', 'put', 'place', 'transfer', 'transport'] | EXAMPLE: Transport boxes from shipping dock to truck

Match #2
PHRASE: bend | LEMMA: bend | POSITION: 37:38 | ALTERNATIVES: ['lower oneself', 'drop', 'move to', 'turn'] | EXAMPLE: Install new ethernet cables under floor rugs

Match #3
PHRASE: move your hands | LEMMA: move your hand | POSITION: 7:10 | ALTERNATIVES: ['observe', 'operate', 'transport', 'transfer', 'activate'] | EXAMPLE: Operates a machine using a lever

Match #4
PHRASE: move your wrists | LEMMA: move your wrist | POSITION: 31:34 | ALTERNATIVES: ['observe', 'operate', 'transport', 'transfer', 'activate'] | EXAMPLE: Operates a machine using a lever
```

### 3. Direct Import

The main functionality is also available directly via `detector.find_ableist_language()` for those who would like a more flexible way to integrate the functionality into existing pipelines/applications. The `detector.find_ableist_language()` function returns a collection of `AbleistLanguageMatch` objects, which contain the same information listed above as attributes.

`AbleistLanguageMatch` Attribute | Type | Description
---- | ---- | -----
`text` | `str` | Raw form of matched phrase
`lemma` | `str` | Lemma (i.e. root form) of matched phrase
`start` | `int` | The starting token index of the matched phrase within the document
`end` | `int` | The ending token index (exclusive) of the matched phrase within the document
`data.verb` | `str` | The lemma form of the matched verb from the ableist lexicon
`data.alternative_verbs` | `List[str]` | The list of suggested alternative verbs from the ableist lexicon
`data.example` | `str` | An example of an alternative verb used in a phrase/sentence from the ableist lexicon
`data.object_dependent` | `bool` | `True` if the `data.verb` is considered ableist depending on the verb's object; else `False`
`data.objects` | `List[str]` | If `data.object_dependent == True`, a list of objects that, combined with `data.verb`, is considered ableist language

**Example usage:**

```python
>>> from ableist_language_detector import detector

>>> sample_job_description = """
    requirements
    - must be able to move your hands repeatedly
    - type on a computer
    - comfortable with lifting heavy boxes
    - excellent communication skills
    - move your wrists in circles and bend your arms
"""
>>> ableist_language = detector.find_ableist_language(sample_job_description)
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

## Ableist Language Lexicon

The tool checks for job descriptions against an ableist language lexicon. To view the language that's currently in our lexicon, see the [ableist_language_detector/ableist_word_list.csv](ableist_language_detector/ableist_word_list.csv) file. This lexicon is constantly evolving and we appreciate any feedback or requests for changes. To do so, please [open an issue](https://github.com/USDepartmentofLabor/ableist-language-detector/issues).

The lexicon was developed based on the following data sources in consultation with subject matter experts at DOL ODEP.

* [O*Net Online](https://www.onetonline.org/)
* ["Writing ADA Compliant Job Descriptions" by the Texas Municipal Human Resources Association](https://tmhra.org/ADAToolkit/5-WriteADA-JobDescrip.pdf)
* ["Non-Prejudicial Language For ADA Compliant Job Descriptions" by Kenneth H. Pritchard, CCP](http://www.thehumanequation.com/en/news_rss/articles/2004/ADALegalJobDescriptions.pdf)
* ["Writing ADA Compliant Job Descriptions" by the University of Massachusetts Office of the President](https://www.umassp.edu/sites/default/files/documents/human-resources/ADA%20job%20descriptions.pdf)
