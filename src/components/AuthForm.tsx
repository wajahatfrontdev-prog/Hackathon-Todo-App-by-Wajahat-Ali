'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Eye, EyeOff, Mail, Lock } from 'lucide-react';
import { signIn, signUp } from '../lib/auth';

export function AuthForm({ action }: { action: 'signIn' | 'signUp' }) {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      if (action === 'signUp') {
        await signUp(email, password);
        router.push('/dashboard');
      } else {
        // For sign in, check if user exists (mock check)
        const existingUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
        const userExists = existingUsers.some((user: any) => user.email === email);
        
        if (!userExists) {
          setError('Account not found. Please sign up first.');
          return;
        }
        
        await signIn(email, password);
        router.push('/dashboard');
      }
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    }
    setLoading(false);
  }

  return (
    <motion.form 
      onSubmit={handleSubmit} 
      className="space-y-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
    >
      <div className="space-y-4">
        <div className="relative">
          <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all bg-white hover:border-green-300 text-gray-900 placeholder-gray-500"
            required
          />
        </div>
        
        <div className="relative">
          <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            className="w-full pl-12 pr-12 py-4 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all bg-white hover:border-green-300 text-gray-900 placeholder-gray-500"
            required
            minLength={8}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        </div>
        
        {action === 'signUp' && (
          <p className="text-sm text-gray-500 flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
            Must be at least 8 characters
          </p>
        )}
      </div>

      {error && (
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="p-4 bg-red-50 border border-red-200 rounded-xl"
        >
          <p className="text-sm text-red-600 flex items-center gap-2">
            <span className="w-2 h-2 bg-red-500 rounded-full"></span>
            {error}
          </p>
        </motion.div>
      )}

      <motion.button
        type="submit"
        disabled={loading}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="w-full gradient-bg text-white py-4 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        {loading && (
          <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
        )}
        {loading ? 'Please wait...' : (action === 'signUp' ? 'Create Account' : 'Sign In')}
      </motion.button>
    </motion.form>
  );
}