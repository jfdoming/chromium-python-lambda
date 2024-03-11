import json
import sys

resp = json.load(sys.stdin)
print("---")
if "errorType" in resp:
    print(resp["errorMessage"], file=sys.stderr)
    sys.exit(1)
elif "status" in resp:
    if "stdout" in resp:
        print(resp["stdout"])
    if "stderr" in resp:
        print(resp["stderr"], file=sys.stderr)
    if resp["status"] == "error":
        sys.exit(1)
    if "stdout" not in resp and "stderr" not in resp:
        print(json.dumps(resp, indent=2))
