interface PiStatusProps {
  data: any;
}

export default function PiStatus({ data }: PiStatusProps) {
  return (
    <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
      <h2 className="text-2xl font-semibold mb-4">System Status</h2>
      
      {data ? (
        <div className="space-y-4">
          <div className="flex justify-between items-center border-b border-gray-700 pb-2">
            <span className="text-gray-400">CPU Usage</span>
            <span className="text-lg font-semibold">{data.cpu || '0'}%</span>
          </div>
          
          <div className="flex justify-between items-center border-b border-gray-700 pb-2">
            <span className="text-gray-400">Memory Usage</span>
            <span className="text-lg font-semibold">{data.memory || '0'}%</span>
          </div>
          
          <div className="flex justify-between items-center border-b border-gray-700 pb-2">
            <span className="text-gray-400">Temperature</span>
            <span className="text-lg font-semibold">{data.temperature || '0'}°C</span>
          </div>
          
          <div className="flex justify-between items-center border-b border-gray-700 pb-2">
            <span className="text-gray-400">Disk Usage</span>
            <span className="text-lg font-semibold">{data.disk || '0'}%</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-gray-400">Last Updated</span>
            <span className="text-sm text-gray-500">
              {data.timestamp ? new Date(data.timestamp).toLocaleTimeString() : 'Never'}
            </span>
          </div>
        </div>
      ) : (
        <div className="text-gray-500 text-center py-8">
          Waiting for data...
        </div>
      )}
    </div>
  );
}
