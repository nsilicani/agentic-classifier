FIND_RELEVANT_TOPIC_PROMPT = """
You are an intelligent assistant for classifying internal corporate emails into existing topics.

## Task
Given a new email, determine whether it belongs to any of the **existing topics** provided below.

## Instructions:
- Read the corporate email ("Email Text").
- Review the list of current topics, which each include a Topic ID, Label, and Summary.
- Check if the email's **intent**, **subject**, or **content** aligns closely with any topic summary.
- If it fits one topic clearly, return the Topic ID.
- If none of the topics are a good fit, return "No topics".

## Matching Criteria:
- Match by business intent (e.g., invoice issue, meeting scheduling, budget request).
- Ignore small stylistic or wording differences.
- Be strict: only assign to a topic if there's a clear and relevant match.

## Format:
Only respond with either a Topic ID or the string: No topics

### Example
Email Text:
"Lucy,

Here are the actual utility bills versus the cap. Did we collect 
these overages? Let's discuss further? Remember these bills were paid in 
July and August. The usage dates are much earlier. I have the bills but I 
can get them to you if need be.

Philip"

Current Topics:
- Topic ID: 2n4l
  Topic Label: Office Supplies Order
  Topic Summary: Emails related to purchasing or requesting administrative supplies.

- Topic ID: 9k45
  Topic Label: Utility Bill
  Topic Summary: Emails about periodic service charges (e.g., electricity, gas, water) including usage, payment, or billing questions.

Output:
9k45
"""

GET_NEW_TOPIC_SUMMARY_PROMPT = """
You are helping organize internal corporate emails into coherent topic groups.

## Task:
Given a new email, generate a one-sentence summary that describes what this new topic group is about.

## Guidelines:
- Be brief and clear.
- Generalize to a business domain where possible.
- Focus on the **intent** and **context** of the email (e.g., budget discussion, vendor payment, meeting scheduling).
- Avoid overly specific summaries that won't generalize to similar emails.

## Example:

Email: "Please send over the July invoice for review"
Output: This topic involves emails related to invoice requests and processing.

Only return the summary sentence.
"""

GET_NEW_TOPIC_LABEL_PROMPT = """
You are generating short, descriptive labels for groups of corporate emails.

## Task:
Given a one-sentence summary of a topic, write a **short topic label** (2–5 words) that clearly reflects the business theme.

## Guidelines:
- Be concise.
- Use terms suitable for routing emails to the correct mailbox based on topic (e.g., "Invoice Issues", "Meeting Scheduling").
- Generalize appropriately (e.g., “Utilities” instead of “Water Bill for March”).
- Avoid using full sentences or names.

## Example:
Summary: Emails related to invoice processing, billing questions, or payment schedules.
Output: Invoice Processing

Summary: Emails about scheduling internal team meetings or calendar updates.
Output: Meeting Scheduling

Only return the topic label.
"""

UPDATE_TOPIC_SUMMARY_PROMPT = """
You are maintaining topic summaries for groups of corporate emails.

## Task:
Given a new email that will be added to an existing topic, update the topic summary so that it still:
- Describes the overall theme of the topic.
- Reflects the new information from the latest email.

## Guidelines:
- Be concise (1 sentence).
- Keep the summary general, covering **all** emails in the topic.
- Incorporate the key intent or context from the new email.
- Avoid repeating exact phrases from the new email.

## Example:
Existing Summary: Emails about utility charges and monthly billing.
New Email: "We were overcharged for gas usage in August. Please review the statement."

Output: This topic includes emails related to billing discrepancies and utility charge reviews.

Only return the updated topic summary.
"""

UPDATE_TOPIC_LABEL_PROMPT = """
You are updating the label of a corporate email topic based on an updated summary.

## Task:
Given the revised topic summary, provide a new short topic label (2–5 words) that better captures the theme of all emails in the topic.

## Guidelines:
- Be concise and business-relevant.
- Avoid being too specific to one email.
- Make sure the label would make sense in a dashboard or filter.

## Example:
Updated Summary: This topic includes emails related to billing discrepancies and utility charge reviews.
Output: Utility Billing Issues

Only return the topic label.
"""
