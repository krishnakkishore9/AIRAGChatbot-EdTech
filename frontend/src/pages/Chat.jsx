import { useState, useEffect, useRef } from 'react';
import { supabase } from '../supabaseClient';
import { Send, Bot, User, Loader2, X } from 'lucide-react';

export default function Chat({ session, onClose }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    const fetchHistory = async () => {
      const { data } = await supabase
        .from('chat_history')
        .select('*')
        .eq('user_id', session.user.id)
        .order('created_at', { ascending: true })
        .limit(20);
      
      if (data) {
        setMessages(data.map(m => ({ text: m.message, isBot: m.role === 'assistant' })));
      }
    };
    fetchHistory();
  }, [session.user.id]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { text: userMessage, isBot: false }]);
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          user_id: session.user.id
        })
      });

      const data = await res.json();
      setMessages(prev => [...prev, { text: data.reply, isBot: true }]);
    } catch (error) {
      setMessages(prev => [...prev, { text: 'Sorry, the server is currently unavailable.', isBot: true }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <header className="bg-white border-b border-slate-200 px-4 py-3 flex justify-between items-center shrink-0">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-md">
            <Bot className="h-6 w-6 text-primary" />
          </div>
          <div>
            <h2 className="font-semibold text-slate-900 text-base">Virtual Assistant</h2>
            <p className="text-sm text-slate-500">RAG-powered support</p>
          </div>
        </div>
        <button onClick={onClose} className="p-2 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition-colors">
          <X className="h-6 w-6" />
        </button>
      </header>

      <main className="flex-1 overflow-y-auto p-5 space-y-5 bg-slate-50 text-base">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-slate-400 space-y-4">
            <Bot className="h-12 w-12 opacity-50" />
            <p className="text-center px-4 text-base">Send a message to start chatting with the school assistant!</p>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-3 ${msg.isBot ? '' : 'flex-row-reverse'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.isBot ? 'bg-primary/10 text-primary' : 'bg-slate-200 text-slate-600'}`}>
              {msg.isBot ? <Bot className="h-5 w-5" /> : <User className="h-5 w-5" />}
            </div>
            <div className={`px-5 py-3 rounded-2xl max-w-[85%] shadow-sm text-base leading-relaxed whitespace-pre-wrap ${
              msg.isBot 
                ? 'bg-white border border-slate-100 text-slate-800 rounded-tl-sm' 
                : 'bg-primary text-white rounded-tr-sm'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center shrink-0">
              <Bot className="h-5 w-5" />
            </div>
            <div className="px-5 py-3 rounded-2xl bg-white border border-slate-100 flex items-center shadow-sm rounded-tl-sm">
              <Loader2 className="h-5 w-5 text-primary animate-spin" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      <footer className="bg-white border-t border-slate-200 p-4 shrink-0">
        <form onSubmit={handleSend} className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question..."
            className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-4 pr-12 py-3.5 text-base focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="absolute right-2 p-2 bg-primary hover:bg-blue-700 text-white rounded-lg disabled:opacity-50 disabled:hover:bg-primary transition-colors"
          >
            <Send className="h-5 w-5" />
          </button>
        </form>
      </footer>
    </>
  );
}
