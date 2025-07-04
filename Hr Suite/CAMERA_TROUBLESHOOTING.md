# 📷 Camera Troubleshooting Guide
**HR Suite - Face Recognition System**
*Built by Snashworld, Promoted by ETRA.AE*

## 🚨 Common Camera Issues & Solutions

### 1. **"Camera Access Denied" Error

**Cause:** Browser blocked camera permissions

**Solutions:**
- **Chrome/Edge:**
  1. Click the camera icon (🎥) in the address bar
  2. Select "Allow" for camera access
  3. Refresh the page

- **Firefox:**
  1. Click the shield icon in the address bar
  2. Turn off "Enhanced Tracking Protection" for this site
  3. Allow camera access when prompted

- **Safari:**
  1. Go to Safari > Preferences > Websites > Camera
  2. Set permission to "Allow" for your HR Suite domain
  3. Refresh the page

### 2. **"No Camera Found" Error

**Cause:** No camera device detected

**Solutions:**
- Check if camera is properly connected
- Try a different USB port (for external cameras)
- Restart your computer
- Update camera drivers
- Test camera in other applications

### 3. **"Camera is Busy" Error

**Cause:** Another application is using the camera

**Solutions:**
- Close other video applications (Zoom, Teams, Skype, etc.)
- Close other browser tabs using camera
- Restart your browser
- Check Task Manager for camera-using processes

### 4. **"Camera Constraints Not Supported" Error

**Cause:** Camera doesn't support required settings

**Solutions:**
- Try a different camera
- Update camera drivers
- Use demo mode as fallback
- Contact IT support for compatible camera

## 🔧 Browser-Specific Instructions

### Google Chrome
```
1. Click the lock icon (🔒) next to the URL
2. Set Camera to "Allow"
3. Refresh the page
4. If still blocked: chrome://settings/content/camera
```

### Microsoft Edge
```
1. Click the lock icon (🔒) next to the URL
2. Set Camera to "Allow"
3. Refresh the page
4. If still blocked: edge://settings/content/camera
```

### Mozilla Firefox
```
1. Click the camera icon in the address bar
2. Select "Allow" and check "Remember this decision"
3. Refresh the page
4. If still blocked: about:preferences#privacy
```

### Safari
```
1. Safari > Preferences > Websites > Camera
2. Set to "Allow" for your domain
3. Refresh the page
```

## 🖥️ Operating System Settings

### Windows 10/11
```
1. Settings > Privacy & Security > Camera
2. Enable "Allow apps to access your camera"
3. Enable "Allow desktop apps to access your camera"
4. Restart browser
```

### macOS
```
1. System Preferences > Security & Privacy > Camera
2. Check the box next to your browser
3. Restart browser if needed
```

### Linux
```
1. Check camera permissions: ls -la /dev/video*
2. Add user to video group: sudo usermod -a -G video $USER
3. Restart browser
```

## 🛠️ Advanced Troubleshooting

### Check Camera in Browser Console
```javascript
// Test camera availability
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    console.log('Camera working!');
    stream.getTracks().forEach(track => track.stop());
  })
  .catch(err => console.error('Camera error:', err));
```

### Reset Browser Permissions
```
1. Clear browser data (cookies, cache)
2. Reset site permissions
3. Restart browser
4. Try accessing camera again
```

## 🎯 Demo Mode Alternative

If camera issues persist, the HR Suite provides a **Demo Mode**:

1. Camera access fails automatically after 3 seconds
2. Click "Use Demo Mode" button
3. Click on the face status to simulate detection
4. Continue with GPS and RFID verification

## 📞 Support Contacts

**Technical Issues:**
- IT Support: [your-it-support@company.com]
- HR Suite Support: [hr-support@company.com]

**Hardware Issues:**
- Camera not working: Contact IT for replacement
- Driver issues: Contact IT for driver updates

## 🔍 Diagnostic Information

When reporting camera issues, include:

```
- Browser: [Chrome/Firefox/Safari/Edge]
- Version: [Browser version number]
- OS: [Windows/macOS/Linux]
- Camera Model: [Built-in/External model]
- Error Message: [Exact error text]
- Console Errors: [F12 > Console tab errors]
```

## ✅ Testing Checklist

- [ ] Camera permissions allowed in browser
- [ ] No other apps using camera
- [ ] Camera working in other applications
- [ ] Browser updated to latest version
- [ ] OS camera permissions enabled
- [ ] Tried different browser
- [ ] Cleared browser cache/cookies
- [ ] Restarted computer

---

**💫 Built by Snashworld, Promoted by ETRA.AE**  
**🧠 RiSa AI Assistant - Smart HR Solutions**

*For additional support, contact your system administrator or IT department.*