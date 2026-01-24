module.exports = {
  appId: 'com.zusamstone.ai-studio',
  productName: 'AI Studio',
  copyright: 'Copyright © 2026 zusamstone',
  
  directories: {
    output: 'dist',
    buildResources: 'build',
  },

  files: [
    'main.js',
    'preload.js',
    'package.json',
    {
      from: '../frontend/dist',
      to: 'frontend/dist',
      filter: ['**/*'],
    },
    {
      from: '../backend',
      to: 'backend',
      filter: ['**/*', '!**/__pycache__', '!**/*.pyc', '!**/venv', '!**/env'],
    },
  ],

  extraResources: [
    {
      from: '../config',
      to: 'config',
    },
    {
      from: '../data/.gitkeep',
      to: 'data/.gitkeep',
    },
  ],

  // Windows configuration
  win: {
    target: [
      {
        target: 'portable',
        arch: ['x64'],
      },
    ],
    icon: 'build/icon.ico',
    artifactName: '${productName}-${version}-portable.${ext}',
  },

  portable: {
    artifactName: '${productName}-${version}-portable.exe',
  },

  // macOS configuration
  mac: {
    target: [
      {
        target: 'default',
        arch: ['x64', 'arm64'],
      },
    ],
    icon: 'build/icon.icns',
    category: 'public.app-category.productivity',
    hardenedRuntime: true,
    gatekeeperAssess: false,
    entitlements: 'build/entitlements.mac.plist',
    entitlementsInherit: 'build/entitlements.mac.plist',
  },

  dmg: {
    contents: [
      {
        x: 130,
        y: 220,
      },
      {
        x: 410,
        y: 220,
        type: 'link',
        path: '/Applications',
      },
    ],
  },

  // Linux configuration
  linux: {
    target: [
      {
        target: 'AppImage',
        arch: ['x64'],
      },
    ],
    icon: 'build/icons',
    category: 'Utility',
    artifactName: '${productName}-${version}.${ext}',
  },

  appImage: {
    license: '../LICENSE',
  },

  // Compression
  compression: 'normal',

  // Update configuration (for future)
  publish: null,
};
