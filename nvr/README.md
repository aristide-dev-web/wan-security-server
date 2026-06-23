[README.md](https://github.com/user-attachments/files/29260574/README.md)
# 📹 WAN Security Server - NVR Personale (Tapo Edition)

Benvenuti nel mio progetto **WAN Security Server**! Questo sistema è stato progettato e ottimizzato specificamente per telecamere **TP-Link Tapo**, permettendo una gestione professionale dei flussi video senza dipendere dai servizi cloud a pagamento. 

Il progetto è il frutto di circa **2 settimane di lavoro** intenso per creare una soluzione di videosorveglianza robusta, flessibile e completamente controllabile a distanza, ora funzionante al 100%.

---

## 🚀 La Mia Visione: Da Vecchio PC a Server Professionale
Ho trasformato un **vecchio Mac** in un server di registrazione dedicato (NVR). Il computer funge da "cervello" centrale che riceve i flussi video dalle telecamere e li salva localmente sulla box, garantendo privacy totale e costi zero.

### 🌟 Caratteristiche Principali:
*   **Controllo Totale da iPhone**: Posso monitorare lo stato del server, avviare o bloccare le registrazioni e visualizzare i video direttamente dal mio iPhone, ovunque mi trovi nel mondo.
*   **Sicurezza WAN con Tailscale**: Utilizzo **Tailscale** per creare una rete privata sicura (VPN), permettendomi di accedere al server con protezione criptata come se fossi in rete locale.
*   **Accesso Remoto Globale**: Ho configurato un portale dedicato (DDNS) per garantire l'accesso in WAN costante, permettendo al sistema di registrare e trasmettere anche fuori casa.
*   **Smart Rotation (Gestione Spazio)**: Il sistema monitora il disco e cancella automaticamente i video più vecchi per far posto ai nuovi, garantendo un ciclo continuo di registrazione.
*   **Watchdog (Cane da Guardia)**: Un processo di controllo attivo 24/7 che riavvia istantaneamente il sistema in caso di crash o blocco dello streaming.

---

## 📁 Struttura del Software
- `recorder.py`: Il cuore del sistema che gestisce la connessione RTSP e lo streaming.
- `watchdog.py`: Il supervisore che garantisce che il servizio sia sempre attivo.
- `rotator.py`: Gestisce la pulizia automatica dello storage in base allo spazio disponibile.
- `config.json`: File di configurazione centrale per gestire telecamere e preferenze.

---

## 🛠️ Guida al Setup Rapido

1. **Installazione Dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurazione (`config.json`)**:
   Inserisci i dati delle tue telecamere (IP locale o DDNS, Username e Password RTSP configurati nell'app Tapo):
   ```json
   {
     "cameras": [
       {
         "name": "Camera_1",
         "ip": "INSERISCI_IP_O_DDNS",
         "username": "TUO_USERNAME",
         "password": "TUA_PASSWORD",
         "enabled": true
       }
     ],
     "storage": {
       "path": "./storage",
       "retention_days": 7
     }
   }
   ```

3. **Avvio del Sistema**:
   Si consiglia di avviare sempre tramite il Watchdog per la massima stabilità:
   ```bash
   python watchdog.py
   ```

---

**Costo di gestione**: €0 al mese 🎉  
*Progetto sviluppato con passione da Aristide per la sicurezza e l'architettura WAN.*
