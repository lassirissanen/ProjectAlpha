import { Message } from "./Message";
import { getTensorflowClassification, getCombinedClassification, getOpenAIClassification } from '../service/backend-service';
import { useState } from "react";
import './MessageList';

export const MessageList = (props) => {
  // const messages = [
  //       {user: "krister", message:"Don't stop until you're proud."},
  //       {user: "lassi", message:"hello"},
  //       {user: "krister", message:"darkness my old friend"},
  //       {user: "lassi", message:"I must have seen you again"},
  //       {user: "krister", message:"absolute pleasure"},
  //       {user: "krister", message: "block w-full rounded-md bg-light-blue px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"},
  // ] 


  const [messages, setMessages] = useState([{ user: "lassi", message: "Moi, Sopiiko sinulle hammastarkastus ensi maanantaina?" }]);
  const [inputStr, setInputStr] = useState("");
  let state = {
    message: ""
  };
  // Retrieve messages from database
  const getClassification = async () => {
    setMessages(prevMessages => [...prevMessages, { user: "krister", message: inputStr }]);
    let response = null;
    switch (props.endpoint) {
      case "classify-1":
        response = await getTensorflowClassification(inputStr)
        break;
      case "classify-2":
        response = await getCombinedClassification(inputStr)
        break;
      case "classify-3":
        response = await getOpenAIClassification(inputStr)
        break;
    };
    setInputStr("");
    setMessages(prevMessages => [...prevMessages, { user: "lassi", message: response["classification"] }]);

  }
  const handleInput = event => {
    setInputStr(event.target.value);
    //this.setState({ message: event.target.value});
  };

  return (
    <div>
      <div className="messageView">
        <ul class="space-y-12 grid grid-cols-1 w-full overflow auto">
          {messages && messages?.map((message) => <Message key={message.user + message.message} message={message} />)}
        </ul>
      </div>
      <div class="flex space-x-4 w-full mt-10" className="inputForm">
        <div class="w-3/4">
          <div class="">
            <input onChange={handleInput} value={inputStr} name="message" id="message" rows="4" class="block w-full rounded-md border-0 py-2 px-3.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"></input>
          </div>
        </div>
        <div class="w-1/4">
          <button type="submit" onClick={getClassification} class="block w-full rounded-md bg-light-blue px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Send </button>
        </div>
      </div>
    </div>

  )
}