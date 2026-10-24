"""Build and verify the runtime-only Caretaker Compass 1.0.0 release."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = 'Caretaker-Compass-1.0.0.zip'
PREFIX = 'Voyage/Binaries/Win64/ue4ss/Mods/CaretakerCompass/'
EXPECTED = {PREFIX + p for p in ('enabled.txt', 'Scripts/main.lua', 'Scripts/config.lua')}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    files = {p.relative_to(ROOT).as_posix(): p.read_bytes()
             for p in (ROOT/'Voyage').rglob('*') if p.is_file()}
    assert set(files) == EXPECTED, 'Unexpected runtime file set'
    for name, data in files.items():
        assert '..' not in PurePosixPath(name).parts
        text = data.decode('utf-8')
        for private in ('C:\\Users\\', 'C:/Users/', 'E:\\Program Files',
                        'E:/Program Files', 'ghp_', 'glpat-', 'gho_'):
            assert private not in text, f'Private marker in {name}'
    rows = [dict(path=n, bytes=len(d), sha256=digest(d)) for n, d in sorted(files.items())]
    (ROOT/'Dateien.json').write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')
    out = ROOT/'dist'
    out.mkdir(exist_ok=True)
    target = out/ARCHIVE
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 24, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compresslevel=9)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None and set(archive.namelist()) == EXPECTED
        for row in rows:
            assert digest(archive.read(row['path'])) == row['sha256']
    result = dict(file=ARCHIVE, bytes=target.stat().st_size,
                  sha256=digest(target.read_bytes()), runtimeFiles=len(files), runtimeOnly=True)
    (out/'SHA256SUMS.txt').write_text(result['sha256']+'  '+ARCHIVE+'\n', encoding='ascii')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
