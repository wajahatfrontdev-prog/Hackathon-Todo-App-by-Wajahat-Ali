'use client';

import { motion } from 'framer-motion';
import { BarChart3, LineChart, PieChart, TrendingUp } from 'lucide-react';
import { useState } from 'react';

export function ProductivityChart() {
  const [chartType, setChartType] = useState('weekly');

  const weeklyData = [
    { day: 'Mon', tasks: 8, completed: 6 },
    { day: 'Tue', tasks: 12, completed: 10 },
    { day: 'Wed', tasks: 10, completed: 9 },
    { day: 'Thu', tasks: 15, completed: 12 },
    { day: 'Fri', tasks: 14, completed: 13 },
    { day: 'Sat', tasks: 5, completed: 5 },
    { day: 'Sun', tasks: 6, completed: 4 }
  ];

  const maxTasks = Math.max(...weeklyData.map(d => d.tasks));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <BarChart3 className="w-5 h-5" />
          Productivity Insights
        </h3>
        <div className="flex gap-2">
          {['weekly', 'monthly'].map((type) => (
            <button
              key={type}
              onClick={() => setChartType(type)}
              className={`px-3 py-1 rounded-lg text-sm font-medium transition-all ${
                chartType === type
                  ? 'bg-purple-500 text-white'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700">
        <div className="flex items-end justify-between gap-2 h-48">
          {weeklyData.map((data, index) => (
            <motion.div
              key={data.day}
              initial={{ height: 0 }}
              animate={{ height: `${(data.tasks / maxTasks) * 100}%` }}
              transition={{ delay: index * 0.1, duration: 0.6, ease: 'easeOut' }}
              className="flex-1 flex flex-col items-end justify-end gap-1 group cursor-pointer"
            >
              {/* Completed tasks bar */}
              <motion.div
                className="w-full bg-gradient-to-t from-green-500 to-emerald-400 rounded-t-lg transition-all duration-200 group-hover:shadow-lg group-hover:shadow-green-500/50"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: index * 0.1 + 0.2, duration: 0.4 }}
                style={{ height: `${(data.completed / maxTasks) * 100}%` }}
              />
              {/* Total tasks bar background */}
              <div className="w-full flex-1 bg-slate-700 rounded-t-lg opacity-30" />
              
              {/* Label */}
              <p className="text-xs font-semibold text-slate-400 mt-2 group-hover:text-white transition-colors">
                {data.day}
              </p>
              {/* Tooltip */}
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                whileHover={{ opacity: 1, y: -10 }}
                className="absolute bg-slate-900 text-white text-xs px-2 py-1 rounded pointer-events-none whitespace-nowrap"
              >
                {data.completed}/{data.tasks} completed
              </motion.div>
            </motion.div>
          ))}
        </div>

        {/* Legend */}
        <div className="flex items-center justify-center gap-6 mt-8">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500" />
            <span className="text-sm text-slate-400">Completed</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-slate-600" />
            <span className="text-sm text-slate-400">Pending</span>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { label: 'Avg Daily', value: Math.round(weeklyData.reduce((a, d) => a + d.completed, 0) / 7), color: 'from-blue-500 to-cyan-500' },
          { label: 'This Week', value: weeklyData.reduce((a, d) => a + d.completed, 0), color: 'from-green-500 to-emerald-500' },
          { label: 'Success Rate', value: `${Math.round((weeklyData.reduce((a, d) => a + d.completed, 0) / weeklyData.reduce((a, d) => a + d.tasks, 0)) * 100)}%`, color: 'from-purple-500 to-pink-500' }
        ].map((stat) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={`bg-gradient-to-br ${stat.color} p-4 rounded-xl`}
          >
            <p className="text-white/80 text-xs font-medium mb-1">{stat.label}</p>
            <p className="text-2xl font-bold text-white">{stat.value}</p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
