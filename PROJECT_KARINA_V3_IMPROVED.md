# Karina V3 Improved Spectrum Project

Base reale: armel/uv-k1-k5v3-firmware-custom.

Obiettivo:
- firmware V3 compilabile dal sorgente reale;
- mantenere la gestione tastiera originale;
- non introdurre il precedente problema "press #";
- migliorare la leggibilità dello Spectrum;
- frequenza/etichette Spectrum più pesanti e leggibili;
- mantenere posizione e dimensioni del framebuffer per ridurre il rischio di regressioni.

La modifica visuale è isolata in App/app/spectrum.c:
1. frequenza principale dello Spectrum usa il font small bold già presente nel progetto;
2. numeri/lettere compatti dello Spectrum ricevono un rinforzo orizzontale di 1 pixel;
3. nessuna modifica alla scansione tasti, bootloader, radio state machine o gestione EEPROM.

Il progetto contiene anche una GitHub Action che clona il sorgente V3 reale, applica la modifica e produce il BIN Fusion come artifact.
