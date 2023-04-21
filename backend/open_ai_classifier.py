import openai
import re
import datetime
openai.api_key = "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"


def open_ai_classifier(response_text, original_suggestion):
    prompt = f'''
    suggestion: "{original_suggestion}"
    The suggestion is in finnish. Classify the following responses to the suggestion as accept, decline, or suggestion:
    "Sopii hyvin": accept
    "Ei käy": decline
    "Olisiko seuraavalla viikolla vapaita aikoja?": suggestion
    "{response_text}": '''

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=10,
        n=1,
        temperature=0.1,
    )

    # print(response.choices[0].text)
    patterns = ['accept', 'decline', 'suggestion']
    response_result = response.choices[0].text.lower().strip()
    for pattern in patterns:
        if re.search(pattern, response_result):
            return pattern

    return 'unknown'


'''
Gets suggested time from response

@param original_suggestion: The original suggestion sent to customer
@param response_text: The response from customer

@return object like {'from': 'dd.mm.YYYY-hh:mm', 'to': 'dd.mm.YYYY-hh:mm', 'status': 'success | failed' }
'''


def deduce_time(response_text, original_suggestion):
    today = datetime.date.today()

    # Next weeks wednesday
    days_to_monday = (6 - today.weekday()) + 1
    days_to_wednesday = (6 - today.weekday()) + 3
    days_to_sunday = (6 - today.weekday()) + 7
    next_monday = today + datetime.timedelta(days=days_to_monday)
    next_wednesday = today + datetime.timedelta(days=days_to_wednesday)
    next_sunday = today + datetime.timedelta(days=days_to_sunday)

    # Format the date as "Monday X Month YYYY"
    formatted_today = today.strftime("%A %d %B %Y")
    formatted_next_monday = next_monday.strftime("%d %B %Y")
    formatted_next_wednesday = next_wednesday.strftime("%d %B %Y")
    formatted_next_sunday = next_sunday.strftime("%d %B %Y")

    p = f"""
    suggestion: "{original_suggestion}"

    The suggestion is in finnish. Given that today is {formatted_today}, infer any time frames mentioned in the following responses to the before mentioned suggestion:

    text: Ensi maanantaina sopisi hyvin
    time: {formatted_next_monday}, 00:00 to {formatted_next_monday}, 23:59

    text: Ensi viikolla keskiviikosta eteen päin kävisi
    time: {formatted_next_wednesday}, 00:00 to {formatted_next_sunday}, 23:59

    text: {response_text}
    time: """
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=p,
        max_tokens=20,
        n=1,
        temperature=0.1,
    )

    result = response.choices[0].text
    try:
        [from_time, to_time] = result.split(" to ")
        from_time = from_time.strip()
        to_time = to_time.strip()
        from_date_obj = datetime.datetime.strptime(
            from_time, "%d %B %Y, %H:%M")
        to_date_obj = datetime.datetime.strptime(to_time, "%d %B %Y, %H:%M")
        suggestion_obj = {
            "from": from_date_obj.strftime("%d.%m.%Y-%H:%M"),
            "to": to_date_obj.strftime("%d.%m.%Y-%H:%M"),
            "status": "success"
        }
        return suggestion_obj
    except:
        print(
            f"OpenAI returned unexpected result:'{result}' in open_ai_classifier.getTime")
    return {
        "from": "-",
        "to": "-",
        "status": "failed"
    }
