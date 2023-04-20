import { MessageList } from "./MessageList";
import { useState } from "react";
import './MessageList.css';

function ChatView() {
    const endpoints = [
        {
            value: "classify-1",
            name: "tensorflow"
        },
        {
            value: "classify-2",
            name: "mixed"
        },
        {
            value: "classify-3",
            name: "OpenAI"
        },
    ]
    const [endpoint, setEndpoint] = useState("classify-1")

    const handleSelectEndpoint = (event) => {
        setEndpoint(event.target.value);
        console.log(endpoint);
    }

    return (
        <div class="chat-view flex flex-col justify-start items-center w-full h-screen">
            <header class="p-16 h-1 mb-8">
                <h1 class="text-3xl">chat view</h1>
                <select onInput={handleSelectEndpoint} id="endpoint-select" name="endpoints" class="mt-1">
                    {endpoints.map(e => <option value={e.value} key={e.value}>{e.name}</option>)}
                </select>
            </header>
            <MessageList endpoint={endpoint} />
        </div>
    );
}

export default ChatView;
