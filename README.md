# Agentic Text Classifier (Unsupervised Topic Modeling)

## Goal
Automatically discover and assign texts (e.g., emails) into coherent topics using an LLM-powered agentic workflow — without predefined topic categories.

## Workflow Steps

1. **Initialize Framework**
   - Loads model (OpenAI or HF).
   - Sets up parameters, topic dictionary, and prompt templates.

2. **Process a Text**
   - Try to assign it to an existing topic using LLM-based prompt.
   - If no topic is suitable, create a new one with its own summary and label.

3. **Create New Topic**
   - Use prompts to generate a topic summary and label.
   - Assign a UUID-based `topic_id`.

4. **Update Topic**
   - Append new text to the topic.
   - If enabled, re-generate topic summary and label using updated text context.

5. **Maintain Topic Outline**
   - Keep a dynamic string containing all current topics to feed into the LLM.

## Output Format
```json
{
  "topic_id": "a1b2",
  "summary": "Payment delays related to invoice issues.",
  "label": "Invoice Disputes",
  "texts": ["..."]
}
