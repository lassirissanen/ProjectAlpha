import { getTensorflowClassification, getCombinedClassification, getOpenAIClassification } from '../service/backend-service';
import React from 'react';

export class SendMessage extends React.Component {


  messages = [
        {user: "krister", message:"Don't stop until you're proud."},
        {user: "lassi", message:"hello"},
        {user: "krister", message:"darkness my old friend"},
        {user: "lassi", message:"I must have seen you again"},
        {user: "krister", message:"absolute pleasure"},
    ] // Retrieve messages from database

    state = {
        message: ""
    };

    handleInput = event =>  {
        this.setState({ message: event.target.value});
    };

    getClassification = async () => {    
        const response = await getTensorflowClassification(this.state.message);
        
    }

  render() {
        return;
            // <div class="flex space-x-4 w-full mt-10">
            //     <div class="w-3/4">
            //         <div class="">
            //             <input onChange={this.handleInput} name="message" id="message" rows="4" class="block w-full rounded-md border-0 py-2 px-3.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"></input>
            //         </div>
            //     </div>
            //     <div class="w-1/4">
            //         <button type="submit" onClick={this.getClassification} class="block w-full rounded-md bg-light-blue px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Send </button>
            //     </div>
            // </div>
        
    }
}
