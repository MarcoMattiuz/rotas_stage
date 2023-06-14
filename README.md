# TODO List
- risolvere: 'Couldn't read data from stream: 'nn' (X_LINK_ERROR)'
- pm2 config
- decode nn results onboard: https://docs.luxonis.com/projects/api/en/latest/components/nodes/mobilenet_detection_network/
- adc esterno
- scheda
- gpio cleanup e i2c reset
- aggiungere retry button che invia richiesta di reinizializzazione della oak-d
- stile mappa https://leaflet-extras.github.io/leaflet-providers/preview/
- far funzionare il feed della camera (con h264: https://www.codeinsideout.com/blog/pi/stream-picamera-h264/#create-a-webpage, https://docs.luxonis.com/projects/api/en/latest/tutorials/low-latency/)


## Comandi bluetoothctl
Entra sulla console di bluetoothctl

`bluetoothctl`

Se la cassa è connessa dovrebbe comparire un prompt simile:

`[JBL GO]# `

Altrimenti si può connettere in questo modo. Rimuovere il dispositivo:

`[bluetooth]# remove 30:C0:1B:C8:DF:4B`

Rieffettuare il pairing:

`[bluetooth]# pair 30:C0:1B:C8:DF:4B`

Connessione:

`[bluetooth]# connect 30:C0:1B:C8:DF:4B`
