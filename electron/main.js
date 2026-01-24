const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const Store = require('electron-store');

// Initialize electron-store for settings
const store = new Store();

// Python backend process
let pythonProcess = null;
let mainWindow = null;

// Portable mode configuration
const isPortable = process.env.PORTABLE_MODE === 'true' || !app.isPackaged;
const appRoot = app.getAppPath();
const dataDir = isPortable 
  ? path.join(appRoot, '..', 'data')
  : path.join(app.getPath('userData'), 'data');

// Set userData path for portable mode
if (isPortable) {
  const portableUserData = path.join(appRoot, '..', 'userData');
  app.setPath('userData', portableUserData);
}

// Configure app for portable mode
if (isPortable) {
  process.env.AI_STUDIO_DATA_DIR = dataDir;
  process.env.PORTABLE_MODE = 'true';
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 600,
    backgroundColor: '#1a1a1a',
    titleBarStyle: 'default',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webSecurity: true,
    },
  });

  // Load the app
  if (app.isPackaged) {
    // Production: load built frontend
    mainWindow.loadFile(path.join(__dirname, '..', 'frontend', 'dist', 'index.html'));
  } else {
    // Development: load from Vite dev server
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  }

  // Open external links in browser
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function startPythonBackend() {
  if (pythonProcess) {
    console.log('Python backend already running');
    return;
  }

  const pythonPath = app.isPackaged
    ? path.join(appRoot, '..', 'python', 'python') // Bundled Python
    : 'python3'; // Development

  const backendScript = app.isPackaged
    ? path.join(appRoot, '..', 'backend', 'main.py')
    : path.join(appRoot, '..', 'backend', 'main.py');

  console.log('Starting Python backend:', pythonPath, backendScript);

  pythonProcess = spawn(pythonPath, [backendScript], {
    env: {
      ...process.env,
      PORTABLE_MODE: isPortable ? 'true' : 'false',
      AI_STUDIO_DATA_DIR: dataDir,
    },
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
    pythonProcess = null;
  });

  // Health check
  setTimeout(() => {
    checkBackendHealth();
  }, 3000);
}

async function checkBackendHealth() {
  try {
    const response = await fetch('http://localhost:8000/api/health');
    if (response.ok) {
      console.log('Backend is healthy');
      if (mainWindow) {
        mainWindow.webContents.send('backend:ready');
      }
    } else {
      throw new Error('Backend health check failed');
    }
  } catch (error) {
    console.error('Backend health check failed:', error);
    if (mainWindow) {
      dialog.showErrorBox(
        'Backend Error',
        'Failed to start the AI Studio backend. Please check logs for details.'
      );
    }
  }
}

function stopPythonBackend() {
  if (pythonProcess) {
    console.log('Stopping Python backend');
    pythonProcess.kill('SIGTERM');
    
    // Force kill if not stopped after 5 seconds
    setTimeout(() => {
      if (pythonProcess) {
        pythonProcess.kill('SIGKILL');
      }
    }, 5000);
  }
}

// App lifecycle
app.whenReady().then(() => {
  createWindow();
  startPythonBackend();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  stopPythonBackend();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  stopPythonBackend();
});

// IPC Handlers

// Settings
ipcMain.handle('settings:get', async (event, key) => {
  return store.get(key);
});

ipcMain.handle('settings:set', async (event, key, value) => {
  store.set(key, value);
  return true;
});

ipcMain.handle('settings:getAll', async () => {
  return store.store;
});

ipcMain.handle('settings:reset', async () => {
  store.clear();
  return true;
});

// File operations
ipcMain.handle('file:select', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile', 'multiSelections'],
    filters: [
      { name: 'Documents', extensions: ['pdf', 'txt', 'md', 'docx', 'html', 'json', 'csv'] },
      { name: 'All Files', extensions: ['*'] },
    ],
  });
  return result.filePaths;
});

ipcMain.handle('file:selectFolder', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory'],
  });
  return result.filePaths[0];
});

ipcMain.handle('file:saveDialog', async (event, options) => {
  const result = await dialog.showSaveDialog(mainWindow, options);
  return result.filePath;
});

// System
ipcMain.handle('system:getDataDir', async () => {
  return dataDir;
});

ipcMain.handle('system:openExternal', async (event, url) => {
  await shell.openExternal(url);
  return true;
});

ipcMain.handle('system:showItemInFolder', async (event, path) => {
  shell.showItemInFolder(path);
  return true;
});

// Window controls
ipcMain.handle('window:minimize', () => {
  mainWindow?.minimize();
});

ipcMain.handle('window:maximize', () => {
  if (mainWindow?.isMaximized()) {
    mainWindow.unmaximize();
  } else {
    mainWindow?.maximize();
  }
});

ipcMain.handle('window:close', () => {
  mainWindow?.close();
});

// App info
ipcMain.handle('app:getVersion', () => {
  return app.getVersion();
});

ipcMain.handle('app:getPath', (event, name) => {
  return app.getPath(name);
});

// Notifications
ipcMain.on('notification:show', (event, { title, body }) => {
  if (mainWindow && !mainWindow.isFocused()) {
    const notification = {
      title,
      body,
    };
    // Show system notification
    console.log('Notification:', notification);
  }
});

// Backend communication relay
ipcMain.on('backend:request', async (event, { id, endpoint, method, data }) => {
  try {
    const response = await fetch(`http://localhost:8000${endpoint}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: data ? JSON.stringify(data) : undefined,
    });

    const result = await response.json();
    event.reply('backend:response', { id, success: true, data: result });
  } catch (error) {
    event.reply('backend:response', { 
      id, 
      success: false, 
      error: error.message 
    });
  }
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  dialog.showErrorBox('Unexpected Error', error.message);
});

process.on('unhandledRejection', (error) => {
  console.error('Unhandled Rejection:', error);
});

console.log('Electron main process started');
console.log('Portable mode:', isPortable);
console.log('App root:', appRoot);
console.log('Data directory:', dataDir);
