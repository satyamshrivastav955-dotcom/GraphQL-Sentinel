/**
 * Formatting utilities for the dashboard
 */

// Risk tier colors matching the design spec
export const RISK_COLORS = {
    SAFE: '#2ecc71',
    LOW_RISK: '#f1c40f',
    MEDIUM_RISK: '#e67e22',
    HIGH_RISK: '#e74c3c',
    CRITICAL: '#8e0000',
} as const;

// Corporate palette
export const THEME_COLORS = {
    navy: '#1e3a5f',
    navyLight: '#2c5282',
    teal: '#0d9488',
    tealLight: '#14b8a6',
    white: '#ffffff',
    gray50: '#f8fafc',
    gray100: '#f1f5f9',
    gray200: '#e2e8f0',
    gray500: '#64748b',
    gray700: '#334155',
    gray900: '#0f172a',
} as const;

export type RiskTier = keyof typeof RISK_COLORS;

export const getRiskColor = (tier: string): string => {
    const normalizedTier = tier?.toUpperCase().replace(' ', '_') as RiskTier;
    return RISK_COLORS[normalizedTier] || RISK_COLORS.SAFE;
};

export const getRiskBgClass = (tier: string): string => {
    const tierMap: Record<string, string> = {
        SAFE: 'bg-emerald-100 text-emerald-800',
        LOW_RISK: 'bg-yellow-100 text-yellow-800',
        MEDIUM_RISK: 'bg-orange-100 text-orange-800',
        HIGH_RISK: 'bg-red-100 text-red-800',
        CRITICAL: 'bg-red-200 text-red-900',
    };
    return tierMap[tier] || tierMap.SAFE;
};

export const getDecisionColor = (decision: string): string => {
    const colors: Record<string, string> = {
        ALLOW: 'text-emerald-600',
        THROTTLE: 'text-yellow-600',
        BLOCK: 'text-red-600',
    };
    return colors[decision] || colors.ALLOW;
};

export const getDecisionBorderClass = (decision: string): string => {
    const borders: Record<string, string> = {
        ALLOW: 'border-l-emerald-500',
        THROTTLE: 'border-l-yellow-500',
        BLOCK: 'border-l-red-500',
    };
    return borders[decision] || borders.ALLOW;
};

export const formatTimestamp = (timestamp: string): string => {
    try {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        });
    } catch {
        return timestamp;
    }
};

export const formatScore = (score: number): string => {
    if (score === undefined || score === null) return '0';
    return score.toFixed(1);
};

export const formatPercentage = (value: number): string => {
    return `${(value * 100).toFixed(1)}%`;
};

export const truncateQuery = (query: string, maxLength: number = 80): string => {
    if (!query) return '';
    const cleaned = query.replace(/\s+/g, ' ').trim();
    if (cleaned.length <= maxLength) return cleaned;
    return cleaned.substring(0, maxLength) + '...';
};

export const formatFeatureName = (name: string): string => {
    return name
        .replace(/_/g, ' ')
        .replace(/\b\w/g, (l) => l.toUpperCase());
};

export const formatNumber = (num: number): string => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
};
