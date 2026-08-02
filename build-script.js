const fs = require('fs');
const { execSync } = require('child_process');

// 1. Create main.js for Electron
const mainJsContent = `
const { app, BrowserWindow } = require('electron');

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: true
    }
  });
  win.loadFile('index.html');
}

app.whenReady().then(createWindow);
`;

fs.writeFileSync('main.js', mainJsContent.trim());

// 2. Update package.json
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
pkg.main = 'main.js';
pkg.build = {
  appId: 'com.nexura.desktop',
  productName: 'Nexura',
  win: {
    target: 'portable'
  }
};

fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));

// 3. Build Portable EXE
console.log('Building Portable Windows Executable...');
execSync('npx electron-builder --win portable', { stdio: 'inherit' });
