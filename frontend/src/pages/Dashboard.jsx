/**
 * Dashboard Page - Main user dashboard
 */

import React from 'react';

export default function Dashboard() {
  return (
    <div className="container-custom py-12">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Welcome Card */}
        <div className="bg-white dark:bg-slate-800 p-6 rounded-lg border border-gray-200 dark:border-slate-700">
          <h2 className="text-xl font-bold mb-2">Welcome to AgroAI</h2>
          <p className="text-gray-600 dark:text-gray-400">
            Your agricultural market intelligence assistant
          </p>
        </div>

        {/* Quick Stats */}
        <div className="bg-white dark:bg-slate-800 p-6 rounded-lg border border-gray-200 dark:border-slate-700">
          <h3 className="font-bold mb-4">Quick Features</h3>
          <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
            <p>✓ Live Mandi Prices</p>
            <p>✓ Price Trends & Predictions</p>
            <p>✓ Sell/Wait Recommendations</p>
          </div>
        </div>

        {/* Actions */}
        <div className="bg-white dark:bg-slate-800 p-6 rounded-lg border border-gray-200 dark:border-slate-700">
          <h3 className="font-bold mb-4">Get Started</h3>
          <button className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition">
            Go to Chat
          </button>
        </div>
      </div>
    </div>
  );
}
