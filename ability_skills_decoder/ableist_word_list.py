"""Module to create ableist language dataclass instance collection from csv wordlist."""

import os
from csv import DictReader
from dataclasses import dataclass
from typing import List, Union

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
WORDLIST_CSV_PATH = os.path.join(__location__, "ableist_word_list.csv")


@dataclass
class AbleistLanguage:
    """Dataclass of ableist language to search for; automatically generated from the
    wordlist csv.
    """

    verb: str
    object_dependent: Union[str, bool]
    alternative_verbs: Union[str, List[str]]
    example: str
    objects: Union[str, List[str]]

    def __post_init__(self):
        # Handle empty objects
        if self.objects == "":
            self.objects = None

        # Convert alt verbs & objects into list of verbs instead of one big string
        if isinstance(self.alternative_verbs, str):
            self.alternative_verbs = [
                word.strip() for word in self.alternative_verbs.split(",")
            ]
        if self.objects and isinstance(self.objects, str):
            if self.objects:
                self.objects = [word.strip() for word in self.objects.split(",")]

        # Convert string boolean values to true boolean
        if not isinstance(self.object_dependent, bool):
            if self.object_dependent.lower() in ["true", "t", "y", "yes"]:
                self.object_dependent = True
            elif self.object_dependent.lower() in ["false", "f", "n", "no"]:
                self.object_dependent = False
            else:
                raise ValueError(
                    f"Value for object_dependent ({self.object_dependent}) "
                    f"cannot be mapped to boolean."
                )

        # TODO: Check to see if input is actually in lemma form?


ABLEIST_VERBS = {}
with open(WORDLIST_CSV_PATH, "r") as wordlist_csv:
    reader = DictReader(wordlist_csv)
    for row in reader:
        row_data = AbleistLanguage(**row)
        ABLEIST_VERBS[row_data.verb] = row_data


if __name__ == "__main__":
    print(ABLEIST_VERBS)
