'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Menu, X } from 'lucide-react';
import { getSession, signOut } from '@/lib/auth';

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [session, setSession] = useState<any>(null);

  useEffect(() => {
    async function checkAuth() {
      const currentSession = await getSession();
      setSession(currentSession);
    }
    checkAuth();
  }, []);

  return (
    <nav className="bg-white/90 backdrop-blur-md shadow-lg border-b border-green-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <motion.a
              href="/"
              className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 400, damping: 10 }}
            >
              ✨ Todo Pro
            </motion.a>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="/" className="text-gray-700 hover:text-green-600 transition-colors font-medium">Home</a>
            {session && (
              <>
                <a href="/dashboard" className="text-gray-700 hover:text-green-600 transition-colors font-medium">Dashboard</a>
                <a href="/chat" className="text-gray-700 hover:text-green-600 transition-colors font-medium">Chat</a>
              </>
            )}
            {!session ? (
              <>
                <a href="/login" className="text-gray-700 hover:text-green-600 transition-colors font-medium">Login</a>
                <motion.a 
                  href="/signup" 
                  className="gradient-bg text-white px-6 py-2 rounded-full hover:shadow-lg transition-all font-medium"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Get Started
                </motion.a>
              </>
            ) : (
              <motion.button
                onClick={() => signOut()}
                className="bg-red-500 text-white px-4 py-2 rounded-full hover:bg-red-600 transition-colors font-medium"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Logout
              </motion.button>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 hover:text-green-600 p-2"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <motion.div
        initial={false}
        animate={isOpen ? { height: 'auto', opacity: 1 } : { height: 0, opacity: 0 }}
        className="md:hidden bg-white/95 backdrop-blur-md border-t border-green-100 overflow-hidden"
      >
        <div className="px-4 py-4 space-y-3">
          <a href="/" className="block py-2 text-gray-700 hover:text-green-600 font-medium">Home</a>
          {session && (
            <>
              <a href="/dashboard" className="block py-2 text-gray-700 hover:text-green-600 font-medium">Dashboard</a>
              <a href="/chat" className="block py-2 text-gray-700 hover:text-green-600 font-medium">Chat</a>
            </>
          )}
          {!session ? (
            <>
              <a href="/login" className="block py-2 text-gray-700 hover:text-green-600 font-medium">Login</a>
              <a href="/signup" className="block py-3 gradient-bg text-white text-center rounded-full hover:shadow-lg font-medium">Get Started</a>
            </>
          ) : (
            <button
              onClick={() => signOut()}
              className="block w-full py-3 bg-red-500 text-white text-center rounded-full hover:bg-red-600 font-medium"
            >
              Logout
            </button>
          )}
        </div>
      </motion.div>
    </nav>
  );
}