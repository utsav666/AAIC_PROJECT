Chain-of-Thought Reasoning Without Prompting

Objective of the Paper:
The paper aims to enable smaller language models to perform chain-of-thought (CoT) reasoning without relying on prompt engineering. Instead of using large models with handcrafted prompts, the authors propose fine-tuning smaller models on explanation-rich datasets to make reasoning an internal learned skill.


Workflow for the Paper:
Step 1: Teacher Model Setup
Start with a very large language model (e.g., PaLM 540B or GPT-3) capable of performing chain-of-thought reasoning via prompting.
Design prompt templates that elicit step-by-step reasoning answers from these large models.

Step 2: Data Generation (Teacher Forcing Phase)
Query the large model with multiple CoT prompts across diverse tasks (math, commonsense, QA).
Collect outputs from the large model containing question → detailed explanation → final answer.
Curate and filter these responses to build a high-quality dataset.

Step 3: Dataset Construction
Combine thousands of these teacher-generated examples into a single training corpus.
Each entry in the dataset consists of:
Question
Step by step explanation
Generate Final answer

Step 4: Fine-Tuning Smaller Models
Choose smaller models (e.g., 137M, 8B parameters).
Fine-tune these models on the explanation-rich dataset using supervised learning.
Train until the models learn to replicate step-by-step reasoning patterns.

Step 5: Inference Without Prompting
Post fine-tuning, smaller models can now generate CoT reasoning naturally.
Users can ask questions without special prompts, and the model will respond with step-by-step reasoning followed by the final answer.

Step 6: Evaluation
Compare performance of the fine-tuned models against:
Prompted CoT inference on large models
Zero-shot and few-shot baselines
Evaluate on datasets like GSM8K, SVAMP, and AQuA.

Step 7: Key Findings
Small models, once fine-tuned on explanation-rich datasets, outperform zero-shot and few-shot prompting baselines.
CoT reasoning becomes an internal capability rather than an external prompt-based trick.

Visual Summary:

[ Large Model + Prompt Engineering ]
                |
                v
        [ Generate Large Dataset of CoT Explanations ]
                |
                v  
            [ Build Explanation-Rich Training Dataset ]
                |
                v
            [ Fine-Tune Smaller Models on CoT Dataset ]
                |
                v
              [ Smaller Models Learn to Reason Step-by-Step ]
                |
                v
                  ->[ Inference Without Special Prompting ]