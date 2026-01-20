import subprocess
import time
import os
import pandas as pd

ADB_PATH = r"C:\Users\vedan\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def run_adb(args):
    command = [ADB_PATH] + args
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def get_installed_apps():
    output = run_adb(["shell", "pm", "list", "packages", "-3"])
    return [line.split(":")[1] for line in output.splitlines() if line.strip()]

def get_foreground_app():
    # Modern adb command to get the foreground package name
    output = run_adb(["shell", "dumpsys", "window", "windows", "|", "grep", "-E", "'mCurrentFocus|mFocusedApp'"])
    return output

def test_app(package_name, app_type="Third Party"):
    print(f"Testing {app_type}: {package_name}")
    
    # Clear logcat
    run_adb(["logcat", "-c"])
    
    # Launch app
    run_adb(["shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"])
    time.sleep(5)  # Let it load
    
    # Take screenshot
    screenshot_name = f"screenshots/{package_name.replace('.', '_')}.png"
    run_adb(["shell", "screencap", "-p", f"/sdcard/tmp.png"])
    run_adb(["pull", f"/sdcard/tmp.png", screenshot_name])
    
    # Capture brief logcat for errors/crashes
    log_output = run_adb(["logcat", "-d", "*:E"]) # Capture Errors only
    log_summary = "No Errors Found" if not log_output else log_output[:500].replace("\n", "; ")
    
    # Check if app is in foreground
    foreground = get_foreground_app()
    status = "Passed" if package_name in foreground else "Failed (Not in focus)"
    
    # Return to home
    run_adb(["shell", "input", "keyevent", "3"])
    time.sleep(1)
    
    return {
        "App Name": package_name,
        "Type": app_type,
        "Result": status,
        "Screenshot": screenshot_name,
        "Errors": log_summary
    }

def main():
    all_apps = get_installed_apps()
    # Test up to 30 apps total now
    apps_to_test = all_apps[:25]
    
    results = []
    
    # Specific System tests
    system_tests = [
        ("com.google.android.dialer", "Dialer"),
        ("com.google.android.apps.messaging", "Messaging"),
        ("com.nothing.camera", "Nothing Camera"),
        ("com.android.settings", "Settings"),
        ("com.google.android.contacts", "Contacts")
    ]
    
    for pkg, name in system_tests:
        res = test_app(pkg, "System UI")
        res["App Name"] = f"{name} ({pkg})"
        results.append(res)
        
    for pkg in apps_to_test:
        results.append(test_app(pkg, "Third Party"))

    df = pd.DataFrame(results)
    df.to_excel("test_report_expanded.xlsx", index=False)
    print("Expanded report generated: test_report_expanded.xlsx")

if __name__ == "__main__":
    main()
