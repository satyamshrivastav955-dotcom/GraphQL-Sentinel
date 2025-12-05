import React, { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { getStream } from '../utils/api';
import { AlertTriangle, CheckCircle, ShieldAlert } from 'lucide-react';

const LiveStream: React.FC = () => {
    const [logs, setLogs] = useState<any[]>([]);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const data = await getStream();
                setLogs(data.reverse()); // Show newest first
            } catch (error) {
                console.error("Failed to fetch stream", error);
            }
        };

        fetchLogs();
        const interval = setInterval(fetchLogs, 2000); // Poll every 2s
        return () => clearInterval(interval);
    }, []);

    return (
        <Layout>
            <h1 className="text-2xl font-bold mb-6 text-slate-800">Live Query Stream</h1>
            <div className="space-y-4">
                {logs.map((log, index) => (
                    <div key={index} className={`bg-white p-4 rounded-lg shadow border-l-4 ${log.decision === 'BLOCK' ? 'border-red-500' :
                        log.decision === 'THROTTLE' ? 'border-yellow-500' : 'border-green-500'
                        }`}>
                        <div className="flex justify-between items-start">
                            <div className="flex items-center space-x-2">
                                {log.decision === 'BLOCK' && <ShieldAlert className="text-red-500" />}
                                {log.decision === 'THROTTLE' && <AlertTriangle className="text-yellow-500" />}
                                {log.decision === 'ALLOW' && <CheckCircle className="text-green-500" />}
                                <span className="font-bold text-slate-700">{log.decision}</span>
                                <span className="text-sm text-slate-500">| {new Date(log.timestamp).toLocaleTimeString()}</span>
                            </div>
                            <div className="text-right">
                                <div className="text-sm text-slate-500">
                                    Score: <span className="font-mono font-bold">{log.scores?.ensemble_score?.toFixed(1)}</span>
                                </div>
                                {/* Risk Tier Badge */}
                                <span className={`inline-block mt-1 px-2 py-0.5 text-xs font-bold rounded ${log.scores?.risk_tier === 'CRITICAL' ? 'bg-red-100 text-red-700' :
                                        log.scores?.risk_tier === 'HIGH_RISK' ? 'bg-orange-100 text-orange-700' :
                                            log.scores?.risk_tier === 'MEDIUM_RISK' ? 'bg-yellow-100 text-yellow-700' :
                                                log.scores?.risk_tier === 'LOW_RISK' ? 'bg-blue-100 text-blue-700' :
                                                    'bg-green-100 text-green-700'
                                    }`}>
                                    {log.scores?.risk_tier || 'SAFE'}
                                </span>
                            </div>
                        </div>
                        <div className="mt-2 font-mono text-sm bg-slate-50 p-2 rounded text-slate-600 truncate">
                            {log.query}
                        </div>
                        {/* Model Scores */}
                        <div className="mt-2 grid grid-cols-4 gap-2 text-xs">
                            <div className="bg-purple-50 p-1 rounded text-center">
                                <div className="text-purple-600 font-semibold">AE</div>
                                <div className="font-mono">{(log.scores?.autoencoder || 0).toFixed(2)}</div>
                            </div>
                            <div className="bg-blue-50 p-1 rounded text-center">
                                <div className="text-blue-600 font-semibold">RF</div>
                                <div className="font-mono">{(log.scores?.random_forest || 0).toFixed(2)}</div>
                            </div>
                            <div className="bg-green-50 p-1 rounded text-center">
                                <div className="text-green-600 font-semibold">LSTM</div>
                                <div className="font-mono">{(log.scores?.lstm || 0).toFixed(2)}</div>
                            </div>
                            <div className="bg-orange-50 p-1 rounded text-center">
                                <div className="text-orange-600 font-semibold">GNN</div>
                                <div className="font-mono">{(log.scores?.gnn || 0).toFixed(2)}</div>
                            </div>
                        </div>
                        <div className="mt-2 flex space-x-4 text-xs text-slate-400">
                            <span>Client: {log.client_id}</span>
                            <span>IP: {log.ip}</span>
                            <span>Latency: {log.latency_ms?.toFixed(2)}ms</span>
                        </div>
                        {log.explanations && log.explanations.length > 0 && (
                            <div className="mt-2 pt-2 border-t border-slate-100">
                                <span className="text-xs font-semibold text-slate-500">Top Factors:</span>
                                <div className="flex flex-wrap gap-2 mt-1">
                                    {log.explanations.map((exp: any, i: number) => (
                                        <span key={i} className="px-2 py-1 bg-pink-50 text-pink-700 text-xs rounded-full">
                                            {exp.feature} ({exp.score})
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                ))}
                {logs.length === 0 && (
                    <div className="text-center text-slate-400 py-10">
                        Waiting for queries...
                    </div>
                )}
            </div>
        </Layout>
    );
};

export default LiveStream;
