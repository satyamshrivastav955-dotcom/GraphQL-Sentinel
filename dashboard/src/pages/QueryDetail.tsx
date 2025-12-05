import React from 'react';
import Layout from '../components/Layout';

const QueryDetail: React.FC = () => {
    return (
        <Layout>
            <h1 className="text-2xl font-bold mb-6 text-slate-800">Query Detail</h1>
            <div className="bg-white p-6 rounded-lg shadow">
                <p className="text-slate-500">Select a query from the Live Stream to view details.</p>
                {/* In a real app, this would take an ID from URL params and fetch details */}
            </div>
        </Layout>
    );
};

export default QueryDetail;
