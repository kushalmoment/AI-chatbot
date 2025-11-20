import React, { useState } from "react";
import { sendMessage } from "../services/apiClients";
import "../App.css";

interface ChatItem {
  role: "user" | "assistant";
  content: string;
}

interface ChatWindowProps {
  user: any;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ user }) => {
  const [input, setInput] = useState("");
  const [history, setHistory] = useState<ChatItem[]>([]);

  const onSend = async () => {
    if (!input.trim() || !user) return;
    const userMsg = input;
    setHistory([...history, { role: "user", content: userMsg }]);
    setInput("");
    try {
      const reply = await sendMessage(user.uid, userMsg);
      setHistory((prev) => [...prev, { role: "assistant", content: reply }]);
    } catch (err) {
      setHistory((prev) => [...prev, { role: "assistant", content: "応答に失敗しました。" }]);
    }
  };

  return (
    <div className="chat-window">
      <div className="messages-area">
        {history.map((item, index) => (
          <div key={index} style={{ marginBottom: "1rem" }}>
            <strong>{item.role === "user" ? "You" : "AI"}:</strong> {item.content}
          </div>
        ))}
      </div>
      <div className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyPress={(e) => e.key === "Enter" && onSend()}
        />
        <button onClick={onSend}>Send</button>
      </div>
    </div>
  );
};

export default ChatWindow;
