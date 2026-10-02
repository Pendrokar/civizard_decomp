# Civizard: Majutsu no Keifu matching decompilation

Matching decompilation of the Japanese PlayStation release **SLPS-00618** (*Civizard: Majutsu no Keifu*, Elf, 1996).

This repository is the splat / objdiff project intended for [decomp.dev](https://decomp.dev/). It is not the Windows PSXRecomp port. Source is written to compile back to the original MIPS binaries with a PlayStation toolchain (Psy-Q / MASPSX), not to a native `.exe`.

| File | Role | Load | Entry | Text | SHA-1 |
| --- | --- | --- | --- | --- | --- |
| `disc/SLPS_006.18` | Boot EXE from `SYSTEM.CNF` | `0x80150000` | `0x80150B4C` | `0x20000` | `0fc5782013abead42b66d1159992de7e82d3dd58` |
| `disc/WIZARDS.EXE` | Main program loaded by the boot EXE | `0x80010000` | `0x8007C978` | `0x14D800` | `d18ddc594f31c0534206913da229cf3cf9896301` |

Do not commit those files. Place a legal dumpsxiso extract in `disc/` (or keep this folder next to the recompiler tree so `configure.py --link-disc` can copy `../disks/us/SLPS_006.18` and `../disks/us/WIZARDS.EXE`).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
make extract
```

On Windows PowerShell, from this directory:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3 -m pip install -r requirements.txt
py -3 configure.py --link-disc
py -3 -m splat split config/slps_006.18.yaml --disassemble-all --make-full-disasm-for-code
py -3 -m splat split config/wizards.exe.yaml --disassemble-all --make-full-disasm-for-code
```

`make extract` splits both executables. Matching C lives in `src/slps_006.18` and `src/wizards` once functions move out of `asm/`.

## decomp.dev

Layout follows listed PS1 projects (Silent Hill, Xenogears): splat YAML under `config/`, GitHub Actions artifact named `VERSION_report`.

1. Push this tree as its own GitHub repository (default branch `main`).
2. Add repository secrets `FILE_URL` (boot EXE) and `FILE_URL_WIZARDS` (main EXE).
3. Confirm `.github/workflows/progress.yml` uploads `SLPS_006.18_report` and `WIZARDS.EXE_report` from `main`.
4. A repository admin adds the project at [https://decomp.dev/manage/new](https://decomp.dev/manage/new).
5. Install the [decomp.dev GitHub app](https://github.com/apps/decomp-dev).

A matching `ninja` / MASPSX rebuild is the next step after the first splat split. Until objdiff has base and target objects, CI writes a zero-percent report so the artifact name is in place.

## License

Original work in this repository is [CC0 1.0](LICENSE). The game itself is not redistributed.
