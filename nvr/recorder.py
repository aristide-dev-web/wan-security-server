import threading
import subprocess
from datetime import datetime
from pathlib import Path
import time
import socket
from logger_utils import setup_logger
from config_utils import load_config

logger = setup_logger()

def check_port(ip, port):
    """Verifica se la porta è aperta prima di lanciare FFmpeg"""
    try:
        with socket.create_connection((ip, port), timeout=3):
            return True
    except Exception:
        return False

def record_camera(camera_config):
    """STABILIZZATORE NVR: Versione Ultra-Debug WAN"""
    name = camera_config["name"]
    ip = camera_config["ip"]
    port = camera_config.get("port", 554)
    username = camera_config["username"]
    password = camera_config["password"]

    rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/stream1"
    # Mascheriamo la password per il log
    masked_url = f"rtsp://{username}:******@{ip}:{port}/stream1"

    storage_dir = Path("storage") / name
    storage_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"🛠️ [DEBUG] Avvio test per {name}")
    logger.info(f"🛠️ [DEBUG] URL: {masked_url}")

    while True:
        now = datetime.now()
        hour_tag = now.strftime("%Y%m%d_%H00")
        filename = storage_dir / f"{name}_{hour_tag}.ts"
        start_hour = now.hour

        while datetime.now().hour == start_hour:
            logger.info(f"📡 [DEBUG] Controllo portale {ip}:{port}...")
            if check_port(ip, port):
                logger.info(f"✅ [DEBUG] Portale raggiungibile. Connessione alla telecamera...")
            else:
                logger.error(f"❌ [DEBUG] Portale chiuso. Controlla il Port Forwarding nella Vodafone Station.")
                time.sleep(10)
                continue

            # Comando FFmpeg ORIGINALE (Rifatto da zero per stabilità)
            ffmpeg_cmd = [
                "ffmpeg", "-hide_banner",
                "-loglevel", "error",
                "-rtsp_transport", "tcp",
                "-i", rtsp_url,
                "-c:v", "copy", "-c:a", "aac", "-f", "mpegts", "pipe:1"
            ]

            try:
                with open(filename, "ab") as f:
                    process = subprocess.Popen(
                        ffmpeg_cmd,
                        stdout=f,
                        stderr=subprocess.PIPE,
                        text=True
                    )

                    time.sleep(7)

                    if process.poll() is not None:
                        stderr_output = process.stderr.read()
                        logger.error(f"❌ [FAIL] {name} - Errore FFmpeg: {stderr_output.strip()[:150]}")

                        if "401" in stderr_output:
                            logger.error("👉 SUGGERIMENTO: Lo username o la password sono sbagliati.")
                        elif "Operation not permitted" in stderr_output:
                            logger.error("🛡️ [DEBUG WAN] Rifiuto dal router. Possibile blocco Antifrode o troppe connessioni.")
                    else:
                        logger.info(f"🟢 [OK] {name}: Registrazione partita correttamente!")
                        process.stderr.close()

                        last_size = filename.stat().st_size
                        stagnant_count = 0

                        while process.poll() is None:
                            time.sleep(10)
                            try:
                                current_size = filename.stat().st_size
                            except:
                                current_size = last_size

                            if current_size > last_size:
                                last_size = current_size
                                stagnant_count = 0
                            else:
                                stagnant_count += 1
                                if stagnant_count >= 4:
                                    logger.warning(f"💀 [TIMEOUT] {name}: Niente dati da 40 secondi. Riavvio...")
                                    process.terminate()
                                    break

                            if datetime.now().hour != start_hour:
                                process.terminate()
                                break

                    process.wait(timeout=5)

            except Exception as e:
                logger.error(f"❌ [ERRORE] {name}: {e}")

            if datetime.now().hour == start_hour:
                time.sleep(5)
            else:
                break

def main():
    config = load_config()
    if not config: return
    
    logger.info("🚀 [NVR] Avviato in modalità Debug WAN.")
    threads = []
    for camera in config.get("cameras", []):
        if camera.get("enabled"):
            thread = threading.Thread(target=record_camera, args=(camera,), daemon=True)
            thread.start()
            threads.append(thread)
            time.sleep(1)
    
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 [STOP] Arresto NVR...")

if __name__ == "__main__":
    main()
