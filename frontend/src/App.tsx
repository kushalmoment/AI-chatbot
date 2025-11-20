import React, { useState, useEffect } from 'react';
import ChatWindow from './components/ChatWindow';
import Login from './components/Login';
import { onAuthStateChange, logout } from './services/auth';
import './App.css';

function App() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChange((user) => {
      setUser(user);
    });
    return unsubscribe;
  }, []);

  const handleLogout = async () => {
    await logout();
  };

  return (
    <div className="App" style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header className="App-header" style={{ padding: '1rem', backgroundColor: '#1a73e8', color: 'white', textAlign: 'center' }}>
        <h1>AI Chatbot</h1>
        {user && <button onClick={handleLogout} style={{ position: 'absolute', right: '1rem', top: '1rem' }}>Logout</button>}
      </header>
      <main style={{ flexGrow: 1 }}>
        {user ? <ChatWindow user={user} /> : <Login onLogin={() => {}} />}
      </main>
    </div>
  );
}

export default App;
