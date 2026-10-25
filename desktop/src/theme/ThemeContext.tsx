import React, { createContext, useContext, useEffect, useState, useMemo, useCallback } from 'react';

export type ThemeMode = 'light' | 'dark' | 'system';
export type ResolvedTheme = 'light' | 'dark';

export interface ThemeContextType {
    theme: ThemeMode;
    resolvedTheme: ResolvedTheme;
    setTheme: (mode: ThemeMode) => void;
    toggleTheme: () => void;
}

const STORAGE_KEY = 'theme';
const LEGACY_STORAGE_KEY = 'precisionx_theme_mode';

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export interface ThemeProviderProps {
    children: React.ReactNode;
    defaultTheme?: ThemeMode;
    storageKey?: string;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({
    children,
    defaultTheme = 'system',
    storageKey = STORAGE_KEY,
}) => {
    const [theme, setThemeState] = useState<ThemeMode>(() => {
        if (typeof window === 'undefined') return defaultTheme;
        try {
            const saved = (localStorage.getItem(storageKey) || localStorage.getItem(LEGACY_STORAGE_KEY)) as ThemeMode;
            if (saved === 'light' || saved === 'dark' || saved === 'system') {
                return saved;
            }
        } catch (e) {
            console.warn('[ThemeContext] LocalStorage read failed:', e);
        }
        return defaultTheme;
    });

    const [systemPrefersDark, setSystemPrefersDark] = useState<boolean>(() => {
        if (typeof window === 'undefined') return true;
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    });

    // Real-time listener for OS color-scheme changes when in 'system' mode
    useEffect(() => {
        if (typeof window === 'undefined') return;

        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        const handleChange = (e: MediaQueryListEvent) => {
            setSystemPrefersDark(e.matches);
        };

        if (mediaQuery.addEventListener) {
            mediaQuery.addEventListener('change', handleChange);
            return () => mediaQuery.removeEventListener('change', handleChange);
        } else if (mediaQuery.addListener) {
            mediaQuery.addListener(handleChange);
            return () => mediaQuery.removeListener(handleChange);
        }
    }, []);

    // Compute resolved theme
    const resolvedTheme: ResolvedTheme = useMemo(() => {
        if (theme === 'system') {
            return systemPrefersDark ? 'dark' : 'light';
        }
        return theme;
    }, [theme, systemPrefersDark]);

    // Apply root data-theme and classes to document.documentElement (<html>)
    useEffect(() => {
        if (typeof document === 'undefined') return;

        const root = document.documentElement;
        const body = document.body;

        // Toggle data-theme="light" or data-theme="dark"
        root.setAttribute('data-theme', resolvedTheme);

        if (resolvedTheme === 'dark') {
            root.classList.add('dark');
            root.classList.remove('light');
            body?.classList.remove('theme-emerald');
        } else {
            root.classList.add('light');
            root.classList.remove('dark');
            body?.classList.add('theme-emerald');
        }

        // Bridge to window for hybrid vanilla/react interop
        if (typeof window !== 'undefined') {
            (window as any).currentThemeMode = theme;
            if ((window as any).ThemeContext) {
                (window as any).ThemeContext.mode = theme;
                (window as any).ThemeContext.resolvedTheme = resolvedTheme;
            }
        }
    }, [theme, resolvedTheme]);

    const setTheme = useCallback((newTheme: ThemeMode) => {
        if (!['light', 'dark', 'system'].includes(newTheme)) return;
        setThemeState(newTheme);
        try {
            localStorage.setItem(storageKey, newTheme);
            localStorage.setItem(LEGACY_STORAGE_KEY, newTheme);
        } catch (e) {
            console.warn('[ThemeContext] LocalStorage write failed:', e);
        }
    }, [storageKey]);

    const toggleTheme = useCallback(() => {
        setTheme(resolvedTheme === 'dark' ? 'light' : 'dark');
    }, [resolvedTheme, setTheme]);

    const value = useMemo<ThemeContextType>(() => ({
        theme,
        resolvedTheme,
        setTheme,
        toggleTheme,
    }), [theme, resolvedTheme, setTheme, toggleTheme]);

    return (
        <ThemeContext.Provider value={value}>
            {children}
        </ThemeContext.Provider>
    );
};

export const useTheme = (): ThemeContextType => {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
};

export default ThemeContext;
