import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../api/client';
import { useAuthStore } from '../store';

const Login = () => {
    const DEMO_EMAIL = 'demo@synthesis.ai';
    const DEMO_PASSWORD = 'demo123';
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();
    const setAuth = useAuthStore((state) => state.setAuth);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await authAPI.login({ email, password });
            const { access_token, user } = response.data;

            setAuth(user, access_token);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    const handleDemoLogin = async () => {
        setError('');
        setLoading(true);
        setEmail(DEMO_EMAIL);
        setPassword(DEMO_PASSWORD);

        try {
            // Try normal login first
            let response;
            try {
                response = await authAPI.login({
                    email: DEMO_EMAIL,
                    password: DEMO_PASSWORD
                });
            } catch (loginErr) {
                // If demo user does not exist yet, create it once then continue
                if (loginErr.response?.status === 401) {
                    try {
                        response = await authAPI.register({
                            email: DEMO_EMAIL,
                            password: DEMO_PASSWORD,
                            full_name: 'Demo User',
                            academic_role: 'student',
                            research_interests: ['AI', 'NLP']
                        });
                    } catch (registerErr) {
                        // If someone already created the user in parallel, retry login.
                        if (
                            registerErr.response?.status === 400 &&
                            registerErr.response?.data?.detail === 'Email already registered'
                        ) {
                            response = await authAPI.login({
                                email: DEMO_EMAIL,
                                password: DEMO_PASSWORD
                            });
                        } else {
                            throw registerErr;
                        }
                    }
                } else {
                    throw loginErr;
                }
            }

            const { access_token, user } = response.data;
            setAuth(user, access_token);
            navigate('/dashboard');
        } catch (err) {
            setError(
                err.response?.data?.detail ||
                'Demo login failed. Please try again.'
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-2xl">
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
                        Sign in to Synthesis AI
                    </h2>
                    <p className="mt-2 text-center text-sm text-gray-600">
                        AI-powered research paper generation
                    </p>
                </div>

                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    {error && (
                        <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative">
                            {error}
                        </div>
                    )}

                    <div className="rounded-md shadow-sm -space-y-px">
                        <div>
                            <label htmlFor="email" className="sr-only">Email address</label>
                            <input
                                id="email"
                                name="email"
                                type="email"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                                placeholder="Email address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                        <div>
                            <label htmlFor="password" className="sr-only">Password</label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                    </div>

                    <div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'Signing in...' : 'Sign in'}
                        </button>
                    </div>

                    <div>
                        <button
                            type="button"
                            onClick={handleDemoLogin}
                            disabled={loading}
                            className="group relative w-full flex justify-center py-2 px-4 border border-indigo-200 text-sm font-medium rounded-md text-indigo-700 bg-indigo-50 hover:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'Please wait...' : 'Demo Login'}
                        </button>
                        <p className="mt-2 text-xs text-center text-gray-500">
                            Demo: {DEMO_EMAIL} / {DEMO_PASSWORD}
                        </p>
                    </div>

                    <div className="text-sm text-center">
                        <Link to="/register" className="font-medium text-indigo-600 hover:text-indigo-500">
                            Don't have an account? Register
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;
