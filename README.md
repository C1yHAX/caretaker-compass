# Caretaker Compass 1.0.0

Eine eigene Kompass-Mod für **The Last Caretaker**, entwickelt für Spielbuild
**0.10.0.653173**. Sie ergänzt zu Fuß einen Kompass oben in der Bildschirmmitte.
Kompassband und Gradzahl stammen aus der aktuellen Spielversion; die Mod übernimmt
deren Anzeige und Lebenszyklus mit eigenem Lua-Code.

## Download

- [GitHub: Release 1.0.0](https://github.com/C1yHAX/caretaker-compass/releases/tag/v1.0.0)
- [GitLab: Release 1.0.0](https://gitlab.com/c0d1ngf1eber/caretaker-compass/-/releases/v1.0.0)

Für die Installation die Datei **`Caretaker-Compass-1.0.0.zip`** herunterladen.
Sie enthält nur die drei Mod-Dateien im richtigen Installationspfad. Die automatisch
von der Plattform angebotenen Quellcodearchive sind kein Installationspaket.
Eine separate `SHA256SUMS.txt` dient zum Prüfen des Downloads.

## Funktionen

- Blickrichtung und Gradzahl mit der nativen Kompassberechnung des Spiels.
- Sofort verfügbar, sobald der lokale Spieler in der Welt bereit ist. Kein
  vorausgesetztes Boot und keine Suche nach einem bestimmten Bootsmodell.
- Beim Steuern eines Boots wird die Zusatzanzeige ausgeblendet. Die Bootsanzeige
  des Spiels bleibt zuständig. Dies lässt sich in der Konfiguration ändern.
- Ausblenden bei Menüs, Dialogen, Intro und ausgeblendetem Spiel-HUD; automatische
  Rückkehr nach dem Schließen.
- Wiederherstellung nach Entfernen der Anzeige und Weltwechseln; eigene verwaiste
  Anzeigen werden beim Neuladen aufgeräumt.
- Keine zusätzlichen Tasten und keine Änderung an Kabel- oder Interaktionsaktionen.
- Breite, Abstand vom oberen Rand, Höhe des Bands und Deckkraft konfigurierbar.

Die Mod benötigt keinen eigenen pro Bild ausgeführten Lua-Callback. Der vorhandene
Kompass wird von der Engine aktualisiert. Die Lua-Verwaltung prüft den Zustand viermal
pro Sekunde und verwendet zwischengespeicherte Referenzen. Ein vollständiger Scan
nach eigenen alten Kompass-Widgets findet nur einmal beim Initialisieren statt.
Die tatsächliche Bildrate hängt vom System und dem übrigen Modpack ab.

## Installation

1. Das Spiel schließen.
2. UE4SS mit `LoopInGameThreadWithDelay` installieren, sofern noch nicht vorhanden.
   Im Caretaker-Modpack ist diese Voraussetzung bereits enthalten. Getestete
   Laufzeit: UE4SS v3.0.1-1125-g527a483b.
3. Eine bisherige zusätzliche Kompass-Mod vollständig entfernen. Für das alte
   Paket „Compass – for game update 5.5“ betrifft das `Compass.pak`,
   `Compass.ucas` und `Compass.utoc` im entsprechenden Unterordner von
   `Voyage/Content/Paks/~mods`. Nicht beide Kompass-Mods parallel installieren.
4. `Caretaker-Compass-1.0.0.zip` in den Spielinstallationsordner entpacken, sodass
   `Voyage/Binaries/Win64/ue4ss/Mods/CaretakerCompass/Scripts/main.lua` entsteht.
5. Das Spiel starten. Es ist keine Freischaltung oder Taste erforderlich.

Einstellungen stehen in `Scripts/config.lua` neben der `main.lua`. Nach Änderungen
das Spiel neu starten. `HideWhileSteering = false` lässt den zusätzlichen Kompass
auch beim Steuern eines Boots sichtbar; standardmäßig wird eine doppelte Anzeige
vermieden. `Enabled = false` schaltet die Anzeige ab.

Zur Deinstallation bei geschlossenem Spiel ausschließlich den Ordner
`CaretakerCompass` aus `ue4ss/Mods` entfernen. Es werden keine Gegenstände,
Fähigkeiten oder Mod-Daten in Spielständen gespeichert.

## Eigenständige Umsetzung

Das Paket enthält eigenen Lua-Code und verwendet die zur Laufzeit vorhandene
Spielanzeige. Es enthält keine kopierten Blueprint-Pakete oder sonstige Dateien
der früheren Compass-Mod. Es überschreibt keine Originaldateien des Spiels.

Die frühere Mod war für Update 5.5 bezeichnet. Die statische Prüfung fand keinen
eindeutigen aktuellen Absturzfehler. Die neue Fassung ersetzt insbesondere deren
Bindung an ein zuerst gefundenes Barge-Boot durch die Bindung an den lokalen Spieler.

## Entwicklung und Paketinhalt

`tools/package_release.py` baut das deterministische ZIP und prüft Dateiliste und
SHA-256 jeder Datei. `tests/test_lifecycle.py` führt die Lua-Lebenszyklustests mit
`lupa.lua54` aus. Testberichte bleiben außerhalb der Downloads.

Die ZIP enthält ausschließlich drei Laufzeitdateien: `main.lua`, `config.lua`
und `enabled.txt`, jeweils unter dem Installationspfad. Beschreibung, Quelltests,
Prüfberichte und Prüfsummen werden nicht in das ZIP gepackt.
