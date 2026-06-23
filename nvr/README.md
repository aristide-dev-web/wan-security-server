# 📹 NVR Tapo - Sistema di Registrazione Locale

Registrazione video da telecamere Tapo senza server Cloud. Salva tutto localmente sulla tua box.

## 📁 Struttura

```
NVR/
├── recorder.py       → Script principale di registrazione
├── config.json       → Configurazione camere (da compilare)
├── requirements.txt  → Dipendenze Python
├── storage/          → Video registrati
└── logs/             → Log di sistema
```

## 🚀 Setup

1. **Installa dipendenze:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configura le camere in `config.json`:**
   - Inserisci IP della Tapo
   - Username e password RTSP
   - Imposta `"enabled": true`

3. **Avvia la registrazione:**
   ```bash
   python recorder.py
   ```

## ⚙️ Configurazione (config.json)

```json
{
  "cameras": [
    {
      "name": "Camera 1",
      "ip": "192.168.1.100",
      "username": "tapo",
      "password": "tapo",
      "enabled": true
    }
  ],
  "storage": {
    "path": "./storage",
    "retention_days": 7
  }
}
```

## 💾 Storage

I video vengono salvati in:
```
storage/Camera_1/Camera_1_YYYYMMDD_HHMMSS.mp4
storage/Camera_2/Camera_2_YYYYMMDD_HHMMSS.mp4
```

## 📊 Log

I log vengono salvati in:
```
logs/nvr_YYYYMMDD.log
```

## ⏹️ Arresta

Premi `Ctrl+C` per fermare tutte le registrazioni.

---

**Costo**: €0 al mese 🎉
