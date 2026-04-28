import { Link } from 'react-router-dom';
import { GraduationCap, Bot, BookOpen, Clock, Shield, LogOut, MessageCircle } from 'lucide-react';
import { supabase } from '../supabaseClient';
import { useState } from 'react';
import Chat from './Chat';

export default function Landing({ session }) {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div className="min-h-screen font-sans relative flex flex-col bg-slate-900">
      {/* Navigation */}
      <nav className="border-b bg-white border-slate-100 shrink-0 z-20 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-primary/10 rounded-lg">
              <GraduationCap className="h-6 w-6 text-primary" />
            </div>
            <span className="text-xl font-bold text-slate-900 tracking-tight">Nexus Edu</span>
          </div>
          {session ? (
            <button
              onClick={() => supabase.auth.signOut()}
              className="inline-flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 px-4 py-2 rounded-lg transition-colors"
            >
              <LogOut className="h-4 w-4" /> Sign Out
            </button>
          ) : (
            <Link
              to="/auth"
              className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-slate-900 hover:bg-slate-800 rounded-lg transition-colors"
            >
              Login to Portal
            </Link>
          )}
        </div>
      </nav>

      {/* Main Content Area (Fills remaining height) */}
      <main className="relative flex-1 flex flex-col justify-center items-center overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 z-0">
          <img 
            src="/hero-bg.png" 
            alt="School Campus" 
            className="w-full h-full object-cover opacity-30"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-slate-900/50 via-slate-900/60 to-slate-900"></div>
        </div>
        
        {/* Hero Content */}
        <div className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center pt-10 pb-8 flex-1 flex flex-col justify-center">
          <div>
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 text-white text-sm font-medium mb-6 border border-white/20 backdrop-blur-sm">
              <Bot className="h-4 w-4" />
              <span>Your Personal AI School Assistant</span>
            </div>
            <h1 className="text-5xl md:text-7xl font-extrabold text-white tracking-tight leading-tight mb-4 drop-shadow-lg">
              Education meets <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">Intelligent Communication</span>
            </h1>
            <p className="text-xl text-slate-200 mb-8 max-w-2xl mx-auto leading-relaxed font-light drop-shadow-md">
              "Education is the passport to the future, tomorrow belongs to those who prepare for it today."
            </p>
          </div>

          {/* Features Grid inside Hero */}
          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto mt-8">
            {[
              {
                icon: <Clock className="h-6 w-6 text-indigo-400" />,
                title: "24/7 Availability",
                desc: "Get instant answers about exam schedules, vacations, and policies anytime."
              },
              {
                icon: <BookOpen className="h-6 w-6 text-emerald-400" />,
                title: "Live Database Access",
                desc: "Real-time textbook & fee updates."
              },
              {
                icon: <Shield className="h-6 w-6 text-rose-400" />,
                title: "Secure & Private",
                desc: "Row-Level Security protects your data."
              }
            ].map((feature, i) => (
              <div key={i} className="bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/20 text-left hover:bg-white/15 transition-all">
                <div className="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-slate-300 text-sm leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Floating Chat Button */}
      {session && !isChatOpen && (
        <button
          onClick={() => setIsChatOpen(true)}
          className="fixed bottom-6 right-6 pl-5 pr-6 py-4 bg-primary text-white rounded-full shadow-2xl hover:bg-blue-700 transition-all hover:scale-105 z-50 flex items-center gap-3 border border-blue-500"
        >
          <MessageCircle className="h-6 w-6" />
          <span className="font-semibold text-[15px]">Ask Nexus AI</span>
        </button>
      )}

      {/* Chat Pop-up Window */}
      {session && isChatOpen && (
        <div className="fixed bottom-6 right-6 w-[450px] h-[700px] max-w-[calc(100vw-3rem)] max-h-[calc(100vh-3rem)] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden z-50 border border-slate-200">
          <Chat session={session} onClose={() => setIsChatOpen(false)} />
        </div>
      )}
    </div>
  );
}
