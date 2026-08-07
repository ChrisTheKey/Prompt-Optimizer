# Wanddesigns – Elbisch-kalligrafischer Stil

10 originale Ziermuster mit hellen, fließenden Linien auf schwarzem Hintergrund,
im Look elbischer Kalligrafie. Als **Vektorgrafik (SVG)** – verlustfrei skalierbar,
ideal zum **Nachzeichnen**, **Projizieren** oder **direkten Übertragen auf die Wand**.

> Hinweis: Alle Glyphen und Ornamente sind **frei erfunden** und rein dekorativ.
> Es werden **keine echten Tengwar-/Tolkien-Schriftzeichen** oder geschützten
> Texte verwendet.

## Ansehen

Öffne **`index.html`** im Browser (Doppelklick) – zeigt alle 10 Designs als Galerie.
Einzelne SVGs liegen in `svg/` und lassen sich im Browser beliebig zoomen.

## Die 10 Versionen

| Nr. | Motiv           | Eignung                                   |
|-----|-----------------|-------------------------------------------|
| 01  | Schriftbänder   | Fries / horizontale Bordüre über Türen    |
| 02  | Inschrift-Ring  | rundes Zentralmotiv, z. B. über dem Bett  |
| 03  | Ranken-Bordüre  | seitliche vertikale Rahmung               |
| 04  | Lebensbaum      | großes Einzelmotiv an einer Akzentwand    |
| 05  | Eckornamente    | vier Ecken eines Rahmens / Spiegels       |
| 06  | Flächenmuster   | ganzflächige, wiederholende Textur        |
| 07  | Torbogen        | Portal-/Türrahmung                        |
| 08  | Sternenkarte    | verstreute Sterne, Decke oder Nische      |
| 09  | Flechtband      | durchlaufendes Band / Sockelleiste        |
| 10  | Zentral-Emblem  | großes Prunkstück als Blickfang           |

## Auf die Wand übertragen – drei Wege

1. **Projizieren (am genauesten):** SVG im Browser (oder als PDF exportiert)
   mit einem Beamer an die Wand werfen, in gewünschter Größe scharfstellen,
   Linien mit Kreide-/Lackstift nachfahren.
2. **Rastermethode:** Motiv und Wand in gleich viele Felder (z. B. 10×10) einteilen,
   Feld für Feld übertragen.
3. **Ausdruck als Schablone:** SVG als große PDF-Kachel (mehrere A4/A3-Seiten)
   drucken, ausschneiden, an der Wand anlegen und durchpausen.

Weißer/silberner Stift auf schwarz gestrichener Wand ergibt den stärksten Effekt;
die goldenen Punkte (Akzente) mit Gold-Marker setzen.

## Selbst neu generieren / anpassen

```bash
python3 generate.py      # schreibt svg/wanddesign-01.svg … -10.svg neu
```

Farben (Linie/Akzent/Hintergrund), Format und Motive lassen sich oben in
`generate.py` (Konstanten `INK`, `GOLD`, `BG`, `W`, `H` sowie die `design_XX`-Funktionen)
anpassen.

## Empfohlene freie Ressourcen (extern, nicht enthalten)

Zum Vertiefen/Erweitern des Stils – bewusst **verlinkt** statt einkopiert,
um Lizenzen der jeweiligen Projekte zu respektieren:

- **Tengwar Annatar / Tengwar Telcontar** – frei nutzbare Schriftarten im elbischen Stil
  (für eigene, selbst gewählte Wörter). Suche nach „Tengwar Telcontar SIL/Google Noto".
- **Glaemscribe** (Open Source) – Transkriptions-Werkzeug für elbische Schriftstile.
- **Inkscape** (Open Source) – zum Bearbeiten/Vergrößern der SVGs und PDF-Kachel-Export.
- **potrace** (Open Source) – falls du eigene Skizzen in saubere Vektorlinien wandeln willst.
