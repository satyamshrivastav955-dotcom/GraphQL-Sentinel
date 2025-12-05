import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

interface TimelinePoint {
    time: string;
    score: number;
}

interface ThreatTimelineProps {
    data: TimelinePoint[];
}

const ThreatTimeline: React.FC<ThreatTimelineProps> = ({ data }) => {
    if (!data || data.length === 0) {
        return (
            <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 h-full">
                <h3 className="font-semibold text-gray-800 mb-3">Threat Score Timeline</h3>
                <div className="flex items-center justify-center h-48 text-gray-400 text-sm">
                    No data available
                </div>
            </div>
        );
    }

    // Get last 30 points for display
    const displayData = data.slice(-30);

    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 h-full">
            <h3 className="font-semibold text-gray-800 mb-2">Threat Score Timeline</h3>
            <ResponsiveContainer width="100%" height={200}>
                <LineChart data={displayData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis
                        dataKey="time"
                        tick={{ fontSize: 10, fill: '#9ca3af' }}
                        tickLine={false}
                        interval="preserveStartEnd"
                    />
                    <YAxis
                        domain={[0, 100]}
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
                        formatter={(value: number) => [value.toFixed(1), 'Score']}
                    />
                    <ReferenceLine y={70} stroke="#e74c3c" strokeDasharray="5 5" label={{ value: 'High Risk', fill: '#e74c3c', fontSize: 10 }} />
                    <ReferenceLine y={40} stroke="#f1c40f" strokeDasharray="5 5" />
                    <Line
                        type="monotone"
                        dataKey="score"
                        stroke="#0d9488"
                        strokeWidth={2}
                        dot={false}
                        activeDot={{ r: 4, stroke: '#0d9488', strokeWidth: 2 }}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ThreatTimeline;
