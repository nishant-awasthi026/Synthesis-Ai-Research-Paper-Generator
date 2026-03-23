import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
    persist(
        (set) => ({
            user: null,
            token: null,
            isAuthenticated: false,

            setAuth: (user, token) => {
                localStorage.setItem('token', token);
                set({ user, token, isAuthenticated: true });
            },

            clearAuth: () => {
                localStorage.removeItem('token');
                set({ user: null, token: null, isAuthenticated: false });
            },

            updateUser: (user) => set({ user }),
        }),
        {
            name: 'auth-storage',
        }
    )
);

export const usePaperStore = create((set) => ({
    currentPaper: null,
    papers: [],

    setCurrentPaper: (paper) => set({ currentPaper: paper }),
    setPapers: (papers) => set({ papers }),
    addPaper: (paper) => set((state) => ({ papers: [...state.papers, paper] })),
    updatePaper: (id, updates) => set((state) => ({
        papers: state.papers.map(p => p.id === id ? { ...p, ...updates } : p),
        currentPaper: state.currentPaper?.id === id
            ? { ...state.currentPaper, ...updates }
            : state.currentPaper,
    })),
    removePaper: (id) => set((state) => ({
        papers: state.papers.filter(p => p.id !== id),
        currentPaper: state.currentPaper?.id === id ? null : state.currentPaper,
    })),
}));

export const useValidationStore = create((set) => ({
    validations: {},

    setValidation: (paperId, validation) => set((state) => ({
        validations: { ...state.validations, [paperId]: validation },
    })),

    clearValidation: (paperId) => set((state) => {
        const { [paperId]: removed, ...rest } = state.validations;
        return { validations: rest };
    }),
}));

export const useChatStore = create((set) => ({
    chatHistory: {},

    addMessage: (paperId, message) => set((state) => ({
        chatHistory: {
            ...state.chatHistory,
            [paperId]: [...(state.chatHistory[paperId] || []), message],
        },
    })),

    clearChat: (paperId) => set((state) => {
        const { [paperId]: removed, ...rest } = state.chatHistory;
        return { chatHistory: rest };
    }),

    setHistory: (paperId, history) => set((state) => ({
        chatHistory: { ...state.chatHistory, [paperId]: history },
    })),
}));
