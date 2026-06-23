import subprocess
import time
import sys
from logger_utils import setup_logger

logger = setup_logger()

def start_nvr():
    logger.info("🐕 [WATCHDOG] Avvio del processo NVR (recorder.py)...")
    return subprocess.Popen([sys.executable, "recorder.py"])

def monitor():
    process = start_nvr()

    while True:
        # Controlla se il processo è ancora vivo
        if process.poll() is not None:
            logger.error("🚨 [WATCHDOG] Il recorder si è fermato inaspettatamente! Riavvio in corso...")
            time.sleep(5)
            process = start_nvr()

        # Controlla ogni 30 secondi
        time.sleep(30)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        logger.info("🛑 [WATCHDOG] Arresto monitoraggio.")
