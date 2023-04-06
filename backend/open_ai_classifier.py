import openai
import re
openai.api_key = "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"


def open_ai_classifier(response_text):
    prompt = (
        "Classify the following response as accepting, declining, or neutral for an appointment: "
        f"{response_text} "
        "Accepting: Yes, I can make it. | I'd love to come. | That works for me. | I'll see you then. "
        "Declining: I'm sorry, I can't make it. | I won't be able to come. | "
        "Unfortunately, I have a prior commitment. | That doesn't work for me, sorry. "
        "Neutral: Let me check my schedule and I'll let you know. | I'll think about it and let you know. | "
        "I'm not sure, can I get back to you later? | I'm unavailable that day, but maybe we can reschedule?"
    )

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=25,
        n=1,
        temperature=0.7,
    )

    # print(response.choices[0].text)
    patterns = ['accepting', 'declining', 'neutral']
    response_result = response.choices[0].text.lower()
    for pattern in patterns:
        if re.search(pattern, response_result):
            return pattern

    return 'unknown'
