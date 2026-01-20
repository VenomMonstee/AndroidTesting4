# Android UI and App Tester

Automated testing framework for Android devices using ADB (Android Debug Bridge) and Python.

## 🚀 Overview

This project automates the process of testing third-party and system applications on an Android device. It launches apps, checks if they successfully come to the foreground, captures screenshots, and logs errors into an Excel report.

## ✨ Features

- **Automated App Launching**: Uses `adb monkey` to launch both third-party and system apps.
- **Foreground Verification**: Checks if the app successfully gained focus.
- **Error Capture**: Gathers error-level logs from `logcat` during the test run.
- **Visual Evidence**: Automatically takes screenshots of each application after launch.
- **Excel Reporting**: Generates a comprehensive `.xlsx` report with test results, app types, and error summaries.

## 🛠️ Prerequisites

Before running the script, ensure you have the following installed:

1.  **Android SDK Platform-Tools**: ADB must be installed.
2.  **Python 3.x**: The core script is written in Python.
3.  **Required Python Packages**:
    ```bash
    pip install pandas openpyxl
    ```
4.  **USB Debugging**: Enabled on your connected Android device.

## ⚙️ Configuration

In `android_tester.py`, update the `ADB_PATH` variable to point to your local `adb.exe` location:

```python
ADB_PATH = r"C:\path\to\your\android-sdk\platform-tools\adb.exe"
```

## 📂 Project Structure

- `android_tester.py`: The main automation script.
- `screenshots/`: Directory where test screenshots are saved.
- `.gitignore`: Configured to exclude temporary files and large reports.
- `README.md`: This documentation.

## 📊 How to Run

1. Connect your Android device via USB.
2. Verify connection: `adb devices`.
3. Run the script:
   ```bash
   python android_tester.py
   ```
4. View the results in `test_report_expanded.xlsx`.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
