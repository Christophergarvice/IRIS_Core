import os
import sys
import datetime

# Add project root to path so IRIS can access modules
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from modules.simplebook_memory_logger import log_event, get_summary
import os
import datetime
from modules.simplebook_memory_logger import log_event, get_summary

# IRIS Core System
def iris_startup():
    print("\n[IRIS SYSTEM STARTED]")
    log_event("IRIS", "startup", "success", "System initialized successfully.")
    print(f"Startup time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def iris_log_action(module, action, result="success", notes=""):
    log_event(module, action, result, notes)
    print(f"Logged: {module} | {action} | {result}")

def iris_summary():
    summary = get_summary()
    print("\n[IRIS SYSTEM SUMMARY]")
    print(f"Successes: {summary['success']}")
    print(f"Failures: {summary['fail']}")

if __name__ == "__main__":
    iris_startup()
    iris_log_action("SimpleBook", "test_backup", "success", "Backup system validated.")
    iris_log_action("Parser", "module_test", "fail", "OCR format mismatch detected.")
    iris_summary()