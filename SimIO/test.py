import win32api
import win32con
import win32gui
import win32process
import psutil
import ctypes
from time import sleep


def press_key(num):
    MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
    sleep(0.4)
    win32api.keybd_event(num, MapVirtualKey(num, 0), 0, 0)
    sleep(0.2)
    win32api.keybd_event(num, MapVirtualKey(
        num, 0), win32con.KEYEVENTF_KEYUP, 0)


def press_digital(digital):
    str_digital = str(digital)
    for s in str_digital:
        press_key(int(s) + 48)


def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def db_click():
    click()
    sleep(0.1)
    click()


# hwnd_title = dict()


# def get_all_hwnd(hwnd, mouse):
#     if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
#         hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


# win32gui.EnumWindows(get_all_hwnd, 0)

# for h, t in hwnd_title.items():
#     if t is not "":
#         print(h, t)


def find_window_for_pid(pid):
    result = None

    def callback(hwnd, _):
        nonlocal result
        ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
        # print(cpid)
        if cpid == pid:
            result = hwnd
            return False
        return True
    win32gui.EnumWindows(callback, None)
    return result


def _MyCallback(hwnd, extra):
    windows = extra
    temp = []
    temp.append(hex(hwnd))
    temp.append(win32gui.GetClassName(hwnd))
    temp.append(win32gui.GetWindowText(hwnd))
    windows[hwnd] = temp


if __name__ == '__main__':
    # hwnd = win32gui.FindWindow(None, 'HDCX.exe')
    # print(hwnd)
    # win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    # click()
    # sleep(0.1)
    # press_digital(18623177000)

    app_id = 0
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if p.name() == 'HDCX.exe':
            app_id = pid

    windows = {}
    win32gui.EnumWindows(_MyCallback, windows)
    for hwnd in windows:
        ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
        if cpid == app_id:
            if len(windows[hwnd]) == 3 and windows[hwnd][2] != '':
                # win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
                try:
                    win32gui.SetForegroundWindow(hwnd)
                except:
                    print(windows[hwnd][2])
