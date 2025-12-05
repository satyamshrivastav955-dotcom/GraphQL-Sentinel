import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { formatFeatureName } from '../utils/formatters';

interface FeatureImportance {
    feature: string;
    impact: number;
    count: number;
}

interface FeatureImportanceChartProps {
    data: FeatureImportance[];
}

const FeatureImportanceChart: React.FC<FeatureImportanceChartProps> = ({ data }) => {
    if (!data || data.length === 0) {
        return (
            <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 h-full">
                <h3 className="font-semibold text-gray-800 mb-3">Top Attack Features</h3>
                <div className="flex items-center justify-center h-48 text-gray-400 text-sm">
                    No data available
                </div>
            </div>
        );
    }

    // Take top 6 features
    const chartData = data.slice(0, 6).map(item => ({
        ...item,
        name: formatFeatureName(item.feature),
        impact: Math.round(item.impact * 10) / 10
    }));

    const maxImpact = Math.max(...chartData.map(d => d.impact));

    const getBarColor = (impact: number) => {
        const ratio = impact / maxImpact;
        if (ratio > 0.7) return '#e74c3c';
        if (ratio > 0.4) return '#e67e22';
        return '#f1c40f';
    };

    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 h-full">
            <h3 className="font-semibold text-gray-800 mb-2">Top Attack Features</h3>
            <ResponsiveContainer width="100%" height={200}>
                <BarChart
                    data={chartData}
                    layout="vertical"
                    margin={{ top: 5, right: 20, left: 80, bottom: 5 }}
                >
                    <XAxis
                        type="number"
                        tick={{ fontSize: 10, fill: '#9ca3af' }}
                        tickLine={false}
                        axisLine={false}
                    />
                    <YAxis
                        type="category"
                        dataKey="name"
                        tick={{ fontSize: 11, fill: '#4b5563' }}
                        tickLine={false}
                        axisLine={false}
                        width={75}
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#1e293b',
                            border: 'none',
                            borderRadius: '8px',
                            color: '#fff',
                            fontSize: '12px'
                        }}
                        formatter={(value: number, name: string, props: any) => [
                            `Impact: ${value} (${props.payload.count} occurrences)`,
                            ''
                        ]}
                    />
                    <Bar dataKey="impact" radius={[0, 4, 4, 0]}>
                        {chartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={getBarColor(entry.impact)} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default FeatureImportanceChart;
