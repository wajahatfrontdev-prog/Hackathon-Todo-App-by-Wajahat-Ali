'use client';

import { motion } from 'framer-motion';
import { Calendar, Clock, AlertCircle, CheckCircle2 } from 'lucide-react';
import { useState } from 'react';

interface TimelineTask {
  id: number;
  title: string;
  time: string;
  priority: 'high' | 'medium' | 'low';
  completed: boolean;
  dueDate: string;
}

export function TaskTimeline({ tasks }: { tasks: TimelineTask[] }) {
  const timeline = tasks.slice(0, 5);

  const priorityColors = {
    high: 'from-red-500 to-pink-500',
    medium: 'from-yellow-500 to-orange-500',
    low: 'from-blue-500 to-cyan-500'
  };

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-bold text-white flex items-center gap-2">
        <Calendar className="w-5 h-5" />
        Task Timeline
      </h3>
      <div className="relative space-y-6">
        {timeline.map((task, index) => (
          <motion.div
            key={task.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1, duration: 0.3 }}
            className="flex gap-4 group"
          >
            {/* Timeline connector */}
            <div className="relative flex flex-col items-center">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: index * 0.1 + 0.2, duration: 0.4 }}
                className={`w-10 h-10 rounded-full bg-gradient-to-br ${priorityColors[task.priority]} p-0.5 flex items-center justify-center`}
              >
                <div className="w-full h-full rounded-full bg-slate-900 flex items-center justify-center">
                  {task.completed ? (
                    <CheckCircle2 className="w-5 h-5 text-green-400" />
                  ) : (
                    <Clock className="w-5 h-5 text-slate-400" />
                  )}
                </div>
              </motion.div>
              {index < timeline.length - 1 && (
                <div className="w-0.5 h-12 bg-gradient-to-b from-slate-600 to-slate-700 mt-2" />
              )}
            </div>

            {/* Timeline content */}
            <div className="flex-1 pt-1 pb-4">
              <motion.div
                whileHover={{ x: 5 }}
                className="bg-slate-800 rounded-lg p-4 border border-slate-700 group-hover:border-slate-600 transition-all duration-300 cursor-pointer"
              >
                <div className="flex items-start justify-between mb-2">
                  <h4 className={`font-semibold ${task.completed ? 'text-slate-400 line-through' : 'text-white'}`}>
                    {task.title}
                  </h4>
                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                    task.priority === 'high' ? 'bg-red-500/20 text-red-300' :
                    task.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-300' :
                    'bg-blue-500/20 text-blue-300'
                  }`}>
                    {task.priority}
                  </span>
                </div>
                <p className="text-sm text-slate-400 flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  {task.dueDate || 'No due date'}
                </p>
              </motion.div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
