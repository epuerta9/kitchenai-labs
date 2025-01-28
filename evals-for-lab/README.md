# Evals for Lab

This is a small initial lab workshop on how to get deepseek evaluation framework process under control. 

Starting off by explaining the high level concepts and going down into the practical examples of 

* Building a Golden dataset from sample pdf
* Creating test cases from a data set using a specific AI Model
* Evaluating the test sets using a metric.

# Pre-Reqs

* uv 
* export OPENAI_API_KEY
* export DEEPSEEK_API_KEY (optional)
* run the notebook `uv run -- marimo edit src/kitchenai-labs-evals.py ` 

# Notes

This workshop uses a simple AI implementation which is a chat complete for two different models. OpenAI gpt4 and DeepSeek R1. 

If you run DeepSeek against test cases, be prepared to wait a long time. DeepSeek Reasoning takes a long time to build the test cases. 

The example uses 1 RFP and 6 golden datasets 