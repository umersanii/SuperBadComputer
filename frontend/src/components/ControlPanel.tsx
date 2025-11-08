'use client';

import { useState } from 'react';
import { ref, set } from 'firebase/database';
import { database } from '@/lib/firebase';

export default function ControlPanel() {
  const [loading, setLoading] = useState(false);

  const sendCommand = async (command: string) => {
    setLoading(true);
    try {
      const commandRef = ref(database, 'pi/commands');
      await set(commandRef, {
        command,
        timestamp: Date.now(),
      });
      alert(`Command "${command}" sent successfully!`);
    } catch (error) {
      console.error('Error sending command:', error);
      alert('Failed to send command');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
      <h2 className="text-2xl font-semibold mb-4">Control Panel</h2>
      
      <div className="space-y-3">
        <button
          onClick={() => sendCommand('restart')}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
        >
          Restart Service
        </button>
        
        <button
          onClick={() => sendCommand('update_status')}
          disabled={loading}
          className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
        >
          Update Status
        </button>
        
        <button
          onClick={() => sendCommand('clear_cache')}
          disabled={loading}
          className="w-full bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
        >
          Clear Cache
        </button>
        
        <button
          onClick={() => sendCommand('shutdown')}
          disabled={loading}
          className="w-full bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
        >
          Shutdown
        </button>
      </div>
      
      {loading && (
        <div className="mt-4 text-center text-gray-400">
          Sending command...
        </div>
      )}
    </div>
  );
}
