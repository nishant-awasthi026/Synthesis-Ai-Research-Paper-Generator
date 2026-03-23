import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ResearchWorkflow from './pages/ResearchWorkflow';
import PaperEditor from './pages/PaperEditor';
import InteractiveResearch from './pages/InteractiveResearch';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

function App() {
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

    return (
        <BrowserRouter>
            <Routes>
                {/* Public Routes */}
                <Route
                    path="/login"
                    element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" replace />}
                />
                <Route
                    path="/register"
                    element={!isAuthenticated ? <Register /> : <Navigate to="/dashboard" replace />}
                />

                {/* Protected Routes */}
                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/workflow/:paperId"
                    element={
                        <ProtectedRoute>
                            <ResearchWorkflow />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/paper/:paperId"
                    element={
                        <ProtectedRoute>
                            <PaperEditor />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/research-chat"
                    element={
                        <ProtectedRoute>
                            <InteractiveResearch />
                        </ProtectedRoute>
                    }
                />

                {/* Default Route */}
                <Route
                    path="/"
                    element={<Navigate to={isAuthenticated ? "/research-chat" : "/login"} replace />}
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;

