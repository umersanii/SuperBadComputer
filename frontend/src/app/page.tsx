'use client';

import { useEffect, useState } from 'react';
import { ref, onValue } from 'firebase/database';
import { database } from '@/lib/firebase';
import PiStatus from '@/components/PiStatus';
import ControlPanel from '@/components/ControlPanel';

export default function Home() {
  const [piData, setPiData] = useState<any>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Listen to Pi status changes
    const statusRef = ref(database, 'pi/status');
    const unsubscribe = onValue(statusRef, (snapshot) => {
      const data = snapshot.val();
      setPiData(data);
      setIsConnected(data?.online || false);
    });

    return () => unsubscribe();
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Raspberry Pi Monitor</h1>
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-gray-300">{isConnected ? 'Connected' : 'Disconnected'}</span>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <PiStatus data={piData} />
          <ControlPanel />
        </div>
      </div>
    </main>
  );
}
