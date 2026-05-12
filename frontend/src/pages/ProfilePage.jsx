/**
 * Profile Page - User profile management
 */

import React, { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';

const states = ['Bihar', 'Punjab', 'Haryana', 'Delhi', 'Maharashtra'];

export default function ProfilePage() {
  const { user } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    state: user?.state || '',
    phone: user?.phone || '',
    cropsProduce: user?.cropsProduce || []
  });

  const handleSave = async () => {
    // Call API to update profile
    console.log('Saving:', formData);
  };

  return (
    <div className="container-custom py-12">
      <h1 className="text-3xl font-bold mb-8">My Profile</h1>

      <div className="max-w-2xl bg-white dark:bg-slate-800 p-8 rounded-lg border border-gray-200 dark:border-slate-700">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">State</label>
            <select
              value={formData.state}
              onChange={(e) => setFormData({...formData, state: e.target.value})}
              className="w-full"
            >
              <option value="">Select State</option>
              {states.map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Phone</label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})}
              className="w-full"
            />
          </div>

          <button
            onClick={handleSave}
            className="w-full px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
}
