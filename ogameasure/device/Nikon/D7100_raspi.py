from __future__ import annotations

import subprocess
from pathlib import Path


class d7100(object):
    def capture(self, savepath):
        savepath = str(Path(savepath).expanduser().resolve())
        Path(savepath).parent.mkdir(parents=True, exist_ok=True)

        cmds = [
            ["gphoto2", "--set-config", "capturetarget=sdram"],
            ["gphoto2", "--capture-image-and-download", "--filename", savepath],
        ]

        for cmd in cmds:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if proc.returncode != 0:
                raise RuntimeError(
                    f"gphoto2 failed: {' '.join(cmd)}\n"
                    f"stdout:\n{proc.stdout}\n"
                    f"stderr:\n{proc.stderr}"
                )

        return "Shooting completed"
