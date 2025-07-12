import sys
import os
import re
import subprocess
import shutil

def get_adb_path():
    # 1. 优先查找同级目录
    if getattr(sys, 'frozen', False):
        # exe模式
        script_dir = os.path.dirname(sys.executable)
    else:
        # 脚本模式
        script_dir = os.path.dirname(os.path.abspath(__file__))
    adb_path = os.path.join(script_dir, 'adb.exe')
    print(f'优先查找同级目录adb.exe: {adb_path}')
    if os.path.exists(adb_path):
        return adb_path
    # 2. 查找系统环境变量
    adb_in_path = shutil.which('adb')
    print(f'查找系统环境变量adb: {adb_in_path}')
    if adb_in_path:
        return adb_in_path
    print('未找到adb.exe，请将adb.exe放在脚本/可执行文件同级目录，或配置到环境变量。')
    return None

def get_current_app_package_name():
    adb_path = get_adb_path()
    if not adb_path:
        print('adb未找到，无法继续。')
        return None
    adb_command = [adb_path, 'shell', 'dumpsys', 'activity', 'activities']
    try:
        result = subprocess.check_output(adb_command, stderr=subprocess.STDOUT)
        output = result.decode('gbk', errors='ignore')
        print('ADB Output:')
        print(output)

        for line in output.split('\n'):
            if any(key in line for key in ['mCurrentFocus', 'mFocusedApp', 'mResumedActivity']):
                pattern = r'([\w\.]+)/([\w\.]+)'
                match = re.search(pattern, line)
                if match:
                    return match.group(1), match.group(2)
        return None
    except subprocess.CalledProcessError as e:
        print(f'Failed to execute adb command: {e.output.decode("gbk", errors="ignore")}')
        return None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def uninstall_app(package_name):
    confirm = input(f'Are you sure you want to uninstall {package_name}? (yes/no): ')
    if confirm.lower() != 'yes':
        print('Uninstall cancelled by user.')
        return

    adb_path = get_adb_path()
    if not adb_path:
        print('adb未找到，无法卸载。')
        return
    try:
        subprocess.check_call([adb_path, 'shell', 'pm', 'uninstall', '--user', '0', package_name])
        print(f'App {package_name} uninstalled successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Failed to uninstall app {package_name}: {e}')
    except Exception as e:
        print(f'An error occurred while trying to uninstall app {package_name}: {e}')

if __name__ == '__main__':
    result = get_current_app_package_name()
    if result is not None:
        appPackage, appActivity = result
        print(f'Current app package name: {appPackage}')
        print(f'Current app activity name: {appActivity}')
        uninstall_app(appPackage)
    else:
        print('Failed to get the current app package name.')
    input('按回车键退出...')