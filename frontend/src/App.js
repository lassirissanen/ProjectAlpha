import './App.css';
import ChatView from './chat/ChatView';

function App() {
  return (
    <div class="h-screen flex flex-col justify-center items-center content-start">
      <div class="w-screen md:w-1/2 lg:w-1/3" id="chat">
        <ChatView />
      </div>
    </div>
  );
}

export default App;