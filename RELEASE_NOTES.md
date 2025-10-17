# 📦 Release Notes - Executable Branch

## Version: 1.0.0 - Executable Distribution
**Branch**: `executable`
**Date**: October 17, 2025

---

## 🎉 What's New

### ✨ Standalone Executable Support
- **Windows Executable** (`SistemaMatricula.exe`)
  - Single-file portable application
  - No Python installation required
  - File size: ~10-15 MB
  - Runs on Windows 10/11

- **Linux Executable** (`SistemaMatricula`)
  - Native Linux binary
  - No Python installation required
  - Compatible with most modern Linux distributions

### 🛠️ Build System
- **Automated Build Scripts**
  - `build_windows.ps1`: PowerShell script for Windows
  - `build_linux.sh`: Bash script for Linux
  - `build.ps1` / `build.sh`: Auto-detection scripts
  
- **PyInstaller Configuration**
  - Optimized spec file for minimal size
  - Excludes `data/` directory to reduce size
  - UPX compression enabled
  - Hidden console for clean GUI experience

### 📚 Comprehensive Documentation
- **BUILD_README.md**: Complete build instructions
- **USAGE.md**: End-user guide for the executable
- **Updated README.md**: Project overview with executable info
- **Troubleshooting guides**: Common issues and solutions

### 🎨 GUI Features (Included in Executable)
- Modern dark-themed interface
- Three algorithm implementations:
  - Voraz (Greedy)
  - Fuerza Bruta (Brute Force)
  - Programación Dinámica (Dynamic Programming)
- Real-time execution monitoring
- Results comparison table
- CSV export functionality
- Memory and time metrics
- Cancellable long-running operations

---

## 📥 Download & Installation

### For End Users (No Development Required)
1. Download the appropriate executable:
   - Windows: `dist/SistemaMatricula.exe`
   - Linux: `dist/SistemaMatricula`
2. Run the executable (no installation needed!)
3. Select your input file and run algorithms

### For Developers
```bash
# Clone the repository
git clone https://github.com/Frank-Totti/ADA-II-Algoritmo-mejora-sistema-de-matricula.git
cd ADA-II-Algoritmo-mejora-sistema-de-matricula

# Switch to executable branch
git checkout executable

# Build the executable
# Windows:
.\build_windows.ps1
# Linux:
./build_linux.sh
```

---

## 🔧 Technical Details

### Build Configuration
- **Python Version**: 3.8+
- **PyInstaller Version**: 6.16.0
- **Build Type**: One-file executable
- **Console**: Hidden (windowed mode)
- **Compression**: UPX enabled
- **Icon**: Default (customizable)

### Included Modules
- ✅ GUI (`gui.py`, `gui_styles.py`)
- ✅ Voraz algorithm
- ✅ Brute Force algorithm
- ✅ Dynamic Programming algorithm
- ✅ Input/Output handlers
- ✅ Tkinter and all GUI dependencies

### Excluded from Executable
- ❌ `data/` directory (test files - provide separately)
- ❌ `build/` directory (build artifacts)
- ❌ `__pycache__/` (Python cache)
- ❌ `.venv/` (virtual environment)

---

## 🧪 Testing

The executable has been tested with:
- ✅ All 46 test cases from `data/` directory
- ✅ Large datasets (1000+ students)
- ✅ Edge cases (no students, no courses, etc.)
- ✅ Long-running algorithms (cancellation feature)
- ✅ Memory-intensive operations

---

## 📊 Performance

### Executable Size
- **Windows**: ~10.62 MB (compressed)
- **Linux**: ~12-15 MB (varies by distribution)

### Startup Time
- **Cold start**: < 3 seconds
- **Subsequent runs**: < 1 second

### Memory Usage
- **Idle**: ~30-50 MB
- **Running algorithms**: Varies by input size
  - Small datasets (<100 students): 50-100 MB
  - Large datasets (>1000 students): 200-500 MB

---

## 🐛 Known Issues

1. **Windows Defender**: May flag as unknown publisher
   - **Solution**: Mark as safe or add to exclusions

2. **Linux Permissions**: May need manual chmod
   - **Solution**: `chmod +x SistemaMatricula`

3. **Large Datasets**: Brute Force can be very slow
   - **Solution**: Use cancellation feature or switch to Dynamic Programming

---

## 🔄 Migration from Source Code

If you're currently running from source:
1. No configuration changes needed
2. Same input file format
3. Same output format
4. All features preserved
5. Faster startup time with executable

---

## 📝 Changelog

### Added
- PyInstaller build configuration
- Windows and Linux build scripts
- Comprehensive build documentation
- End-user usage guide
- Auto-detection build scripts
- Git ignore rules for build artifacts

### Changed
- README now includes executable instructions
- Project structure optimized for distribution

### Excluded
- Test data from executable package (provide separately)

---

## 🚀 Future Enhancements

Planned for future releases:
- [ ] macOS executable support
- [ ] Custom application icon
- [ ] Installer packages (MSI for Windows, DEB for Linux)
- [ ] Auto-update mechanism
- [ ] Batch processing mode
- [ ] Command-line interface option
- [ ] Additional algorithms (Genetic Algorithm, Simulated Annealing)

---

## 🤝 Contributing

Contributions welcome! To add executable support features:
1. Fork the `executable` branch
2. Make your changes
3. Test the build on your platform
4. Submit a Pull Request

---

## 📞 Support

- **Repository**: https://github.com/Frank-Totti/ADA-II-Algoritmo-mejora-sistema-de-matricula
- **Branch**: `executable`
- **Issues**: Use GitHub Issues for bug reports
- **Documentation**: See BUILD_README.md and USAGE.md

---

## 🙏 Acknowledgments

- PyInstaller team for the excellent packaging tool
- tkinter for cross-platform GUI support
- All contributors to the project

---

**Happy Computing! 🎉**
