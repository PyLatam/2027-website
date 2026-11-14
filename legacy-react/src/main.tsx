import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import { App } from '@/app/App';
import { LocaleProvider } from '@/i18n/LocaleProvider';
import '@/styles/global.css';

const container = document.getElementById('root');

if (!container) {
  throw new Error('Missing #root element in index.html.');
}

createRoot(container).render(
  <StrictMode>
    <LocaleProvider>
      <App />
    </LocaleProvider>
  </StrictMode>,
);
