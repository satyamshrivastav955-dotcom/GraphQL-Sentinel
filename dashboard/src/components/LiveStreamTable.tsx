import React from 'react';
import { ShieldAlert, CheckCircle, AlertTriangle } from 'lucide-react';
import { LogEntry } from '../utils/websocket';
import { formatTimestamp, truncateQuery, getRiskBgClass, getDecisionBorderClass } from '../utils/formatters';

interface LiveStreamTableProps {
    logs: LogEntry[];
    onSelectQuery: (log: LogEntry, id: string) => void;
    selectedId: string | null;
}

const LiveStreamTable: React.FC<LiveStreamTableProps> = ({ logs, onSelectQuery, selectedId }) => {
    const getDecisionIcon = (decision: string) => {
        switch (decision) {
            case 'BLOCK':
                return <ShieldAlert className="w-4 h-4 text-red-500" />;
            case 'THROTTLE':
                return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
            default:
                return <CheckCircle className="w-4 h-4 text-emerald-500" />;
        }
    };

    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 h-full flex flex-col">
            <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
                <h3 className="font-semibold text-gray-800">Real-time Threat Stream</h3>
                <span className="text-xs text-gray-400">{logs.length} queries</span>
            </div>

            <div className="flex-1 overflow-y-auto">
                {logs.length === 0 ? (
                    <div className="flex items-center justify-center h-32 text-gray-400 text-sm">
                        Waiting for queries...
                    </div>
                ) : (
                    <div className="divide-y divide-gray-50">
                        {logs.map((log, idx) => {
                            return (
                                <div
                                    key={log.id || `${log.timestamp}-${idx}`}
                                    onClick={() => onSelectQuery(log, log.id)}
                                    className={`px-4 py-3 cursor-pointer border-l-4 transition-colors ${getDecisionBorderClass(log.decision)} ${selectedId === log.id ? 'bg-blue-50' : 'hover:bg-gray-50'
                                        }`}
                                >
                                    <div className="flex items-center justify-between mb-1">
                                        <div className="flex items-center gap-2">
                                            {getDecisionIcon(log.decision)}
                                            <span className="font-medium text-sm text-gray-700">{log.decision}</span>
                                            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${getRiskBgClass(log.scores?.risk_tier || 'SAFE')}`}>
                                                {log.scores?.risk_tier || 'SAFE'}
                                            </span>
                                        </div>
                                        <div className="text-right">
                                            <span className="text-sm font-mono font-bold text-gray-800">
                                                {log.scores?.ensemble_score?.toFixed(1) || '0'}
                                            </span>
                                            <span className="text-xs text-gray-400 ml-1">score</span>
                                        </div>
                                    </div>

                                    <div className="font-mono text-xs text-gray-600 bg-gray-50 rounded px-2 py-1 mb-2 truncate">
                                        {truncateQuery(log.query, 60)}
                                    </div>

                                    <div className="flex items-center justify-between text-xs text-gray-400">
                                        <span>{formatTimestamp(log.timestamp)}</span>
                                        <span>{log.client_id} • {log.ip}</span>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
};

export default LiveStreamTable;
