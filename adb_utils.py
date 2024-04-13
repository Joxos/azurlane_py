import subprocess
from loguru import logger
import os


def take_screenshot(
    device_serial, filename="screenshot.png", adb_path="./platform-tools/adb"
):
    results = []

    completed = subprocess.run(
        [
            adb_path,
            "-s",
            device_serial,
            "shell",
            "screencap",
            "-p",
            f"/sdcard/{filename}",
        ],
        capture_output=True,
    )
    logger.debug(completed.stdout.decode())
    results.append(completed)

    if os.path.exists(filename):
        logger.error(f"{filename} already exists.")
        return results

    completed = subprocess.run(
        [adb_path, "-s", device_serial, "pull", f"/sdcard/{filename}", f"./{filename}"],
        capture_output=True,
    )
    logger.debug(completed.stdout.decode())
    results.append(completed)

    completed = subprocess.run(
        [adb_path, "-s", device_serial, "shell", "rm", f"/sdcard/{filename}"],
        capture_output=True,
    )
    logger.debug(completed.stdout.decode())
    results.append(completed)

    return results


def connect_to_device(device_serial, adb_path="./platform-tools/adb"):
    completed = subprocess.run(
        [adb_path, "connect", device_serial], capture_output=True
    )
    logger.debug(completed.stdout.decode())
    return completed


def disconnect_from_device(device_serial, adb_path="./platform-tools/adb"):
    completed = subprocess.run(
        [adb_path, "disconnect", device_serial], capture_output=True
    )
    logger.debug(completed.stdout.decode())
    return completed


def get_device_list(adb_path="./platform-tools/adb"):
    completed = subprocess.run([adb_path, "devices"], capture_output=True)
    logger.debug(completed.stdout.decode())
    result = completed.stdout.decode().split("\n")[1:-1]
    result.pop()  # remove last empty line
    return [x.split("\t")[0] for x in result]


def restart_adb_server(adb_path="./platform-tools/adb"):
    results = []

    completed = subprocess.run([adb_path, "kill-server"], capture_output=True)
    logger.debug(completed.stdout.decode())
    results.append(completed)

    completed = subprocess.run([adb_path, "start-server"], capture_output=True)
    logger.debug(completed.stdout.decode())
    results.append(completed)

    return results


def tap(device_serial, x, y, adb_path="./platform-tools/adb"):
    completed = subprocess.run(
        [adb_path, "-s", device_serial, "shell", "input", "tap", str(x), str(y)],
        capture_output=True,
    )
    logger.debug(completed.stdout.decode())
    return completed


def swipe(
    device_serial, x1, y1, x2, y2, duration=None, adb_path="./platform-tools/adb"
):
    cmd = ["adb", "-s", device_serial, "shell", "input", "swipe"]
    if duration:
        cmd.extend(["-d", str(duration)])
    cmd.extend([str(x1), str(y1), str(x2), str(y2)])
    completed = subprocess.run(cmd, capture_output=True)
    logger.debug(completed.stdout.decode())
    return completed


if __name__ == "__main__":
    # tests
    # logger.info("Restarting adb server.")
    # restart_adb_server()

    logger.info("Getting device list before connecting to any device.")
    get_device_list()

    logger.info("Connecting to device 127.0.0.1:7555.")
    connect_to_device("127.0.0.1:7555")

    logger.info("Getting device list after connecting to device 127.0.0.1:7555.")
    print(get_device_list())

    logger.info("Taking screenshot.")
    take_screenshot("127.0.0.1:7555")

    logger.info("Disconnecting from device 127.0.0.1:7555.")
    disconnect_from_device("127.0.0.1:5555")

    logger.info("Getting device list after disconnecting from device 127.0.0.1:7555.")
    get_device_list()

    logger.info("Done.")
