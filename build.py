import os
import shlex
import shutil
import subprocess
import zipfile

from pathlib import Path


def maturin(*args):
    subprocess.call(["maturin", *list(args)])


def _build():
    build_dir = Path(__file__).parent.joinpath("build")
    build_dir.mkdir(parents=True, exist_ok=True)

    wheels_dir = Path(__file__).parent.joinpath("target/wheels")
    if wheels_dir.exists():
        shutil.rmtree(wheels_dir)

    cargo_args = []
    if os.getenv("MATURIN_BUILD_ARGS"):
        cargo_args = shlex.split(os.getenv("MATURIN_BUILD_ARGS", ""))

    maturin("build", "-r", *cargo_args)

    # We won't use the wheel built by maturin directly since
    # we want Poetry to build it but we need to retrieve the
    # compiled extensions from the maturin wheel.
    wheel = list(wheels_dir.glob("*.whl"))[0]
    with zipfile.ZipFile(wheel.as_posix()) as whl:
        whl.extractall(wheels_dir.as_posix())

        for extension in wheels_dir.rglob("**/*.so"):
            shutil.copyfile(extension, Path(__file__).parent.joinpath(extension.name))

    shutil.rmtree(wheels_dir)


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    try:
        _build()
    except Exception as e:
        print(
            "  Unable to build Rust extensions, "
            "Pendulum will use the pure python version of the extensions."
        )
        print(e)


if __name__ == "__main__":
    build({})
