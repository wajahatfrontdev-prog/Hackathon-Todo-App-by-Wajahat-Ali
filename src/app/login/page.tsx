'use client';

import { motion } from 'framer-motion';
import { AuthForm } from '@/components/AuthForm';
import { ArrowLeft, Sparkles } from 'lucide-react';

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-900 via-green-800 to-teal-700 flex items-center justify-center p-4">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute inset-0"></div>
      </div>
      
      <motion.div 
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6 }}
        className="relative w-full max-w-md"
      >
        {/* Back to Home */}
        <motion.a
          href="/"
          className="inline-flex items-center gap-2 text-white/80 hover:text-white mb-8 transition-colors"
          whileHover={{ x: -5 }}
        >
          <ArrowLeft className="w-4 h-4" />
          <span className="text-sm font-medium">Back to Home</span>
        </motion.a>
        
        {/* Main Card */}
        <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/30 p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
              className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl mb-6 shadow-lg"
            >
              <Sparkles className="w-8 h-8 text-white" />
            </motion.div>
            
            <motion.h1 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-3xl font-bold text-gray-900 mb-2"
            >
              Welcome Back
            </motion.h1>
            
            <motion.p 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-gray-600"
            >
              Sign in to access your todo dashboard
            </motion.p>
          </div>

          {/* Auth Form */}
          <AuthForm action="signIn" />
          
          {/* Footer */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="mt-8 text-center"
          >
            <p className="text-gray-600 text-sm">
              Don't have an account?{' '}
              <motion.a
                href="/signup"
                className="text-green-600 hover:text-green-700 font-semibold transition-colors"
                whileHover={{ scale: 1.05 }}
              >
                Sign up for free
              </motion.a>
            </p>
          </motion.div>
        </div>
        
        {/* Trust Indicators */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="mt-8 flex justify-center items-center gap-6 text-xs text-white/70"
        >
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>Secure Login</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>256-bit SSL</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>GDPR Compliant</span>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}