import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { RISK_COLORS } from '../utils/formatters';

interface RiskTrendPoint {
    time: string;
    SAFE: number;
    LOW_RISK: number;
    MEDIUM_RISK: number;
    HIGH_RISK: number;
    CRITICAL: number;
}

interface RiskTrendChartProps {
    data: RiskTrendPoint[];
}

const RiskTrendChart: React.FC<RiskTrendChartProps> = ({ data }) => {
    if (!data || data.length === 0) {
        return (
            <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 h-full">
                <h3 className="font-semibold text-gray-800 mb-3">Risk Tier Trend</h3>
                <div className="flex items-center justify-center h-48 text-gray-400 text-sm">
                    No data available
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 h-full">
            <h3 className="font-semibold text-gray-800 mb-2">Risk Tier Trend</h3>
            <ResponsiveContainer width="100%" height={200}>
                <LineChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis
                        dataKey="time"
                        tick={{ fontSize: 10, fill: '#9ca3af' }}
                        tickLine={false}
                    />
                    <YAxis
                        tick={{ fontSize: 10, fill: '#9ca3af' }}
                        tickLine={false}
                        axisLine={false}
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#1e293b',
                            border: 'none',
                            borderRadius: '8px',
                            color: '#fff',
                            fontSize: '12px'
                        }}
                    />
                    <Legend
                        verticalAlign="top"
                        height={30}
                        formatter={(value) => <span className="text-xs text-gray-600">{value.replace('_', ' ')}</span>}
                    />
                    <Line type="monotone" dataKey="SAFE" stroke={RISK_COLORS.SAFE} strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="LOW_RISK" stroke={RISK_COLORS.LOW_RISK} strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="MEDIUM_RISK" stroke={RISK_COLORS.MEDIUM_RISK} strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="HIGH_RISK" stroke={RISK_COLORS.HIGH_RISK} strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="CRITICAL" stroke={RISK_COLORS.CRITICAL} strokeWidth={2} dot={false} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default RiskTrendChart;
