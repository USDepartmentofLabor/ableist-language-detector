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

## Features

* [`extract_onet_terms.py`](ability_skills_decoder/extract_terms.py): Extract representative terms for abilities and skills from O*Net data. Used as a source for our ableist lexicon.
* [`decoder.py`](ability_skills_decoder/decoder.py): Main module that identifies ableist language in a job description.

## Data
* [O*NET Content Model Reference](https://www.onetcenter.org/dictionary/25.2/text/content_model_reference.html)