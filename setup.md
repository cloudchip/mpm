
### 1. **Install PyInstaller**
Install PyInstaller globally or in a virtual environment:
```bash
pip install pyinstaller
```

---

### 2. **Generate the Executable**
Run PyInstaller to bundle the script into an executable:
```bash
pyinstaller --onefile mpm.py
```

- `--onefile`: Creates a single executable file.
- `mpm.py`: The name of your main Python script.

This will create an executable in the `dist` folder:
- **Windows**: `dist/mpm.exe`
- **Linux/Mac**: `dist/mpm`

---

### 3. **Test the Executable**
Navigate to the `dist` directory and test the executable:
```bash
cd dist
./mpm init esp32
```

---

### 4. **Distribute the Executable**
- **Windows**: Share `mpm.exe` as the CLI tool.
- **Linux/Mac**: Share the `mpm` binary and ensure it has executable permissions:
  ```bash
  chmod +x mpm
  ```

---

### 5. **Add to PATH for Easy Access**
To make the executable accessible system-wide:
1. Move it to a directory in your system's `PATH`.
   ```bash
   mv mpm /usr/local/bin
   ```
2. Now, you can run `mpm` from anywhere.

---

### 6. **Publish the Binary**
You can distribute the executables via:
- **GitHub Releases**: Upload the executables for each OS in your repository.
- **Custom Installer Scripts**: Provide platform-specific scripts to download and install the binary.
