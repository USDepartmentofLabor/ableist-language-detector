"""Module with ableist verbs and objects."""

# TODO: May want to convert over to a dataclass if we want to store alternative words.

# Verbs we always want to avoid because they are often ableist regardless of context.
# All in lemma form (important!)
ABLEIST_VERBS = {
    "climb",
    "touch",
    "feel",
    "hand",
    "carry",
    "lift",
    "reach",
    "throw",
    "read",
    "see",
    "speak",
    "talk",
    "hear",
    "stand",
    "sit",
    "bend",
    "crouch",
    "kneel",
    "crowd",
    "taste",
    "smell",
    "type",
    "walk",
    "run",
    "jump",
}


# Verbs that may be ableist depending on the object of the verb.
# All in lemma form (important!)
ABLEIST_VERBS_OBJECT_DEPENDENT = {
    "move",
}

# Objects that would make the object dependent verbs ableist.
# All in lemma form (important!)
ABLEIST_OBJECTS = {
    "hand",
    "eye",
    "finger",
    "arm",
    "leg",
    "foot",
    "wrist",
    "limb",
    "torso",
    "body",
}
