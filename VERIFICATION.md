# Verification: Caretaker Compass 1.0.0

Tested on 2026-10-24 with The Last Caretaker 0.10.0.653173 and
UE4SS v3.0.1-1125-g527a483b. Functional tests ran in fresh isolated `UserDir`
profiles with the existing installed modpack. The normal saves were not loaded.

The installed release was launched by UE4SS from its regular mod directory.

## Native game tests

- One owned compass widget, with working direction strip and numeric heading.
- Controller yaw 0/90/180/270: displayed headings 90/180/270/359, following the
  game's coordinate system and its native rounding at north.
- Actual north crossing: yaw 269/271 produces headings 359/1.
- Menu cursor and HUD visibility: hide and recover without adding another widget.
- Real native overlay opened and closed: compass hidden and restored.
- Possessed an existing boat, then returned to the player character: extra compass
  hidden on the boat and visible again on foot.
- Removed the widget from the viewport: exactly one replacement created.
- Final release layout visually inspected at 1280×720 and 1920×1080, including
  resizing during play. Center anchor and readable degree text preserved.
- Left the gameplay world for the initial menu: zero own widgets remained.
  Re-entered gameplay: exactly one visible widget, owned by the new controller.
- Final test concluded with `FINAL_RELEASE_PASS`, then closed the game normally.

Two issues found during development were corrected before packaging: an unreflected
cinematic-state member was incorrectly truthy in UE4SS, and setting viewport
position reset the center anchors. The released code follows HUD visibility and
sets anchors after the position/size calls.

## Automated and deployment checks

- Twelve Lua lifecycle scenarios passed, including reload, pawn/world changes,
  menu suppression, viewport removal, and cleanup.
- All six existing save files retained their original SHA-256 hashes.
- All 63 pre-existing files under the installed UE4SS Mods directory retained
  their original SHA-256 hashes.
- Old Compass pak/ucas/utoc files removed from the active game installation and
  the full modpack. A recovery copy remains outside the game directory.
- Private test helper removed. No test scripts, profiles or saves enter a ZIP.
- Standalone package: three runtime files. Full pack: 109 runtime files, with all
  106 unrelated members byte-for-byte unchanged.
- Every archive member verified against its expected content. Installed compass
  runtime matches the standalone archive.

These checks cover the tested build and the installed modpack. They are not a
long-duration performance benchmark or a guarantee of future game compatibility.
