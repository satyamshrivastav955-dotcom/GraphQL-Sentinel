import React, { useState } from 'react';
import Layout from '../components/Layout';
import axios from 'axios';
import { Play, Shield, AlertTriangle, CheckCircle } from 'lucide-react';
import { API_BASE_URL } from '../utils/api';

const Playground: React.FC = () => {
    const [query, setQuery] = useState<string>('query { user(id: "123") { name } }');
    const [response, setResponse] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const handleRun = async () => {
        setLoading(true);
        try {
            const res = await axios.post(`${API_BASE_URL}/graphql-proxy`, {
                query: query
            });
            setResponse(res.data);
        } catch (error: any) {
            setResponse(error.response?.data || { error: "Request failed" });
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <h1 className="text-2xl font-bold mb-6 text-slate-800">Query Playground</h1>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-12rem)]">
                {/* Input Section */}
                <div className="flex flex-col bg-white rounded-lg shadow overflow-hidden">
                    <div className="bg-slate-100 px-4 py-2 border-b border-slate-200 flex justify-between items-center">
                        <span className="text-sm font-medium text-slate-600">GraphQL Query</span>
                        <button
                            onClick={handleRun}
                            disabled={loading}
                            className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm transition-colors disabled:opacity-50"
                        >
                            <Play size={14} />
                            <span>{loading ? 'Running...' : 'Run Query'}</span>
                        </button>
                    </div>
                    <textarea
                        className="flex-1 p-4 font-mono text-sm resize-none focus:outline-none"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        spellCheck={false}
                    />
                </div>

                {/* Output Section */}
                <div className="flex flex-col bg-white rounded-lg shadow overflow-hidden">
                    <div className="bg-slate-100 px-4 py-2 border-b border-slate-200">
                        <span className="text-sm font-medium text-slate-600">Response & Security Analysis</span>
                    </div>
                    <div className="flex-1 p-4 overflow-auto bg-slate-50">
                        {response ? (
                            <div className="space-y-6">
                                {/* Security Decision */}
                                {response.extensions?.security && (
                                    <div className={`p-4 rounded-lg border ${response.extensions.security.decision === 'BLOCK' ? 'bg-red-50 border-red-200' :
                                        response.extensions.security.decision === 'THROTTLE' ? 'bg-yellow-50 border-yellow-200' :
                                            'bg-green-50 border-green-200'
                                        }`}>
                                        <div className="flex items-center justify-between mb-3">
                                            <div className="flex items-center space-x-2">
                                                {response.extensions.security.decision === 'BLOCK' ? <Shield className="text-red-500" /> :
                                                    response.extensions.security.decision === 'THROTTLE' ? <AlertTriangle className="text-yellow-500" /> :
                                                        <CheckCircle className="text-green-500" />}
                                                <span className="font-bold text-lg">
                                                    {response.extensions.security.decision}
                                                </span>
                                            </div>
                                            {/* Risk Tier Badge */}
                                            <span className={`px-3 py-1 text-sm font-bold rounded-full ${response.extensions.security.risk_tier === 'CRITICAL' ? 'bg-red-200 text-red-800' :
                                                response.extensions.security.risk_tier === 'HIGH_RISK' ? 'bg-orange-200 text-orange-800' :
                                                    response.extensions.security.risk_tier === 'MEDIUM_RISK' ? 'bg-yellow-200 text-yellow-800' :
                                                        response.extensions.security.risk_tier === 'LOW_RISK' ? 'bg-blue-200 text-blue-800' :
                                                            'bg-green-200 text-green-800'
                                                }`}>
                                                {response.extensions.security.risk_tier || 'SAFE'}
                                            </span>
                                        </div>

                                        {/* Score Overview */}
                                        <div className="grid grid-cols-2 gap-4 text-sm mb-3">
                                            <div>
                                                <span className="text-slate-500">Final Score:</span>
                                                <span className="font-mono font-bold ml-2 text-xl">
                                                    {response.extensions.security.score?.toFixed(1) || '0.0'}
                                                </span>
                                                <span className="text-slate-400">/100</span>
                                            </div>
                                            <div>
                                                <span className="text-slate-500">Latency:</span>
                                                <span className="font-mono font-bold ml-2">
                                                    {response.extensions.security.latency_ms?.toFixed(2) || '0.00'}ms
                                                </span>
                                            </div>
                                        </div>

                                        {/* Model Scores */}
                                        {response.extensions.security.model_scores && (
                                            <div className="border-t pt-3">
                                                <h5 className="text-xs font-bold text-slate-400 uppercase mb-2">Model Scores</h5>
                                                <div className="grid grid-cols-4 gap-2 text-xs">
                                                    <div className="bg-white p-2 rounded text-center shadow-sm">
                                                        <div className="text-purple-600 font-semibold">Autoencoder</div>
                                                        <div className="font-mono text-lg">{(response.extensions.security.model_scores.autoencoder || 0).toFixed(3)}</div>
                                                    </div>
                                                    <div className="bg-white p-2 rounded text-center shadow-sm">
                                                        <div className="text-blue-600 font-semibold">Random Forest</div>
                                                        <div className="font-mono text-lg">{(response.extensions.security.model_scores.random_forest || 0).toFixed(3)}</div>
                                                    </div>
                                                    <div className="bg-white p-2 rounded text-center shadow-sm">
                                                        <div className="text-green-600 font-semibold">LSTM</div>
                                                        <div className="font-mono text-lg">{(response.extensions.security.model_scores.lstm || 0).toFixed(3)}</div>
                                                    </div>
                                                    <div className="bg-white p-2 rounded text-center shadow-sm">
                                                        <div className="text-orange-600 font-semibold">GNN</div>
                                                        <div className="font-mono text-lg">{(response.extensions.security.model_scores.gnn || 0).toFixed(3)}</div>
                                                    </div>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                )}

                                {/* Raw JSON Response */}
                                <div>
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">JSON Response</h4>
                                    <pre className="font-mono text-xs text-slate-700 whitespace-pre-wrap break-all">
                                        {JSON.stringify(response, null, 2)}
                                    </pre>
                                </div>
                            </div>
                        ) : (
                            <div className="h-full flex items-center justify-center text-slate-400 text-sm">
                                Run a query to see results
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default Playground;
