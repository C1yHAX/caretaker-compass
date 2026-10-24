# Caretaker Compass 1.0.0 – Erstrelease

Ein zusätzlicher Kompass für **The Last Caretaker**, der zu Fuß oben mittig
die Blickrichtung und Gradzahl anzeigt. Eigener Lua-Code verwaltet die
Kompassanzeige der aktuellen Spielversion.

## Funktionen

- Kompassband und Gradzahl ohne Freischaltung oder zusätzliche Taste.
- Direkt an den lokalen Spieler gebunden; kein bestimmtes Boot als Voraussetzung.
- Beim Steuern eines Boots übernimmt standardmäßig der vorhandene Bootskompass.
- Automatisches Ausblenden in Menüs, Dialogen und bei verborgenem Spiel-HUD.
- Wiederherstellung nach Weltwechseln und Entfernen der Anzeige ohne Doppelungen.
- Einstellbare Breite, Höhe, oberer Abstand und Deckkraft in `Scripts/config.lua`.
- Keine Änderungen an Kabel- und Interaktionssteuerung oder Spielstandsformat.

Die Blickrichtung wird von der Spiel-Engine aktualisiert. Die zusätzliche
Lua-Verwaltung prüft den Zustand viermal pro Sekunde und nutzt gespeicherte
Objektreferenzen.

## Installation

1. Das Spiel schließen.
2. Eine funktionierende UE4SS-Installation mit `LoopInGameThreadWithDelay`
   verwenden. Im Caretaker-Modpack ist sie bereits enthalten. Getestet mit
   UE4SS **v3.0.1-1125-g527a483b** und Spielbuild **0.10.0.653173**.
3. Eine vorherige zusätzliche Kompass-Mod entfernen. Beim alten Compass-Paket
   für Update 5.5 die drei Dateien `Compass.pak`, `Compass.ucas`, `Compass.utoc`
   aus dessen Ordner unter `Voyage/Content/Paks/~mods` entfernen.
4. **`Caretaker-Compass-1.0.0.zip`** in den Spielinstallationsordner entpacken.
   Danach muss folgender Pfad vorhanden sein:
   `Voyage/Binaries/Win64/ue4ss/Mods/CaretakerCompass/Scripts/main.lua`.
5. Das Spiel starten. Der Kompass erscheint automatisch zu Fuß.

Das vollständige Caretaker-Modpack enthält diese Mod bereits. Bei einer
vorhandenen Modpack-Installation ist keine zweite Kopie erforderlich.

Nach Änderungen an `Scripts/config.lua` das Spiel neu starten. Zum Entfernen
der Mod bei geschlossenem Spiel ausschließlich den Ordner `CaretakerCompass`
unter `ue4ss/Mods` löschen.

## Download und Prüfung

Das Installations-ZIP enthält ausschließlich `main.lua`, `config.lua` und
`enabled.txt` in der oben beschriebenen Ordnerstruktur. Beschreibung,
Installationsanleitung, Entwicklungstools und Prüfberichte bleiben außerhalb
des ZIPs. `SHA256SUMS.txt` wird als separater Download bereitgestellt.

Die von GitHub/GitLab automatisch erzeugten Quellcodearchive sind kein
Installationspaket. Für das Spiel die benannte Mod-ZIP verwenden.

Im laufenden Spiel geprüft: Himmelsrichtungen, Übergang über Norden,
Bootswechsel, Menüs, Wiederherstellung und vollständiges Entladen/Neuladen der
Welt. Die Anzeige wurde bei 1280×720 und 1920×1080 kontrolliert. Zwölf
automatisierte Lua-Lebenszyklustests sind erfolgreich. Die vorhandenen
Spielstände blieben unverändert. Details stehen in `VERIFICATION.md` im Projekt.

Veröffentlichung auf beiden Plattformen mit identischem Download:

- [GitHub-Projekt](https://github.com/C1yHAX/caretaker-compass)
- [GitLab-Projekt](https://gitlab.com/c0d1ngf1eber/caretaker-compass)
