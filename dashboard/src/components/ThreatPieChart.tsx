import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { RISK_COLORS } from '../utils/formatters';

interface ThreatDistribution {
    SAFE: number;
    LOW_RISK: number;
    MEDIUM_RISK: number;
    HIGH_RISK: number;
    CRITICAL: number;
}

interface ThreatPieChartProps {
    data: ThreatDistribution;
}

const ThreatPieChart: React.FC<ThreatPieChartProps> = ({ data }) => {
    const chartData = [
        { name: 'Safe', value: data.SAFE, color: RISK_COLORS.SAFE },
        { name: 'Low', value: data.LOW_RISK, color: RISK_COLORS.LOW_RISK },
        { name: 'Medium', value: data.MEDIUM_RISK, color: RISK_COLORS.MEDIUM_RISK },
        { name: 'High', value: data.HIGH_RISK, color: RISK_COLORS.HIGH_RISK },
        { name: 'Critical', value: data.CRITICAL, color: RISK_COLORS.CRITICAL },
    ].filter(item => item.value > 0);

    const total = chartData.reduce((sum, item) => sum + item.value, 0);

    if (total === 0) {
        return (
            <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 h-full">
                <h3 className="font-semibold text-gray-800 mb-3">Threat Distribution</h3>
                <div className="flex items-center justify-center h-48 text-gray-400 text-sm">
                    No data available
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-4 h-full">
            <h3 className="font-semibold text-gray-800 mb-2">Threat Distribution</h3>
            <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                    <Pie
                        data={chartData}
                        cx="50%"
                        cy="50%"
                        innerRadius={50}
                        outerRadius={75}
                        paddingAngle={2}
                        dataKey="value"
                    >
                        {chartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                    </Pie>
                    <Tooltip
                        formatter={(value: number) => [`${value} (${((value / total) * 100).toFixed(1)}%)`, 'Count']}
                    />
                    <Legend
                        verticalAlign="bottom"
                        height={36}
                        formatter={(value) => <span className="text-xs text-gray-600">{value}</span>}
                    />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ThreatPieChart;
