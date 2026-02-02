import { useState } from 'react'
import './App.css'
const API_URL = import.meta.env.VITE_API_URL;

function App() {
   const [open , setOpen] = useState(false);
   const [messages,setMessages] = useState([]);
   const [question,setQuestion] = useState("");
   const [loading,setLoading] = useState(false);

   const askQuestion = async() => {
    if(!question.trim() || loading) return;
    const userMessage = {role:"user" , text:question};
    setMessages((prev) => [...prev , userMessage])
    setQuestion("");
    setLoading(true);
    try{
      const res = await fetch(`${API_URL}/ask`,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({question}),
      });

      const data = await res.json();
      setMessages((prev)=>[...prev,{role:"bot" , text: data.answer}]);
    }catch{
      setMessages((prev)=>[...prev,{role:"bot" , text:"!Server Error"}]);
    }finally{
      setLoading(false)
    }
   };
  return (
    <>
      <button className="chat-toggle" onClick={() => setOpen(!open)}>
        💬
      </button>


      {open && (
        <div className="chat-widget">
          <div className="chat-header">
            <span>Q&A chatbot</span>
            <button onClick={() => setOpen(false)}>✕</button>
          </div>

          <div className="chat-body">
            {messages.map((msg, i) => (
              <div key={i} className={`msg ${msg.role}`}>
                {msg.text}
              </div>
            ))}
            {loading && <div className="msg bot">Thinking...</div>}
          </div>

          <div className="chat-input">
            <textarea
              placeholder="Ask something..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) =>
                e.key === "Enter" && !e.shiftKey && askQuestion()
              }
            />
            <button onClick={askQuestion}>Send</button>
          </div>
        </div>
      )}
    </>
  )
}

export default App
