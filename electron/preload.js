const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Settings
  settings: {
    get: (key) => ipcRenderer.invoke('settings:get', key),
    set: (key, value) => ipcRenderer.invoke('settings:set', key, value),
    getAll: () => ipcRenderer.invoke('settings:getAll'),
    reset: () => ipcRenderer.invoke('settings:reset'),
  },

  // File operations
  file: {
    select: () => ipcRenderer.invoke('file:select'),
    selectFolder: () => ipcRenderer.invoke('file:selectFolder'),
    saveDialog: (options) => ipcRenderer.invoke('file:saveDialog', options),
  },

  // System
  system: {
    getDataDir: () => ipcRenderer.invoke('system:getDataDir'),
    openExternal: (url) => ipcRenderer.invoke('system:openExternal', url),
    showItemInFolder: (path) => ipcRenderer.invoke('system:showItemInFolder', path),
  },

  // Window controls
  window: {
    minimize: () => ipcRenderer.invoke('window:minimize'),
    maximize: () => ipcRenderer.invoke('window:maximize'),
    close: () => ipcRenderer.invoke('window:close'),
  },

  // App info
  app: {
    getVersion: () => ipcRenderer.invoke('app:getVersion'),
    getPath: (name) => ipcRenderer.invoke('app:getPath', name),
  },

  // Notifications
  notification: {
    show: (title, body) => ipcRenderer.send('notification:show', { title, body }),
  },

  // Backend communication
  backend: {
    request: (endpoint, method = 'GET', data = null) => {
      const id = Math.random().toString(36).substring(7);
      return new Promise((resolve, reject) => {
        const responseHandler = (event, { id: responseId, success, data: responseData, error }) => {
          if (responseId === id) {
            ipcRenderer.removeListener('backend:response', responseHandler);
            if (success) {
              resolve(responseData);
            } else {
              reject(new Error(error));
            }
          }
        };

        ipcRenderer.on('backend:response', responseHandler);
        ipcRenderer.send('backend:request', { id, endpoint, method, data });

        // Timeout after 30 seconds
        setTimeout(() => {
          ipcRenderer.removeListener('backend:response', responseHandler);
          reject(new Error('Request timeout'));
        }, 30000);
      });
    },

    onReady: (callback) => {
      ipcRenderer.on('backend:ready', callback);
    },

    removeReadyListener: (callback) => {
      ipcRenderer.removeListener('backend:ready', callback);
    },
  },

  // Event listeners
  on: (channel, callback) => {
    const validChannels = ['backend:ready', 'resource:update', 'notification'];
    if (validChannels.includes(channel)) {
      ipcRenderer.on(channel, (event, ...args) => callback(...args));
    }
  },

  once: (channel, callback) => {
    const validChannels = ['backend:ready'];
    if (validChannels.includes(channel)) {
      ipcRenderer.once(channel, (event, ...args) => callback(...args));
    }
  },

  removeListener: (channel, callback) => {
    const validChannels = ['backend:ready', 'resource:update', 'notification'];
    if (validChannels.includes(channel)) {
      ipcRenderer.removeListener(channel, callback);
    }
  },
});

// Expose platform info
contextBridge.exposeInMainWorld('platform', {
  name: process.platform,
  isWindows: process.platform === 'win32',
  isMac: process.platform === 'darwin',
  isLinux: process.platform === 'linux',
});

console.log('Preload script loaded');
