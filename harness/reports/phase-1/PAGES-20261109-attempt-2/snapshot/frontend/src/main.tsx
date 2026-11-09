import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, HashRouter } from 'react-router-dom';
import { Toaster } from 'sonner';
import { App } from '@/app/App';
import '@/styles.css';
const queryClient=new QueryClient({defaultOptions:{queries:{staleTime:10000}}});
// Pages has no SPA rewrite support; hash routes keep reloads on index.html.
const Router = import.meta.env.VITE_GITHUB_PAGES === 'true' ? HashRouter : BrowserRouter;
ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><QueryClientProvider client={queryClient}><Router><App/></Router><Toaster position="bottom-right" richColors closeButton/></QueryClientProvider></React.StrictMode>);
