'use client';

import { motion } from 'framer-motion';
import { Sparkles, ArrowRight } from 'lucide-react';
import { memo } from 'react';

export const Hero = memo(() => {
  return (
    <div className="relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-emerald-900 via-green-800 to-teal-700">
        <div className="absolute inset-0 opacity-20"></div>
      </div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
        <div className="text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
            className="flex justify-center mb-6"
          >
            <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full border border-white/30">
              <Sparkles className="w-4 h-4 text-green-200" />
              <span className="text-sm font-medium text-white">New: AI-Powered Task Management</span>
            </div>
          </motion.div>
          
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2, delay: 0.1 }}
            className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight"
          >
            Organize Your Life with
            <span className="block bg-gradient-to-r from-green-300 to-emerald-300 bg-clip-text text-transparent">
              Todo Pro
            </span>
          </motion.h1>
          
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2, delay: 0.2 }}
            className="text-xl md:text-2xl text-green-100 mb-8 max-w-3xl mx-auto leading-relaxed"
          >
            Transform your productivity with intelligent task management, 
            smart prioritization, and seamless collaboration tools.
          </motion.p>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2, delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <motion.a
              href="/signup"
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
              className="group bg-white text-green-700 px-8 py-4 rounded-full font-semibold text-lg shadow-lg hover:shadow-xl transition-all flex items-center gap-2"
            >
              Start Free Today
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </motion.a>
            <motion.a
              href="/login"
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
              className="border-2 border-white text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-white/10 transition-all"
            >
              Sign In
            </motion.a>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2, delay: 0.4 }}
            className="mt-12 flex justify-center items-center gap-8 text-sm text-green-200"
          >
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-300 rounded-full"></div>
              <span>Free Forever</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-300 rounded-full"></div>
              <span>No Credit Card</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-300 rounded-full"></div>
              <span>Setup in 2 Minutes</span>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
});