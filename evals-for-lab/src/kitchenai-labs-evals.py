import marimo

__generated_with = "0.10.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import nest_asyncio
    nest_asyncio.apply()
    return (nest_asyncio,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Building up a good evaluation set for AI development

        Part of being able to build solid AI systems is to be able to have objective metrics on why some implementations are better than others.

        In this lab workshop we'll explore building custom eval sets that fit your use case using popular open source libraries like deepeval https://github.com/confident-ai/deepeval
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        # Creating the Goldens

        Taken straight from the deepeval docs, here is what goldens are. 
        > "A Golden is extremely very similar to an LLMTestCase, but they are more flexible as they do not require an actual_output at initialization. On the flip side, whilst test cases are always ready for evaluation, a golden isn't."

        What this means is that we can prep our eval sets with everything except the actual output.
        """
    )
    return


@app.cell
def _(mo):
    fs = mo.ui.number(start=1, stop=3)
    num_of_files = mo.vstack( [mo.md("Number of Source Files you want to create a dataset from") , fs])
    num_of_files
    return fs, num_of_files


@app.cell
def _(fs, mo):
    example_data = mo.ui.text(placeholder="src/data/advertising-rfp.pdf")
    examples = mo.ui.array([example_data] * fs.value, label="Three source files")
    examples
    return example_data, examples


@app.cell
def _(mo):
    create_goldens_button = mo.ui.run_button(label="Create the Goldens")
    create_goldens_button
    return (create_goldens_button,)


@app.cell
def _(
    create_goldens_button,
    create_variable_goldens,
    dataset,
    examples,
    mo,
):
    mo.stop(not create_goldens_button.value, mo.md("Click 👆 to run the creation of goldens from your source files"))
    create_variable_goldens(dataset, examples.value)
    return


@app.cell
def _(dataset):
    len(dataset.goldens)
    return


@app.cell
def _(dataset):
    dataset.goldens[0].model_dump()
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        # Creating the Test Cases from Goldens

        Goldens are synthesized from unstructured documents into inputs, expected outputs, and retrieved content. This gives us the foundation of a TestCase with one crucial missing piece - the **actual output**! 

        Lets first create the TestCases From Goldens. 

        For the sake of simplicity, we're going to just create 6 LLMTestCases from using 1 source document
        """
    )
    return


@app.cell
def _(dataset):
    dataset.goldens[0].model_dump()
    return


@app.cell
def _(dropdown_dict, mo):
    mo.hstack([dropdown_dict, mo.md(f"Has value: {dropdown_dict.value} and selected_key {dropdown_dict.selected_key}")])
    return


@app.cell
def _(mo):
    test_case_button = mo.ui.run_button(label="Create the Test Cases")
    test_case_button
    return (test_case_button,)


@app.cell
def _(deepseek_impl, mo, openai_impl):
    dropdown_dict = mo.ui.dropdown(options={"DeepSeek":deepseek_impl, "OpenAI":openai_impl},
                            value="DeepSeek", # initial value
                            label="choose the LLM of your choice")
    return (dropdown_dict,)


@app.cell
def _(dataset, mo):
    mo.md(f"Number of goldens: {len(dataset.goldens)}")
    return


@app.cell
def _(create_test_cases, dataset, dropdown_dict, mo, test_case_button):
    mo.stop(not test_case_button.value, mo.md("Click 👆 to run the creation of test cases from your goldens"))
    create_test_cases(dataset, dropdown_dict.value)
    return


@app.cell
def _(dataset):
    _cases = [{"input": x.input, "output": x.actual_output} for x in dataset.test_cases]

    for c in _cases:
        input = c["input"]
        output = c["output"]
        print(f"INPUT: {input} \n")
        print(f"OUTPUT: {output} \n\n")
        print("--------------------")
    return c, input, output


@app.cell
def _(mo):
    mo.md(
        r"""
        # Evaluating the Dataset

        We'll pick a set of available metrics to test on. Since most require retrieved context, and we're only using chat, lets resort to using just AnswerRelevancy metric
        """
    )
    return


@app.cell
def _(mo):
    eval_button = mo.ui.run_button(label="Evaluate the Dataset")
    eval_button
    return (eval_button,)


@app.cell
def _(
    AnswerRelevancyMetric,
    HallucinationMetric,
    dataset,
    eval_button,
    evaluate,
    mo,
):
    mo.stop(not eval_button.value, mo.md("Click 👆 to run the evaluation dataset"))
    @mo.cache
    def run_eval(dataset):
        hallucination_metric = HallucinationMetric(threshold=0.3)
        answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5, async_mode=False)

        return evaluate(dataset, metrics=[answer_relevancy_metric], skip_on_missing_params=True)
    result = run_eval(dataset)
    result
    return result, run_eval


@app.cell
def _(dropdown_dict, mo, result):
    _md = result.model_dump()
    def _():
        data = []
        for test in _md["test_results"]:
            for metric in test["metrics_data"]:
                data.append({
                    "test_name": test["name"],
                    "success": test["success"],
                    "metric_name": metric["name"],
                    "threshold": metric["threshold"],
                    "metric_success": metric["success"],
                    "score": metric["score"],
                    "reason": metric["reason"],
                    "evaluation_model": metric["evaluation_model"],
                    "evaluation_cost": metric["evaluation_cost"],
                })

        return data

    _()
    table = mo.ui.table(data=_(), pagination=True, label=dropdown_dict.selected_key)
    table
    return (table,)


@app.cell
def _(LLMTestCase, dataset):
    def create_goldens():
        dataset.generate_goldens_from_docs(document_paths=['src/data/advertising-rfp.pdf', 'src/data/construction-rfp.pdf', 'src/data/consultancy-rfp.pdf'])

    def save_dataset(dataset):
        dataset.save_as(
            file_type='json',
            directory="./synthetic_data"
        )

    def save_dataset_with_test_cases(dataset):
        dataset.save_as(
            file_type='json',
            directory="./synthetic_data_with_test_cases"
        )

    def create_variable_goldens(dataset, sources):
        """ARGS: 
        sources: List[str]
        """
        dataset.generate_goldens_from_docs(document_paths=sources)
        save_dataset(dataset)

    def create_test_cases(dataset, impl_func):

        for i, golden in enumerate(dataset.goldens):
            print(f"creating test case {i}: with golden: {golden.input}")
            # Compute actual output and retrieval context

            actual_output = impl_func(golden.input) # Replace with logic to compute actual output
            retrieval_context = golden.retrieval_context # Replace with logic to compute retrieval context

            dataset.add_test_case(
                LLMTestCase(
                    input=golden.input,
                    actual_output=actual_output,
                    retrieval_context=retrieval_context
                )
            )
    return (
        create_goldens,
        create_test_cases,
        create_variable_goldens,
        save_dataset,
        save_dataset_with_test_cases,
    )


@app.cell
def _(os):
    import json
    def get_latest_json_path(directory):
        try:
            # List all JSON files in the directory
            files = [f for f in os.listdir(directory) if f.endswith('.json')]
            if not files:
                raise FileNotFoundError("No JSON files found in the directory.")

            # Get the full paths of the files
            full_paths = [os.path.join(directory, f) for f in files]

            # Find the latest file based on modification time
            latest_file = max(full_paths, key=os.path.getmtime)

            return latest_file

        except Exception as e:
            print(f"Error: {e}")
            return None
    return get_latest_json_path, json


@app.cell
def _():
    from deepeval.dataset import EvaluationDataset
    from deepeval.metrics import HallucinationMetric, AnswerRelevancyMetric
    from deepeval.dataset import EvaluationDataset
    from openai import OpenAI
    import os
    import asyncio
    from deepeval.test_case import LLMTestCase
    from deepeval import evaluate
    return (
        AnswerRelevancyMetric,
        EvaluationDataset,
        HallucinationMetric,
        LLMTestCase,
        OpenAI,
        asyncio,
        evaluate,
        os,
    )


@app.cell
def _(EvaluationDataset):
    dataset = EvaluationDataset()
    return (dataset,)


@app.cell
def _(OpenAI, os):
    def deepseek_impl(input):

        client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY",None), base_url="https://api.deepseek.com")
        print(input)

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": input},
            ],
            stream=False
        )
        return response.choices[0].message.content


    def openai_impl(input):    
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": input},
            ],
            stream=False
        )
        return response.choices[0].message.content
    return deepseek_impl, openai_impl


if __name__ == "__main__":
    app.run()
