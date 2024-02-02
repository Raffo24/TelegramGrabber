### Telegram Messages Grabber
## Introduzione
Questo script permette di raccogliere i dati delle chats di canali e gruppi telegram e salvarli in un database sqlite.
Quando lo script viene lanciato in modalità "LISTENING" automaticamente raccoglierà anche la cronologia degli ultimi 1000 messaggi inviati sul quel dato gruppo/canale.
Lo script è stato creato per scopi di threat intelligence.
# HOW TO USE
       LISTEN CHANNELS:
          `python3 grabberTelegram.py -l (or --listen) <app_id> <api_hash>`
       UPDATE CHANNELS:
           `python3 grabberTelegram.py -u (or --update) <channel_file_name>`
       ADD 1 CHANNEL:
           `python3 grabberTelegram.py --add-channel`
       PRINT all FOLLOWED CHANNELS:
           `python3 grabberTelegram.py --print-followed`
       PRINT all CHANNELS in DB:
           `python3 grabberTelegram.py --print-database`
       DELETE all CHANNELS from DB:
           `python3 grabberTelegram.py --delete-channels`
       DELETE all MESSAGES from DB:
           `python3 grabberTelegram.py --delete-messages`
      INSERT ID CANALI IN DB:
           `python3 grabberTelegram.py --add-ids <app_id> <api_hash>`
# ATTENZIONE!
Lo script scaricherà i messaggi e si metterà in ascolto solo dei canali presenti *nell'intersezione tra i channels presenti aggiunti al DB e i channels followati* con il nostro account telegram.
# Consigli
Si consiglia di analizzare il database con DB Browser.
DB browser permetter di effettuare query sui dati e esportarli come file csv.
I file una volta esportati possono essere utilizzati per effettuare ulteriori analisi statistiche.


