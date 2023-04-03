import openai
import re
import datetime
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

'''
Gets suggested time from response

@param original_suggestion: The original suggestion sent to customer
@param response_text: The response from customer

@return object like {'date': '04.04.2023', 'from': '00:00', 'to': '24:00, 'status': 'success | failed'}
'''
def deduce_time(response_text, original_suggestion):
    today = datetime.date.today()

    # Next weeks wednesday
    days_to_wednesday = (2 - today.weekday()) % 7 + 7 # 2 represents Wednesday, 7 represents number of days in a week
    next_wednesday = today + datetime.timedelta(days=days_to_wednesday)

    # Format the date as "Monday X Month YYYY"
    formatted_today = today.strftime("%A %d %B %Y")
    formatted_next_wednesday = next_wednesday.strftime("%d %B %Y")

    p = f"""
    suggestion: "{original_suggestion}"

    The suggestion is in finnish. Given that today is {formatted_today}, infer any dates mentioned in the following responses to the before mentioned suggestion:

    text: Ensi keskiviikkona sopisi hyvin
    date: {formatted_next_wednesday}, 00:00-24:00

    text:  {response_text}
    date: """
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=p,
        max_tokens=15,
        n=1,
        temperature=0.1,
    )

    result = response.choices[0].text
    try:
        [datestr, timestr] = result.split(",")
        datestr = datestr.strip()
        timestr = timestr.strip()
        date_obj = datetime.datetime.strptime(datestr, "%d %B %Y")
        #time_pattern = re.compile(r'^\d{2}:\d{2}$')
        [time_from, time_to] = timestr.split("-")
        suggestion_obj = {
            "date": date_obj.strftime("%d.%m.%Y"),
            "from": time_from,
            "to": time_to,
            "status": "success"
        }
        return suggestion_obj
    except:
        print(f"OpenAI returned unexpected result:'{result}' in open_ai_classifier.getTime")
    return {
        "date": "-",
        "from": "-",
        "to": "-",
        "status": "failed" 
    }
