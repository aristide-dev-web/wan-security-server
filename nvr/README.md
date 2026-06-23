# 📹 WAN Security Server - NVR Personale (Tapo Edition)

Benvenuti nel mio progetto **WAN Security Server**! Questo sistema è stato ottimizzato specificamente per telecamere **TP-Link Tapo**, permettendo una gestione professionale dei flussi video senza dipendere dai servizi cloud a pagamento. 

Questo progetto è il frutto di circa **2 settimane di lavoro** intenso per creare un sistema di videosorveglianza robusto, flessibile e completamente controllabile a distanza.

## 🚀 Il Progetto
Ho recuperato un **vecchio PC (Mac)** e l'ho trasformato in un server di registrazione dedicato. Il computer funge da "cervello" che riceve i flussi video dalle telecamere Tapo e li salva localmente sulla box.

### Caratteristiche principali:
- **Controllo Totale da iPhone**: Monitoraggio dello stato, avvio/blocco registrazioni e visualizzazione video direttamente dallo smartphone.
- **Accesso sicuro tramite Tailscale**: Utilizzo di Tailscale per creare una rete privata sicura e protetta.
- **Configurazione WAN**: Accesso remoto globale tramite portale dedicato per gestire il sistema da qualsiasi posto.
- **Smart Rotation & Watchdog**: Gestione automatica dello spazio su disco e sistema "cane da guardia" per garantire la stabilità 24/7.

---

## 📁 Struttura del Software
- `recorder.py`: Lo script principale che gestisce la connessione RTSP e il salvataggio dei flussi.
- `watchdog.py`: Monitora il processo principale e lo riavvia in caso di arresto improvviso.
- `rotator.py`: Gestisce la pulizia intelligente del disco (cancellazione file vecchi).
- `config.json`: File di configurazione centrale (IP, Username, Password).

## 🛠️ Setup Rapido

1. **Installa le dipendenze:**
   
