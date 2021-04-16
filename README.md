# [wip] ability-skills-decoder
Tool to evaluate job postings for ability <> skills bias

## Installation

Clone the repo and install the package in edit mode (preferably in a virtual environment).
```
git@github.com:inclusive-ai/ability-skills-decoder.git
cd ability-skills-decoder
pip install -e .
```

Download spaCy dependencies.
```
python -m spacy download en_core_web_sm
```

## Features

* [`extract_terms.py`](ability_skills_decoder/extract_terms.py): Extract representative terms for abilities and skills from O*Net data.

## Data
* [O*NET Content Model Reference](https://www.onetcenter.org/dictionary/25.2/text/content_model_reference.html)