import subprocess
import re


def get_current_app_package_name():
    # adb_command = "adb shell dumpsys activity"
    # 构建 PowerShell 命令
    adb_command = [
        'powershell.exe',
        '-Command',
        'adb shell dumpsys activity | Select-String -Pattern \'mCurrentFocus|mFocusedApp\''
    ]
    try:
        # 尝试执行adb命令并获取输出
        result = subprocess.check_output(adb_command, shell=True, stderr=subprocess.STDOUT)
        output = result.decode()
        print("ADB Output:")
        print(output)  # 打印完整输出以便调试

        for line in output.split('\n'):
            # 注意：用于过滤的关键字可能会因Android版本而异，如果不起作用，请尝试其他关键字如 'mFocusedApp'
            if "mCurrentFocus" in line:
                pattern = r'([\w.]+)/([\w.]+)'
                match = re.search(pattern, line)
                if match:
                    return match.group(1),match.group(2)

            elif "mFocusedApp" in line:
                pattern = r'([\w.]+)/([\w.]+)'
                match = re.search(pattern, line)
                if match:
                    return match.group(1), match.group(2)

        return None

    except subprocess.CalledProcessError as e:
        # 如果adb命令返回非零退出码，捕获该异常
        print(f"Failed to execute adb command: {e.output.decode()}")  # 解码输出以便阅读
        return None
    except Exception as e:
        # 捕获其他所有异常
        print(f"An error occurred: {e}")
        return None


def uninstall_app(package_name):
    # 询问用户是否确实想要卸载该应用
    confirm = input(f"Are you sure you want to uninstall {package_name}? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Uninstall cancelled by user.")
        return

    try:
        # 使用adb命令卸载应用
        subprocess.check_call(f"adb shell pm uninstall --user 0 {package_name}", shell=True)
        print(f"App {package_name} uninstalled successfully.")
    except subprocess.CalledProcessError as e:
        # 如果卸载失败（例如，因为用户没有足够的权限或应用不存在），则捕获异常
        print(f"Failed to uninstall app {package_name}: {e}")
    except Exception as e:
        # 捕获其他所有异常
        print(f"An error occurred while trying to uninstall app {package_name}: {e}")

    # 调用函数获取当前前台应用的包名

if __name__ == "__main__":
    appPackage, appActivity = get_current_app_package_name()
    print(f"Current app package name: {appPackage}")
    print(f"Current app activity name: {appActivity}")
    # 如果成功获取到包名且包名不为None，则尝试卸载该应用
    # if appPackage is not None:
    #     uninstall_app(appPackage)
    # else:
    #     print("Failed to get the current app package name.")

    # 直接在win11 PowerShell中执行如下命令亦可
    # adb shell dumpsys activity | Select - String - Pattern 'mCurrentFocus|mFocusedApp'