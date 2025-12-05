import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

interface LoadDataPoint {
    time: string;
    total: number;
    allowed: number;
    blocked: number;
    throttled: number;
}

interface LoadChartProps {
    data: LoadDataPoint[];
}

const LoadChart: React.FC<LoadChartProps> = ({ data }) => {
    if (!data || data.length === 0) {
        return (
            <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 h-full">
                <h3 className="font-semibold text-gray-800 mb-3">Query Load Over Time</h3>
                <div className="flex items-center justify-center h-48 text-gray-400 text-sm">
                    No data available
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 h-full">
            <h3 className="font-semibold text-gray-800 mb-2">Query Load Over Time</h3>
            <ResponsiveContainer width="100%" height={200}>
                <BarChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
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
                        formatter={(value) => <span className="text-xs text-gray-600">{value}</span>}
                    />
                    <Bar dataKey="allowed" stackId="a" fill="#2ecc71" name="Allowed" />
                    <Bar dataKey="throttled" stackId="a" fill="#f1c40f" name="Throttled" />
                    <Bar dataKey="blocked" stackId="a" fill="#e74c3c" name="Blocked" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default LoadChart;
