# Extension — Local Loading Instructions

To load the extension in Chromium/Chrome-based browsers:

1. Build/run the frontend and backend locally (frontend at `http://localhost:3000`, backend at `http://localhost:8000`).
2. Open browser `chrome://extensions` and enable "Developer mode".
3. Click "Load unpacked" and select the `extension` folder in this repo.
4. Open any page and click the extension icon, then "Check page" to call the local API proxy.

Note: The extension is a minimal prototype and calls the frontend `/api/flags` proxy running at `localhost:3000`.
