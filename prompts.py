FIND_RELEVANT_TOPIC_PROMPT = """
Determine whether or not the "Text Email" should belong to any of the existing topics.

Instructions:
- Carefully read the "Text Email".
- Review the list of "Current Topics", which include a Topic ID, a Topic Label or Name, and a Topic Summary.
- Decide if the email matches the meaning or intention of any existing topic.
- If the email fits well within an existing topic, return the corresponding Topic ID.
- If the email does not match any existing topic, return "No topics".

Example:
Input:
    - Text Email: "Lucy,

        Here are the actual utility bills versus the cap.  Did we collect 
        these overages?  Let's discuss further?  Remember these bills were paid in 
        July and August.  The usage dates are much earlier.  I have the bills but I 
        can get them to you if need be.

        Philip"
    - Current Topics:
        - Topic ID: 2n4l
          Topic Label: Office Supplies Order
          Topic Summary: Emails related to purchasing, tracking, or requesting office materials such as printers, pens, paper, computers, or other administrative equipment and supplies.

        - Topic ID: 9k45
          Topic Name: Utility Bill
          Topic Summary: Emails related to periodic statement of charges for essential services like electricity, gas, water, and sometimes internet or waste disposal. These bills typically include account details, usage information, amount due, and payment instructions

Output: 9k45
"""

GET_NEW_TOPIC_SUMMARY_PROMPT = """
You are the steward of a group of topics which represent groups of sentences that talk about a similar topic
You should generate a very brief 1-sentence summary which will inform viewers what a topic group is about.

A good summary will say what the topic is about, and give any clarifying instructions on what to add to the topic.

You will be given a proposition which will go into a new topic. This new topic needs a summary.

Your summaries should anticipate generalization. If you get a proposition about apples, generalize it to food.
Or month, generalize it to "date and times".

Example:
Input: Proposition: Greg likes to eat pizza
Output: This topic contains information about the types of food Greg likes to eat.

Only respond with the new topic summary, nothing else.
"""

GET_NEW_TOPIC_LABEL_PROMPT = """
You are the steward of a group of topics which represent groups of sentences that talk about a similar topic
You should generate a very brief few word title which will inform viewers what a topic group is about.

A good topic title is brief but encompasses what the topic is about

You will be given a summary of a topic which needs a title

Your titles should anticipate generalization. If you get a proposition about apples, generalize it to food.
Or month, generalize it to "date and times".

Example:
Input: Summary: This topic is about dates and times that the author talks about
Output: Date & Times

Only respond with the new topic title, nothing else.
"""
