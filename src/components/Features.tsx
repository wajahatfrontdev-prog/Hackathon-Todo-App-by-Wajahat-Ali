'use client';

import { motion } from 'framer-motion';
import { Shield, Database, Users, Smartphone, Zap, Clock, Target, Award } from 'lucide-react';
import { memo } from 'react';

const features = [
  {
    icon: Shield,
    title: 'Bank-Level Security',
    description: 'Your data is protected with enterprise-grade encryption and security protocols'
  },
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Optimized performance ensures your tasks load instantly, anywhere, anytime'
  },
  {
    icon: Target,
    title: 'Smart Prioritization',
    description: 'AI-powered algorithms help you focus on what matters most for maximum productivity'
  },
  {
    icon: Users,
    title: 'Team Collaboration',
    description: 'Share projects, assign tasks, and collaborate seamlessly with your team members'
  },
  {
    icon: Clock,
    title: 'Time Tracking',
    description: 'Built-in time tracking and analytics to understand your productivity patterns'
  },
  {
    icon: Smartphone,
    title: 'Cross-Platform Sync',
    description: 'Access your tasks on any device with real-time synchronization across all platforms'
  },
  {
    icon: Database,
    title: 'Cloud Backup',
    description: 'Never lose your data with automatic cloud backups and version history'
  },
  {
    icon: Award,
    title: 'Productivity Insights',
    description: 'Detailed analytics and reports to track your progress and optimize your workflow'
  }
];

const stats = [
  { value: '10K+', label: 'Happy Users' },
  { value: '500K+', label: 'Tasks Managed' },
  { value: '99%', label: 'User Satisfaction' },
  { value: 'Fast', label: '& Reliable' }
];

export const Features = memo(() => {
  return (
    <div className="py-24 bg-gradient-to-br from-emerald-900 via-green-800 to-teal-700 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-white/5 to-transparent"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-20"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Everything You Need to
            <span className="block bg-gradient-to-r from-green-300 to-emerald-300 bg-clip-text text-transparent">
              Stay Organized
            </span>
          </h2>
          <p className="text-xl text-green-100 max-w-3xl mx-auto leading-relaxed">
            Powerful features designed to boost your productivity and help you achieve your goals faster than ever before.
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: index * 0.1 }}
              className="group card-hover bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20 shadow-sm hover:shadow-xl hover:border-white/30 transition-all duration-300"
            >
              <div className="inline-flex items-center justify-center w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl mb-6 group-hover:scale-110 transition-transform duration-300">
                <feature.icon className="w-8 h-8 text-green-200" />
              </div>
              <h3 className="text-xl font-bold text-white mb-4 group-hover:text-green-200 transition-colors">
                {feature.title}
              </h3>
              <p className="text-green-100 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="mt-24 grid grid-cols-2 md:grid-cols-4 gap-8 text-center"
        >
          {stats.map((stat, index) => (
            <div key={index} className="p-6">
              <div className="text-4xl font-bold text-green-300 mb-2">{stat.value}</div>
              <div className="text-green-100 font-medium">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </div>
    </div>
  );
});