export type LogEntry = {
    id: string;  // Added unique ID
    timestamp: string;
    client_id: string;
    ip: string;
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
    decision: 'ALLOW' | 'BLOCK' | 'THROTTLE';
    explanations: Array<{ feature: string; score: number; description: string }>;
    latency_ms: number;
};

export type SSECallback = (log: LogEntry) => void;

export class LiveStreamClient {
    private eventSource: EventSource | null = null;
    private url: string;
    private onMessage: SSECallback;
    private onError?: (error: Event) => void;
    private reconnectTimeout: number = 3000;
    private reconnectTimer: NodeJS.Timeout | null = null;

    constructor(url: string, onMessage: SSECallback, onError?: (error: Event) => void) {
        this.url = url;
        this.onMessage = onMessage;
        this.onError = onError;
    }

    connect(): void {
        if (this.eventSource) {
            this.disconnect();
        }

        this.eventSource = new EventSource(this.url);

        this.eventSource.onmessage = (event) => {
            try {
                const log = JSON.parse(event.data) as LogEntry;
                this.onMessage(log);
            } catch (e) {
                console.error('Failed to parse SSE message:', e);
            }
        };

        this.eventSource.onerror = (error) => {
            console.error('SSE connection error:', error);
            this.onError?.(error);

            // Attempt to reconnect
            this.scheduleReconnect();
        };
    }

    private scheduleReconnect(): void {
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
        }

        this.reconnectTimer = setTimeout(() => {
            console.log('Attempting SSE reconnect...');
            this.connect();
        }, this.reconnectTimeout);
    }

    disconnect(): void {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
            this.reconnectTimer = null;
        }
    }

    isConnected(): boolean {
        return this.eventSource?.readyState === EventSource.OPEN;
    }
}

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const createLiveStream = (
    onMessage: SSECallback,
    onError?: (error: Event) => void
): LiveStreamClient => {
    return new LiveStreamClient(`${API_BASE_URL}/api/live`, onMessage, onError);
};
