/**
 * Dashboard Page - Main user dashboard
 */

import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

export default function Dashboard() {
  const { user, token } = useContext(AuthContext);
  const navigate = useNavigate();

  if (!token) {
    return (
      <div className="container-custom py-20 text-center">
        <h1 className="text-3xl font-bold mb-4">Please Log In</h1>
        <button
          onClick={() => navigate('/login')}
          className="px-6 py-2 bg-green-600 text-white rounded-lg"
        >
          Go to Login
        </button>
      </div>
    );
  }

  return (
    <div className="container-custom py-12">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Welcome Card */}
        <div className="bg-white dark:bg-slate-800 p-6 rounded-lg border border-gray-200 dark:border-slate-700">
          <h2 className="text-xl font-bold mb-2">Welcome, {user?.name}!</h2>
          <p className="text-gray-600 dark:text-gray-400">
            {user?.state ? `From ${user.state}` : 'Tell us about your farm'}
          </p>
        </div>

        {/* Quick Stats */}
        <div className="bg-white dark:bg-slate-800 p-6 rounded-lg border border-gray-200 dark:border-slate-700">
          <h3 className="font-bold mb-4">Your Activities</h3>
          <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
            <p>Queries: 0</p>
            <p>Saved Markets: 0</p>
            <p>Crops Tracked: 0</p>
          </div>
        </div>

        {/* Actions */}
        <div className="bg-white dark:bg-slate-800 p-6 rounded-lg border border-gray-200 dark:border-slate-700">
          <h3 className="font-bold mb-4">Quick Actions</h3>
          <div className="space-y-2">
            <button className="block w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
              Check Prices
            </button>
            <button className="block w-full px-4 py-2 border border-green-600 text-green-600 rounded-lg hover:bg-green-50">
              Ask AI
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
