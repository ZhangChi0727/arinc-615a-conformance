"""Build hook that carries source-controlled JSON into the offline wheel."""

from __future__ import annotations

from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


_CONTROLLED_FILES = (
    "cltav_development_contracts.json",
    "cltav_development_contracts.schema.json",
    "cltav_offline_intake_evidence.schema.json",
)


class build_py(_build_py):
    """Copy exact source authority bytes into the package build directory."""

    def run(self) -> None:
        super().run()
        root = Path(__file__).resolve().parent
        source_root = root / "configs" / "engineering"
        target = Path(self.build_lib) / "cltav_offline" / "resources"
        target.mkdir(parents=True, exist_ok=True)
        for filename in _CONTROLLED_FILES:
            source = source_root / filename
            if not source.is_file():
                raise RuntimeError(f"controlled source resource is unavailable: {source}")
            (target / filename).write_bytes(source.read_bytes())


setup(cmdclass={"build_py": build_py})
