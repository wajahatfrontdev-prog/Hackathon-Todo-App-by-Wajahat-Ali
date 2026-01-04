'use client';

import { motion } from 'framer-motion';
import { BarChart3, TrendingUp, Calendar, Target } from 'lucide-react';
import { useState, useEffect } from 'react';

interface AnalyticsData {
  completionRate: number;
  tasksCompleted: number;
  totalTasks: number;
  productivity: number;
  streak: number;
}

export function Analytics() {
  const [data, setData] = useState<AnalyticsData>({
    completionRate: 75,
    tasksCompleted: 24,
    totalTasks: 32,
    productivity: 89,
    streak: 7
  });

  const stats = [
    { label: 'Completion Rate', value: `${data.completionRate}%`, icon: Target, color: 'from-blue-500 to-cyan-500' },
    { label: 'Tasks Completed', value: data.tasksCompleted, icon: CheckCircle, color: 'from-green-500 to-emerald-500' },
    { label: 'Productivity', value: `${data.productivity}%`, icon: TrendingUp, color: 'from-purple-500 to-pink-500' },
    { label: 'Current Streak', value: `${data.streak}d`, icon: Flame, color: 'from-orange-500 to-red-500' }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, index) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1, duration: 0.3 }}
          className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-slate-700 hover:border-slate-600 transition-all duration-300"
        >
          <div className="flex items-start justify-between mb-4">
            <div className={`bg-gradient-to-br ${stat.color} p-3 rounded-lg`}>
              <stat.icon className="w-6 h-6 text-white" />
            </div>
          </div>
          <h3 className="text-slate-400 text-sm font-medium mb-2">{stat.label}</h3>
          <p className="text-3xl font-bold text-white mb-2">{stat.value}</p>
          <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${data.completionRate}%` }}
              transition={{ delay: index * 0.1 + 0.3, duration: 0.8 }}
              className={`h-full bg-gradient-to-r ${stat.color}`}
            />
          </div>
        </motion.div>
      ))}
    </div>
  );
}

import { CheckCircle, Flame } from 'lucide-react';
