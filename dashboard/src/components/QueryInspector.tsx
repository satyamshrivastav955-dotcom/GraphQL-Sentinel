import React, { useEffect, useState } from 'react';
import { X, Code, FileJson, BarChart3, Activity } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts';
import { getQueryDetails, getExplanation } from '../utils/api';
import { LogEntry } from '../utils/websocket';
import { formatTimestamp, getRiskBgClass, formatFeatureName, RISK_COLORS } from '../utils/formatters';

interface QueryInspectorProps {
    log: LogEntry | null;
    logId: string | null;
    onClose: () => void;
}

interface QueryDetails {
    query: string;
    features: Record<string, number>;
    scores: {
        ensemble_score: number;
        risk_tier: string;
        autoencoder?: number;
        random_forest?: number;
        lstm?: number;
        gnn?: number;
    };
    explanations: Array<{ feature: string; score: number; description: string }>;
    client_timeline: Array<{ time: string; score: number }>;
}

interface ExplanationData {
    model_scores: {
        autoencoder: number;
        random_forest: number;
        lstm: number;
        gnn: number;
    };
    contributions: Array<{ feature: string; contribution: number; description: string }>;
}

const QueryInspector: React.FC<QueryInspectorProps> = ({ log, logId, onClose }) => {
    const [details, setDetails] = useState<QueryDetails | null>(null);
    const [explanation, setExplanation] = useState<ExplanationData | null>(null);
    const [activeTab, setActiveTab] = useState<'query' | 'features' | 'scores' | 'explain'>('query');

    useEffect(() => {
        if (logId) {
            // Fetch additional details
            getQueryDetails(logId)
                .then(data => setDetails(data))
                .catch(console.error);

            getExplanation(logId)
                .then(data => setExplanation(data))
                .catch(console.error);
        }
    }, [logId]);

    if (!log) {
        return (
            <div className="bg-white rounded-lg shadow-sm border border-gray-100 h-full flex items-center justify-center">
                <div className="text-center text-gray-400">
                    <FileJson className="w-12 h-12 mx-auto mb-2 opacity-50" />
                    <p>Select a query to inspect</p>
                </div>
            </div>
        );
    }

    const modelScores = explanation?.model_scores || log.scores;
    const contributions = explanation?.contributions || [];

    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 h-full flex flex-col">
            {/* Header */}
            <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-gray-800">Query Inspector</h3>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${getRiskBgClass(log.scores?.risk_tier || 'SAFE')}`}>
                        {log.scores?.risk_tier || 'SAFE'}
                    </span>
                </div>
                <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
                    <X className="w-5 h-5" />
                </button>
            </div>

            {/* Tabs */}
            <div className="flex border-b border-gray-100">
                {[
                    { id: 'query', label: 'Query', icon: Code },
                    { id: 'features', label: 'Features', icon: FileJson },
                    { id: 'scores', label: 'Scores', icon: BarChart3 },
                    { id: 'explain', label: 'Explain', icon: Activity },
                ].map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id as any)}
                        className={`flex items-center gap-1.5 px-4 py-2 text-sm font-medium transition-colors ${activeTab === tab.id
                            ? 'text-teal-600 border-b-2 border-teal-500'
                            : 'text-gray-500 hover:text-gray-700'
                            }`}
                    >
                        <tab.icon className="w-4 h-4" />
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4">
                {activeTab === 'query' && (
                    <div>
                        <div className="mb-4">
                            <div className="flex items-center justify-between text-xs text-gray-400 mb-2">
                                <span>{formatTimestamp(log.timestamp)}</span>
                                <span>{log.client_id} • {log.ip}</span>
                            </div>
                        </div>
                        <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg text-sm overflow-x-auto font-mono">
                            {log.query}
                        </pre>
                    </div>
                )}

                {activeTab === 'features' && (
                    <div className="space-y-2">
                        <h4 className="text-sm font-medium text-gray-600 mb-3">Extracted Features</h4>
                        <div className="grid grid-cols-2 gap-2">
                            {Object.entries(log.features || {}).map(([key, value]) => (
                                <div key={key} className="bg-gray-50 rounded p-2">
                                    <div className="text-xs text-gray-500">{formatFeatureName(key)}</div>
                                    <div className="text-sm font-mono font-semibold text-gray-800">{value}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {activeTab === 'scores' && (
                    <div className="space-y-4">
                        {/* Ensemble Score */}
                        <div className="bg-gray-50 rounded-lg p-4">
                            <div className="text-sm text-gray-500 mb-1">Final Ensemble Score</div>
                            <div className="text-3xl font-bold text-gray-900">
                                {log.scores?.ensemble_score?.toFixed(1) || 0}
                                <span className="text-lg font-normal text-gray-400">/100</span>
                            </div>
                        </div>

                        {/* Model Breakdown */}
                        <div className="space-y-3">
                            <h4 className="text-sm font-medium text-gray-600">Model Breakdown</h4>
                            {[
                                { name: 'Autoencoder', key: 'autoencoder', color: 'bg-purple-500' },
                                { name: 'Random Forest', key: 'random_forest', color: 'bg-blue-500' },
                                { name: 'LSTM', key: 'lstm', color: 'bg-green-500' },
                                { name: 'GNN', key: 'gnn', color: 'bg-orange-500' },
                            ].map(model => {
                                const score = (modelScores as any)?.[model.key] || 0;
                                return (
                                    <div key={model.key} className="flex items-center gap-3">
                                        <div className="w-24 text-xs text-gray-600">{model.name}</div>
                                        <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                                            <div
                                                className={`h-full ${model.color} transition-all duration-500`}
                                                style={{ width: `${Math.min(score * 100, 100)}%` }}
                                            />
                                        </div>
                                        <div className="w-12 text-xs font-mono text-right">{score.toFixed(2)}</div>
                                    </div>
                                );
                            })}
                        </div>

                        {/* Client Timeline */}
                        {details?.client_timeline && details.client_timeline.length > 1 && (
                            <div>
                                <h4 className="text-sm font-medium text-gray-600 mb-2">Client History</h4>
                                <div className="h-24">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <LineChart data={details.client_timeline}>
                                            <XAxis dataKey="time" tick={{ fontSize: 9 }} />
                                            <YAxis domain={[0, 100]} tick={{ fontSize: 9 }} />
                                            <Tooltip />
                                            <Line type="monotone" dataKey="score" stroke="#0d9488" strokeWidth={2} dot={{ r: 3 }} />
                                        </LineChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {activeTab === 'explain' && (
                    <div className="space-y-4">
                        <h4 className="text-sm font-medium text-gray-600">Top Contributing Features</h4>
                        {contributions.length === 0 ? (
                            <div className="text-center text-gray-400 py-4">No significant features detected</div>
                        ) : (
                            <div className="space-y-2">
                                {contributions.map((contrib, idx) => (
                                    <div key={idx} className="flex items-center gap-3">
                                        <div className="w-32 text-xs text-gray-600 truncate" title={contrib.feature}>
                                            {formatFeatureName(contrib.feature)}
                                        </div>
                                        <div className="flex-1 h-5 bg-gray-100 rounded overflow-hidden relative">
                                            <div
                                                className="h-full bg-gradient-to-r from-red-400 to-red-600 transition-all duration-500"
                                                style={{ width: `${Math.min(contrib.contribution * 4, 100)}%` }}
                                            />
                                            <span className="absolute right-2 top-0.5 text-xs font-mono text-gray-700">
                                                +{contrib.contribution.toFixed(1)}
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Original explanations from backend */}
                        {log.explanations && log.explanations.length > 0 && (
                            <div className="mt-4 pt-4 border-t border-gray-100">
                                <h4 className="text-sm font-medium text-gray-600 mb-2">Explanations</h4>
                                {log.explanations.map((exp, idx) => (
                                    <div key={idx} className="flex items-center gap-2 py-1">
                                        <span className="px-2 py-0.5 bg-pink-50 text-pink-700 text-xs rounded-full">
                                            {exp.feature}
                                        </span>
                                        <span className="text-xs text-gray-500">{exp.description}</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default QueryInspector;
