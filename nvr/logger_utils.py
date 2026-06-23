import logging
from datetime import datetime
from pathlib import Path

def setup_logger():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f"nvr_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("NVR")
