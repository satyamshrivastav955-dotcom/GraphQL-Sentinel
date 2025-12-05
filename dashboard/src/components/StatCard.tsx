import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
    title: string;
    value: string | number;
    icon: LucideIcon;
    iconColor?: string;
    trend?: {
        value: number;
        isPositive: boolean;
    };
}

const StatCard: React.FC<StatCardProps> = ({
    title,
    value,
    icon: Icon,
    iconColor = 'text-teal-500',
    trend
}) => {
    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-5 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">{title}</p>
                    <p className="mt-1 text-2xl font-bold text-gray-900">{value}</p>
                    {trend && (
                        <p className={`text-xs mt-1 ${trend.isPositive ? 'text-emerald-600' : 'text-red-600'}`}>
                            {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}% from last hour
                        </p>
                    )}
                </div>
                <div className={`p-3 rounded-full bg-gray-50 ${iconColor}`}>
                    <Icon className="w-6 h-6" />
                </div>
            </div>
        </div>
    );
};

export default StatCard;
