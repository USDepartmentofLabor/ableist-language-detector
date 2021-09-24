"""For training a custom mlflow model for detector api access."""

import click
import mlflow
import mlflow.pyfunc
import pandas as pd
import pprint
from ableist_language_detector.detector import find_ableist_language


class MLflowLanguageModel(mlflow.pyfunc.PythonModel):

    def __init__(self, func):
        self.func = func

    def predict(self, context, model_input):
        properties = ["lemma", "text", "start", "end",
                      "alternative_verbs", "example"]
        result = self.func(model_input['data'][0])
        terms = {}
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
            for ableist_term in result:
                terms[str(ableist_term.start)] = dict()
                if len(properties) > 0:
                    for p in properties:
                        try:
                            terms[str(ableist_term.start)][p] = str(getattr(ableist_term, p))
                        except AttributeError:
                            terms[str(ableist_term.start)][p] = str(getattr(ableist_term.data, p))
        return terms


@click.command()
@click.option(
    "--train_only",
    "-t",
    type=bool,
    required=True,
    default=True,
    help="Option to only train model and without testing on local file.",
)
@click.option(
    "--job_description_file",
    "-j",
    type=str,
    required=False,
    help="Path to file containing the job description text.",
)
def main(train_only, job_description_file):
    model_path = "detector_model"

    # Construct and save the model if one does not exist
    try:
        analyzer = MLflowLanguageModel(find_ableist_language)
        mlflow.pyfunc.save_model(path=model_path, python_model=analyzer)
        print("Generating new model in path {}".format(model_path))

    except:
        print("Existing model in path {}".format(model_path))
        pass

    if train_only is False:
        # Load the model in `python_function` format
        local_model = mlflow.pyfunc.load_model(model_uri=model_path)

        with open(job_description_file, "r") as jd_file:
            job_description_text = jd_file.read()

        data = pd.DataFrame({'data': [job_description_text]})

        local_output = local_model.predict(data)
        pprint.pprint(local_output)

    else:
        pass


if __name__ == "__main__":
    main()
