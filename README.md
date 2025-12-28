# zekkie's fun fl studio rpc tool for discord
![GitHub License](https://img.shields.io/github/license/swagswagstar/fl-rpc)  ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/swagswagstar/fl-rpc)  ![GitHub top language](https://img.shields.io/github/languages/top/swagswagstar/fl-rpc)  ![GitHub last commit](https://img.shields.io/github/last-commit/swagswagstar/fl-rpc)  ![GitHub Release Date](https://img.shields.io/github/release-date/swagswagstar/fl-rpc)  ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/swagswagstar/fl-rpc/total)  ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/swagswagstar/fl-rpc)  ![GitHub Release](https://img.shields.io/github/v/release/swagswagstar/fl-rpc)  
because fl doesn't have native discord rpc support

## features
- customize your status when you have no project open, in a saved or unsaved project!
- save your settings so you don't lose them!
- minimize to tray to avoid distractions
- yea that's pretty much it

**this program works for FL Studio 2025 only** (as far as i am aware)

## screenshot
<img width="522" height="547" alt="image" src="https://github.com/user-attachments/assets/9328aa05-ad3f-475b-8729-a0347cfd45e0" />

it's not the prettiest i know

## contributions
we accept all contributions! feel free to fork this and help out how you'd like.
if you have any issues, don't hesitate to open a issue and i'll look right into it.

## how do i make this program launch when i launch fl studio?
### instructions for windows
1. make a powershell script (make a new text file and change it's extension to `.ps1`)
2. add this to your powershell script
```sh
Start-Process "C:\Program Files\Image-Line\FL Studio 2025\FL64.exe"
Start-Sleep -Seconds 3
Start-Process "C:\wherever you downloaded our built the rpc tool.exe"
```
3. save
4. make a new shortcut on your desktop and set the location to
```sh
powershell.exe -WindowStyle Hidden -File "C:\wherever you just saved your powershell script.ps1"
```
5. set the shortcut name to **FL Studio 2025**
6. open the shortcuts properties
7. press on **Change Icon...**
8. under _Look for icons in this file:_, paste in `C:\Program Files\Image-Line\FL Studio 2025\FL64.exe`
9. click on the fl studio icon, then press **OK**
10. **Apply** > **OK** to close the properties
11. drag and drop your new shortcut onto your taskbar (and if its there, delete your old fl shortcut and use your new one)
12. enjoy
