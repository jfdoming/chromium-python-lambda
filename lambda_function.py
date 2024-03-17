import json
import os
import subprocess
import sys
from io import IOBase
from tempfile import TemporaryFile
from typing import Any


def get_env():
    env = os.environ.copy()

    # Keep the PYTHONPATH from the lambda environment
    env["PYTHONPATH"] = ":".join(sys.path)

    # Don't buffer stdout/stderr
    env["PYTHONUNBUFFERED"] = "1"

    # Disable dbus
    env["DBUS_SESSION_BUS_ADDRESS"] = "/dev/null"

    # Configure fonts
    env["FONTCONFIG_PATH"] = "/opt/.fonts"

    return env


def TempFile():
    return TemporaryFile(mode="w+b")


def read_file(file: IOBase):
    file.seek(0)
    return file.read().decode("utf-8")


CMD_BASE = ["python", "main.py"]
REDACTED_CMD = ["python", "main.py", "..."]


def lambda_handler(event: Any, _):
    with TempFile() as stdout, TempFile() as stderr:
        try:
            subprocess.run(
                CMD_BASE + [json.dumps(event)],
                stdout=stdout,
                stderr=stderr,
                check=True,
                env=get_env(),
                # This should be under the lambda's limit.
                timeout=60 * 4.5,
            )
            return json.loads(read_file(stdout))
        except subprocess.TimeoutExpired as e:
            error_message = str(
                subprocess.TimeoutExpired(REDACTED_CMD, e.timeout)
            )
        except subprocess.CalledProcessError as e:
            error_message = str(
                subprocess.CalledProcessError(e.returncode, REDACTED_CMD)
            )
        except json.JSONDecodeError as e:
            error_message = str(e)
        except FileNotFoundError:
            error_message = (
                "FileNotFoundError: Did you forget to add a main.py file?"
            )

        raise Exception(
            json.dumps(
                {
                    "status": "error",
                    "stdout": read_file(stdout),
                    "stderr": read_file(stderr) + "\n---\n" + error_message,
                }
            )
        )


if __name__ == "__main__":
    raise AssertionError(
        "Function should be called from a lambda docker image"
    )
