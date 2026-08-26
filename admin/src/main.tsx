import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import { presetGpnDefault, Theme } from '@consta/uikit/Theme';

import { App } from './App';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Theme preset={presetGpnDefault}>
      <App />
    </Theme>
  </StrictMode>
);
