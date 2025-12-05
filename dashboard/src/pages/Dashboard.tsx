import React, { useEffect, useState, useCallback, useRef } from 'react';
import { Activity, Shield, ShieldAlert, BarChart3, Users, Zap } from 'lucide-react';
import Layout from '../components/Layout';
import StatCard from '../components/StatCard';
import LiveStreamTable from '../components/LiveStreamTable';
import ThreatPieChart from '../components/ThreatPieChart';
import ThreatTimeline from '../components/ThreatTimeline';
import LoadChart from '../components/LoadChart';
import FeatureImportanceChart from '../components/FeatureImportanceChart';
import RiskTrendChart from '../components/RiskTrendChart';
import QueryInspector from '../components/QueryInspector';
import { getMetrics, getStream } from '../utils/api';
import { LogEntry, createLiveStream, LiveStreamClient } from '../utils/websocket';

interface Metrics {
    total_queries: number;
    blocked_count: number;
    throttled_count: number;
    high_risk_count: number;
    avg_threat_score: number;
    active_clients: number;
    avg_latency: number;
    attack_rate: number;
    threat_distribution: {
        SAFE: number;
        LOW_RISK: number;
        MEDIUM_RISK: number;
        HIGH_RISK: number;
        CRITICAL: number;
    };
    feature_importance: Array<{ feature: string; impact: number; count: number }>;
    load_over_time: Array<{ time: string; total: number; allowed: number; blocked: number; throttled: number }>;
    risk_trend: Array<{ time: string; SAFE: number; LOW_RISK: number; MEDIUM_RISK: number; HIGH_RISK: number; CRITICAL: number }>;
    threat_scores_timeline: Array<{ time: string; score: number }>;
}

const Dashboard: React.FC = () => {
    const [metrics, setMetrics] = useState<Metrics | null>(null);
    const [logs, setLogs] = useState<LogEntry[]>([]);
    const [selectedLog, setSelectedLog] = useState<LogEntry | null>(null);
    const [selectedId, setSelectedId] = useState<string | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const streamClientRef = useRef<LiveStreamClient | null>(null);

    // Fetch initial data
    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                const [metricsData, streamData] = await Promise.all([
                    getMetrics(),
                    getStream()
                ]);
                setMetrics(metricsData);
                setLogs(streamData.reverse()); // Newest first
            } catch (error) {
                console.error('Failed to fetch initial data:', error);
            }
        };

        fetchInitialData();
    }, []);

    // Set up SSE streaming
    useEffect(() => {
        const handleNewLog = (log: LogEntry) => {
            setLogs(prev => [log, ...prev].slice(0, 100)); // Keep last 100

            // Update metrics incrementally
            setMetrics(prev => {
                if (!prev) return prev;

                const tier = log.scores?.risk_tier || 'SAFE';
                const decision = log.decision;

                return {
                    ...prev,
                    total_queries: prev.total_queries + 1,
                    blocked_count: prev.blocked_count + (decision === 'BLOCK' ? 1 : 0),
                    throttled_count: prev.throttled_count + (decision === 'THROTTLE' ? 1 : 0),
                    high_risk_count: prev.high_risk_count + (['HIGH_RISK', 'CRITICAL'].includes(tier) ? 1 : 0),
                    threat_distribution: {
                        ...prev.threat_distribution,
                        [tier]: (prev.threat_distribution[tier as keyof typeof prev.threat_distribution] || 0) + 1
                    },
                    threat_scores_timeline: [
                        ...prev.threat_scores_timeline,
                        { time: new Date().toLocaleTimeString('en-US', { hour12: false }), score: log.scores?.ensemble_score || 0 }
                    ].slice(-100)
                };
            });
        };

        const handleError = () => {
            setIsConnected(false);
        };

        streamClientRef.current = createLiveStream(handleNewLog, handleError);
        streamClientRef.current.connect();
        setIsConnected(true);

        return () => {
            streamClientRef.current?.disconnect();
        };
    }, []);

    // Periodic metrics refresh (every 10 seconds)
    useEffect(() => {
        const interval = setInterval(async () => {
            try {
                const metricsData = await getMetrics();
                setMetrics(metricsData);
            } catch (error) {
                console.error('Failed to refresh metrics:', error);
            }
        }, 10000);

        return () => clearInterval(interval);
    }, []);

    const handleSelectQuery = useCallback((log: LogEntry, id: string) => {
        setSelectedLog(log);
        setSelectedId(id);
    }, []);

    const handleCloseInspector = useCallback(() => {
        setSelectedLog(null);
        setSelectedId(null);
    }, []);

    return (
        <Layout>
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Security Dashboard</h1>
                    <p className="text-sm text-gray-500 mt-1">Real-time GraphQL threat monitoring</p>
                </div>
                <div className="flex items-center gap-2">
                    <span className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium ${isConnected ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
                        }`}>
                        <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`} />
                        {isConnected ? 'Live' : 'Disconnected'}
                    </span>
                </div>
            </div>

            {/* Stat Cards */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
                <StatCard
                    title="Total Queries"
                    value={metrics?.total_queries || 0}
                    icon={Activity}
                    iconColor="text-teal-500"
                />
                <StatCard
                    title="Blocked"
                    value={metrics?.blocked_count || 0}
                    icon={ShieldAlert}
                    iconColor="text-red-500"
                />
                <StatCard
                    title="High Risk"
                    value={metrics?.high_risk_count || 0}
                    icon={Shield}
                    iconColor="text-orange-500"
                />
                <StatCard
                    title="Avg Score"
                    value={metrics?.avg_threat_score?.toFixed(1) || '0'}
                    icon={BarChart3}
                    iconColor="text-blue-500"
                />
                <StatCard
                    title="Active Clients"
                    value={metrics?.active_clients || 0}
                    icon={Users}
                    iconColor="text-purple-500"
                />
            </div>

            {/* Main Content - 3 Column Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
                {/* Left Panel - Live Stream */}
                <div className="lg:col-span-4 h-[600px]">
                    <LiveStreamTable
                        logs={logs}
                        onSelectQuery={handleSelectQuery}
                        selectedId={selectedId}
                    />
                </div>

                {/* Center Panel - Charts */}
                <div className="lg:col-span-4 space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <ThreatPieChart data={metrics?.threat_distribution || { SAFE: 0, LOW_RISK: 0, MEDIUM_RISK: 0, HIGH_RISK: 0, CRITICAL: 0 }} />
                        <FeatureImportanceChart data={metrics?.feature_importance || []} />
                    </div>
                    <ThreatTimeline data={metrics?.threat_scores_timeline || []} />
                    <LoadChart data={metrics?.load_over_time || []} />
                </div>

                {/* Right Panel - Inspector + Risk Trend */}
                <div className="lg:col-span-4 space-y-4">
                    <div className="h-[380px]">
                        <QueryInspector
                            log={selectedLog}
                            logId={selectedId}
                            onClose={handleCloseInspector}
                        />
                    </div>
                    <RiskTrendChart data={metrics?.risk_trend || []} />
                </div>
            </div>
        </Layout>
    );
};

export default Dashboard;
