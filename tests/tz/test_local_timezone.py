from __future__ import annotations

import os
import sys

import pytest

from pendulum.tz.local_timezone import _get_unix_timezone
from pendulum.tz.local_timezone import _get_windows_timezone


@pytest.mark.skipif(
    sys.platform == "win32", reason="Test only available for UNIX systems"
)
def test_unix_symlink():
    # A ZONE setting in the target path of a symbolic linked localtime,
    # f ex systemd distributions
    local_path = os.path.join(os.path.split(__file__)[0], "..")
    tz = _get_unix_timezone(_root=os.path.join(local_path, "fixtures", "tz", "symlink"))

    assert tz.name == "Europe/Paris"


@pytest.mark.skipif(
    sys.platform == "win32", reason="Test only available for UNIX systems"
)
def test_unix_clock():
    # A ZONE setting in the target path of a symbolic linked localtime,
    # f ex systemd distributions
    local_path = os.path.join(os.path.split(__file__)[0], "..")
    tz = _get_unix_timezone(_root=os.path.join(local_path, "fixtures", "tz", "clock"))

    assert tz.name == "Europe/Zurich"


@pytest.mark.skipif(sys.platform != "win32", reason="Test only available for Windows")
def test_windows_timezone():
    timezone = _get_windows_timezone()

    assert timezone is not None


@pytest.mark.skipif(
    sys.platform == "win32", reason="Test only available for UNIX systems"
)
def test_unix_etc_timezone_dir():
    # Should not fail if `/etc/timezone` is a folder
    local_path = os.path.join(os.path.split(__file__)[0], "..")
    root_path = os.path.join(local_path, "fixtures", "tz", "timezone_dir")
    tz = _get_unix_timezone(_root=root_path)

    assert tz.name == "Europe/Paris"


@pytest.mark.skipif(
    sys.platform == "win32", reason="Test only available for UNIX systems"
)
def test_unix_localtime_regular_file_defaults_to_utc():
    # /etc/localtime as a bare copy of a zoneinfo file (no IANA key), as
    # found in minimal containers / Slurm jobs, used to yield a Timezone
    # with key=None, which crashed the Rust helpers (#989). It must now
    # fall through to the UTC default with a named key.
    import shutil
    import tempfile

    local_path = os.path.join(os.path.split(__file__)[0], "..")
    root_path = tempfile.mkdtemp()
    os.makedirs(os.path.join(root_path, "etc"), exist_ok=True)
    shutil.copy(
        os.path.join(local_path, "fixtures", "tz", "Paris"),
        os.path.join(root_path, "etc", "localtime"),
    )
    tz = _get_unix_timezone(_root=root_path)

    assert tz.key is not None
    assert tz.name == "UTC"
