import os
import time
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from logger_utils import setup_logger
from config_utils import load_config

logger = setup_logger()

def get_disk_free_percent(path):
    """Ritorna la percentuale di spazio libero sul disco"""
    total, used, free = shutil.disk_usage(path)
    return (free / total) * 100

def cleanup_smart():
    config = load_config()
    if not config: return

    storage_path = Path("storage")
    if not storage_path.exists(): return

    # Parametri di sicurezza
    MIN_FREE_PERCENT = 10  # Mantieni almeno il 10% di spazio libero
    SAFE_HOURS = 24       # NON toccare mai i file delle ultime 24 ore (Protezione Forza Maggiore)

    logger.info(f"🛡️ [ROTATOR] Controllo spazio disco... Libero: {get_disk_free_percent(storage_path):.1f}%")

    # 1. Se lo spazio è scarso (< 10%), procediamo alla pulizia
    if get_disk_free_percent(storage_path) < MIN_FREE_PERCENT:
        logger.warning(f"⚠️ [ROTATOR] Spazio scarso (<{MIN_FREE_PERCENT}%). Avvio pulizia protetta...")

        cutoff_date = datetime.now() - timedelta(hours=SAFE_HOURS)
        files_deleted = 0

        # Raccogliamo tutti i file cancellabili (più vecchi di 24h)
        cancellable_files = []
        for camera_dir in storage_path.iterdir():
            if camera_dir.is_dir():
                for video_file in camera_dir.glob("*.ts"):
                    mtime = datetime.fromtimestamp(video_file.stat().st_mtime)
                    if mtime < cutoff_date:
                        cancellable_files.append((video_file, mtime))

        # Ordiniamo dal più vecchio al più nuovo
        cancellable_files.sort(key=lambda x: x[1])

        for video_file, _ in cancellable_files:
            try:
                video_file.unlink()
                files_deleted += 1
                logger.info(f"🗑️ [DELETE] Rimosso file vecchio: {video_file.name}")

                # Appena torniamo sopra la soglia di sicurezza, ci fermiamo
                if get_disk_free_percent(storage_path) > (MIN_FREE_PERCENT + 2):
                    break
            except Exception as e:
                logger.error(f"❌ [ERRORE] Impossibile eliminare {video_file}: {e}")

        if files_deleted > 0:
            logger.info(f"✨ [ROTATOR] Pulizia completata. Liberati {files_deleted} file.")
        else:
            logger.error("🚨 [CRITICO] Spazio esaurito ma tutti i file sono protetti (ultime 24h)! Libera spazio manualmente.")
    else:
        logger.info("✅ [ROTATOR] Spazio su disco sufficiente.")

if __name__ == "__main__":
    while True:
        try:
            cleanup_smart()
        except Exception as e:
            logger.error(f"❌ [ROTATOR] Errore imprevisto: {e}")

        # Controlla ogni ora
        time.sleep(3600)
