'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, X } from 'lucide-react';
import { ChatInterface } from '@/components/ChatInterface';
import { getSession } from '../../lib/auth';
import { useRouter } from 'next/navigation';

export default function ChatPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    async function checkAuth() {
      try {
        const session = await getSession();
        if (!session?.user) {
          setIsAuthenticated(false);
        } else {
          setIsAuthenticated(true);
        }
      } catch (error) {
        setIsAuthenticated(false);
      }
      setIsLoading(false);
    }
    checkAuth();
  }, [router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="relative">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
              className="w-16 h-16 border-4 border-green-200 border-t-green-600 rounded-full mx-auto mb-4"
            />
            <Sparkles className="w-8 h-8 text-green-600 mx-auto -mt-10 relative z-10" />
          </div>
          <p className="text-green-700 font-medium">Loading your AI assistant...</p>
        </motion.div>
      </div>
    );
  }

  if (!isAuthenticated && !isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center bg-white rounded-2xl p-8 shadow-xl max-w-md mx-4"
        >
          <div className="mb-6">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <X className="w-8 h-8 text-red-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Authentication Required</h2>
            <p className="text-gray-600">Please log in to access the AI chat assistant.</p>
          </div>
          <div className="space-y-3">
            <a
              href="/login"
              className="block w-full bg-green-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-green-700 transition-colors"
            >
              Sign In
            </a>
            <a
              href="/signup"
              className="block w-full border border-green-600 text-green-600 py-3 px-6 rounded-lg font-medium hover:bg-green-50 transition-colors"
            >
              Create Account
            </a>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50"
    >
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent mb-2">
            AI Task Assistant
          </h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Chat with your AI assistant to manage your tasks using natural language.
            Create, update, complete, and organize your tasks effortlessly.
          </p>
        </motion.div>

        <ChatInterface />
      </div>
    </motion.div>
  );
}
