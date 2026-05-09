import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./Home.css";
import { ToastContainer, toast } from 'react-toastify';

const Home = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
  
    const userMessage = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true); // Show loading animation
  
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/get`, { msg: input });
      const botMessage = { text: response.data.response, sender: "bot" };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      toast.error(error.response?.data?.error || "Error getting response!",{
        position: 'top-center',
      });
      console.error("Error fetching response:", error);
      const errorMessage = { text: "Error getting response!", sender: "bot" };
      setMessages((prev) => [...prev, errorMessage]);
    }
    finally{
      setLoading(false); // Hide loading animation after response
    }
  };
  

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <>
    <ToastContainer/>
    <div className="chat-container">
      <div className="chat-header">
        <img
          src="https://cdn-icons-png.flaticon.com/512/387/387569.png"
          alt="bot"
          className="bot-icon"
        />
        <h2>Medical Chatbot</h2>
      </div>

      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.sender}`}>
            {msg.sender === "bot" && (
              <img
                src="https://cdn-icons-png.flaticon.com/512/387/387569.png"
                alt="bot"
                className="bot-icon-msg"
              />
            )}
            <p>{msg.text}</p>
          </div>
        ))}

        {/* Loading Animation when waiting for bot response */}
        {loading && (
          <div className="chat-message bot">
            <img
              src="https://cdn-icons-png.flaticon.com/512/387/387569.png"
              alt="bot"
              className="bot-icon-msg"
            />
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      <form className="chat-input" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
    </>
  );
};

export default Home;
