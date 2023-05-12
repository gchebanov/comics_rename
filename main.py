import sys
from zipfile import ZipFile
from pathlib import Path
from collections import Counter

REPLACE = {'.rar': '.cbr', '.zip': '.cbz', '.7z': '.cb7'}


def process_comic(path: Path, lf: list[Path]):
    if not lf:
        print(f'SKIP {path=} reason=no-files')
        return
    c = Counter((e.suffix for e in lf))
    if c.keys() < {'.png', '.jpg', '.jpeg'}:
        print(f'convert to cbz {path=} {c!r}')
        name = path.with_name(path.name + '.cbz')
        assert not name.exists()
        with ZipFile(name, 'w') as fz:
            for e in lf:
                fz.write(e)
                e.unlink()
        path.rmdir()
        return
    if c.keys() & {'.png', '.jpg', '.jpeg'}:
        print(f'WARNING {path=} {c!r}')
        return
    ok, skip = 0, 0
    for e in lf:
        if ns := REPLACE.get(e.suffix):
            ne = e.with_suffix(ns)
            e.rename(ne)
            ok += 1
        else:
            skip += 1
    print(f'Done {path=} {ok=} {skip=}')


def main(path: Path) -> None:
    if not path.exists():
        return
    if not path.is_dir():
        return
    lf, ld = [], []
    for e in path.iterdir():
        (ld if e.is_dir() else lf).append(e)
    if not ld:
        process_comic(path, lf)
    for d in ld:
        main(d)


if __name__ == '__main__':
    main(Path(r'E:\\Comics\\'))

