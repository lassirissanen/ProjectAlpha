import { Message } from "./Message";
import { getTensorflowClassification, getCombinedClassification, getOpenAIClassification } from '../service/backend-service';
import { useState } from "react";
import { Statistics } from "./Statistics";
import './MessageList.css';

export const MessageList = (props) => {
  let today = new Date();
  let nextMonday = new Date(today.getFullYear(), today.getMonth(), today.getDate() + (1 + 7 - today.getDay()) % 7);
  let nextMondayFormatted = nextMonday.toLocaleDateString('fi-FI', { year: "numeric", month: "2-digit", day: "2-digit" });
  const initialMessage = `Hei! Olemme varanneet sinulle alustavan hammastarkastus ajan ${nextMondayFormatted} klo 12:00. Vastaa 'V' varmistaaksesi ajan`;

  const [messages, setMessages] = useState([{ user: "lassi", message: initialMessage }]);
  const [inputStr, setInputStr] = useState("");
  const [verdict, setVerdict] = useState("");
  const [classtype, setClasstype] = useState("");
  const [probability, setProbability] = useState("");
  const [probabilities, setProbabilities] = useState("");

  // Retrieve messages from database
  const getClassification = async () => {
    // An empty message cannot be sent
    if (inputStr.trim() === '') {
      window.alert("Viestin lähettäminen ei ole mahdollista, sillä viesti on tyhjä. Ole hyvä ja kirjoita viesti ennen sen lähettämistä.");
    }
    else {
      setMessages(prevMessages => [...prevMessages, { user: "krister", message: inputStr }]);
      let response = null;
      // eslint-disable-next-line default-case
      switch (props.endpoint) {
        case "classify-1":
          response = await getTensorflowClassification(inputStr, initialMessage)
          setVerdict(response.verdict);
          console.log("asetettu verdict: ", verdict);
          setClasstype(response.class);
          console.log("asetettu classtype: ", classtype);
          setProbability(response.classification_probability);
          console.log("asetettu probability: ", probability);
          setProbabilities(response.probabilities);
          console.log("type: ", typeof probabilities)
          console.log("asetettu probabilities: ", probabilities);
          break;
        case "classify-2":
          response = await getCombinedClassification(inputStr, initialMessage)
          setVerdict(response.verdict);
          console.log("asetettu verdict: ", verdict);
          setClasstype(response.class);
          console.log("asetettu classtype: ", classtype);
          setProbability(response.classification_probability);
          console.log("asetettu probability: ", probability);
          setProbabilities(response.probabilities);
          console.log("type: ", typeof probabilities)
          console.log("asetettu probabilities: ", probabilities);
          break;
        case "classify-3":
          response = await getOpenAIClassification(inputStr, initialMessage)
          setVerdict(response.verdict);
          setClasstype(response.class);
          setProbability(response.classification_probability);
          setProbabilities(response.probabilities);
          break;
      };

      setInputStr("");
      const time = response['time'];
      let suggestedTime = time ? `${time.from} - ${time.to}` : '';
      setMessages(prevMessages => [...prevMessages, { user: "lassi", message: response["class"] + ' ' + suggestedTime }]);
    }
  }
  
  const handleInput = event => {
    setInputStr(event.target.value);
  };

  return (
    <div>
      <div className="messageView">
        <ul class="space-y-4 grid grid-cols-1 w-full mt-0">
          {messages && messages?.map((message) => <Message key={message.user + message.message} message={message} />)}
        </ul>
      </div>
      <div class="flex space-x-4 w-full mt-10">
        <div class="w-3/4">
          <div class="">
            <input onChange={handleInput} value={inputStr} name="message" id="message" rows="4" class="block w-full rounded-md border-0 py-2 px-3.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"></input>
          </div>
        </div>
        <div class="w-1/4">
          <button type="submit" onClick={getClassification} class="block w-full rounded-md bg-light-blue px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Send </button>
        </div>
      </div>
      <Statistics verdict={verdict} classtype={classtype} probability={probability} probabilities={probabilities} />
    </div>
  )
};
