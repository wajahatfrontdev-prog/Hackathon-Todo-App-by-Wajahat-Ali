'use client';

import { motion } from 'framer-motion';
import { Hero } from '@/components/Hero';
import { Features } from '@/components/Features';
import { FloatingChatbot } from '@/components/FloatingChatbot';
import { CheckCircle, ArrowRight, Users, Zap, Sparkles } from 'lucide-react';
import { memo } from 'react';

const steps = [
  {
    step: '1',
    title: 'Sign Up Free',
    description: 'Create your account in under 30 seconds.',
    icon: Users
  },
  {
    step: '2',
    title: 'Add Your Tasks',
    description: 'Start organizing your tasks and priorities.',
    icon: CheckCircle
  },
  {
    step: '3',
    title: 'Stay Productive',
    description: 'Complete tasks and track your progress.',
    icon: Zap
  }
];

const HowItWorks = memo(() => (
  <div className="py-24 bg-gradient-to-br from-emerald-900 via-green-800 to-teal-700 relative overflow-hidden">
    <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="text-center mb-20"
      >
        <h2 className="text-5xl md:text-6xl font-bold text-white mb-6">
          Get Started in
          <span className="block bg-gradient-to-r from-green-300 to-emerald-300 bg-clip-text text-transparent">
            3 Simple Steps
          </span>
        </h2>
        <p className="text-xl text-green-100 max-w-3xl mx-auto">
          Join thousands of productive people in just minutes
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
        {steps.map((item, index) => (
          <motion.div
            key={item.step}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: index * 0.2 }}
            whileHover={{ scale: 1.05, y: -10 }}
            className="text-center relative group"
          >
            <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full text-white text-3xl font-bold mb-8 shadow-lg group-hover:shadow-2xl transition-all duration-300">
              {item.step}
            </div>
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl mb-6 group-hover:scale-110 transition-transform duration-300 -mt-20 relative z-10">
              <item.icon className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-3xl font-bold text-white mb-6 group-hover:text-green-300 transition-colors">
              {item.title}
            </h3>
            <p className="text-green-100 leading-relaxed text-lg">
              {item.description}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  </div>
));

HowItWorks.displayName = 'HowItWorks';

const Footer = memo(() => (
  <footer className="bg-gradient-to-br from-emerald-900 via-green-900 to-teal-900 relative overflow-hidden">
    <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="col-span-1 md:col-span-2">
          <h3 className="text-3xl font-bold text-white mb-4">Todo Pro</h3>
          <p className="text-green-100 mb-6 max-w-md">
            Organize your life with the most intuitive todo app. Simple, fast, and reliable.
          </p>
          <div className="flex gap-4">
            <motion.a
              href="/signup"
              whileHover={{ scale: 1.05 }}
              className="bg-white text-green-700 px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition-all"
            >
              Get Started
            </motion.a>
            <motion.a
              href="/login"
              whileHover={{ scale: 1.05 }}
              className="border border-white/30 text-white px-6 py-3 rounded-lg font-semibold hover:bg-white/10 transition-all"
            >
              Sign In
            </motion.a>
          </div>
        </div>
        
        <div>
          <h4 className="text-lg font-semibold text-white mb-4">Product</h4>
          <ul className="space-y-2 text-green-100">
            <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
            <li><a href="#" className="hover:text-white transition-colors">How it Works</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
          </ul>
        </div>
        
        <div>
          <h4 className="text-lg font-semibold text-white mb-4">Support</h4>
          <ul className="space-y-2 text-green-100">
            <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Contact Us</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
          </ul>
        </div>
      </div>
      
      <div className="border-t border-white/20 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
        <p className="text-green-200 text-sm">
          © 2024 Todo Pro. All rights reserved.
        </p>
        <p className="text-green-200 text-sm mt-4 md:mt-0">
          Made with ❤️ for productivity
        </p>
      </div>
    </div>
  </footer>
));

Footer.displayName = 'Footer';

export default function HomePage() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <Hero />
      <Features />
      <HowItWorks />
      <Footer />
      <FloatingChatbot />
    </motion.div>
  );
}
