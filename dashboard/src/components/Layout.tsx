import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, Activity, Play, BarChart2 } from 'lucide-react';

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <div className="min-h-screen bg-gray-50 flex">
            {/* Sidebar */}
            <aside className="w-64 bg-slate-900 text-white flex flex-col fixed h-full">
                <div className="p-5 flex items-center space-x-3 border-b border-slate-800">
                    <div className="p-2 bg-teal-500 rounded-lg">
                        <Shield className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <span className="text-lg font-bold block">GraphQL</span>
                        <span className="text-xs text-slate-400">Sentinel</span>
                    </div>
                </div>

                <nav className="flex-1 p-4 space-y-1">
                    <Link
                        to="/"
                        className="flex items-center space-x-3 px-4 py-3 rounded-lg bg-slate-800 text-white transition"
                    >
                        <BarChart2 className="w-5 h-5 text-teal-400" />
                        <span className="font-medium">Dashboard</span>
                    </Link>
                    <Link
                        to="/playground"
                        className="flex items-center space-x-3 px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition"
                    >
                        <Play className="w-5 h-5" />
                        <span>Playground</span>
                    </Link>
                </nav>

                <div className="p-4 border-t border-slate-800">
                    <div className="flex items-center gap-2 text-xs text-slate-500">
                        <Activity className="w-3 h-3" />
                        <span>v1.0.0</span>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 ml-64 p-6 overflow-auto min-h-screen">
                {children}
            </main>
        </div>
    );
};

export default Layout;
