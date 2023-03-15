import { Button, Container, Box, TextField } from "@material-ui/core";
import { withStyles } from "@material-ui/core/styles";
import React from "react";
import { render } from "react-dom";
import {
  ChatFeed,
  Message,
} from "react-chat-ui";
import AWS from 'aws-sdk';


// Initialize the Amazon Cognito credentials provider
AWS.config.region = "us-west-2"; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
  IdentityPoolId: "us-west-2:83ff2f15-0f48-4309-af55-6e2b8563a8f1"
});

// CREATE THE LEX RUNTIME
let lexRunTime = new AWS.LexRuntime();
let lexUserId = "LumiSightBot" + Date.now();
var classification = "vakio";

// @todo: dev only
AWS.config.credentials.get(function (err) {
  if (err) console.log(err);
  else console.log(AWS.config.credentials);
});

const ERR_MSG = "Trouble connecting to the server."; 

const buildLexParams = (message) => ({
  botAlias: "$LATEST",
  botName: "LumiBot",
  inputText: message,
  userId: lexUserId,
});

const muiStyles = {
  form: {
    borderTop: '1px solid black',
    height: '100%',
    display: 'flex',
    justifyContent: 'space-between',
    padding: '10px',
  },
  container: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    padding: '10px'
  },
  chat: {
    height: "95%",
  },
  text: {
    width: "80%",
    height: "100%",
    border: 'none',
    fontFamily: 'Roboto',
    fontSize: '15px'
  },
  sendButton: {
    width: "10%",
    height: "100%",
    backgroundColor: "#fff",
    borderColor: "#1D2129",
    borderStyle: "solid",
    borderRadius: 30,
    borderWidth: 2,
    color: "#1D2129",
    fontWeight: "300",
  }
};
function getClassification(msg){
const answer = new URLSearchParams();

answer.append('message', msg);

fetch('http://localhost:5000/classify-1',{
  method: 'post',
  body: answer,
})
.then(function (response) {
	// The API call was successful!
	return response.text();
}).then(function (html) {
	// This is the HTML from our response as a text string
	console.log(html);
  classification = html;
  console.log("muutettu");
}).catch(function (err) {
	// There was an error
	console.warn('Something went wrong.', err);
});

}
class Chat extends React.Component {
  constructor(props) {
    super(props);
    this.classes = this.props.classes;
    this.state = {
      isTyping: false,
      messages: [
        new Message({ id: 1, message: "Käykö sulle hampilääkäri 14.4.?", senderName: "botti" }),
      ],
      currentUser: "You"
    };
  }

  onMessageSubmit(e) {
    const input = this.message;
    e.preventDefault();
    if (!input.value) {
      return false;
    }
    getClassification(input);
    this.pushMessage(0, input.value);
    lexRunTime.postText(buildLexParams(input.value), (err, data) => {
      if (err) {
        this.pushMessage(1, ERR_MSG);
        return false; 
      }
      this.pushMessage(1, classification);
      input.value = '';
      return true;
    });
  }

  pushMessage(recipient = 0, message) {
    const prevState = this.state;
    const newMessage = new Message({
      id: recipient,
      message,
      senderName: "botti",
    });
    prevState.messages.push(newMessage);
    this.setState(this.state);
  }

  render() {
    return (
      <div className={this.classes.container}>
        <div className={this.classes.chat}>
          <ChatFeed
            messages={this.state.messages}
            isTyping={this.state.isTyping}
            showSenderName
            bubbleStyles={{
              text: {
                fontSize: 15,
              },
              chatbubble: {
                borderRadius: 35,
                padding: 15,
              },
            }}
          />
        </div>
        <div style={{ height: '5%', marginBottom: '30px' }}>
          <form onSubmit={(e) => this.onMessageSubmit(e)} className={this.classes.form}>
            <input
              className={this.classes.text}
              ref={(m) => {
                this.message = m;
              }}
              placeholder="Type a message here..."
            />
            <input className={this.classes.sendButton} type="submit" value="Send"></input>
          </form>
        </div>
      </div>
    );
  }
}

const StyleChat = withStyles(muiStyles)(Chat);
render(<StyleChat />, document.getElementById("root"));
