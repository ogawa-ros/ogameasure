import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

MODULE_PATH = Path(__file__).parents[1]
MODULE_PATH /= "ogameasure/device/Canon/M100_raspi.py"


class FakeGPhoto2:
    GP_OK = 0
    GP_ERROR_CAMERA_BUSY = -110
    GP_CAPTURE_IMAGE = 1
    GP_FILE_TYPE_NORMAL = 2
    GP_EVENT_TIMEOUT = 3

    def __init__(self, exit_results=None):
        self.camera = object()
        self.exit_results = iter(exit_results or [self.GP_OK])
        self.exit_calls = 0
        self.capture_calls = 0

    @staticmethod
    def check_result(result):
        if isinstance(result, int) and result < 0:
            raise RuntimeError(f"gphoto2 error: {result}")
        return result

    @staticmethod
    def use_python_logging():
        return 0

    def gp_camera_new(self):
        return self.camera

    @staticmethod
    def gp_camera_init(camera):
        return 0

    def gp_camera_capture(self, camera, capture_type):
        self.capture_calls += 1
        return SimpleNamespace(folder="/store", name="image.jpg")

    @staticmethod
    def gp_camera_file_get(camera, folder, name, file_type):
        return object()

    @staticmethod
    def gp_file_save(camera_file, savepath):
        return 0

    def gp_camera_wait_for_event(self, camera, timeout_ms):
        return self.GP_EVENT_TIMEOUT, None

    def gp_camera_exit(self, camera):
        self.exit_calls += 1
        return next(self.exit_results)


def load_m100(monkeypatch, fake_gp):
    monkeypatch.setitem(sys.modules, "gphoto2", fake_gp)
    module_name = "m100_under_test"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module.time, "sleep", lambda _: None)
    return module.m100


def test_close_is_idempotent(monkeypatch):
    fake_gp = FakeGPhoto2()
    camera = load_m100(monkeypatch, fake_gp)()

    camera.close()
    camera.close()

    assert fake_gp.exit_calls == 1


def test_capture_after_close_fails_without_using_camera(monkeypatch, tmp_path):
    fake_gp = FakeGPhoto2()
    camera = load_m100(monkeypatch, fake_gp)()
    camera.close()

    with pytest.raises(RuntimeError, match="session is closed"):
        camera.capture(tmp_path / "image.jpg")

    assert fake_gp.capture_calls == 0


def test_close_retries_busy_then_succeeds(monkeypatch):
    busy_then_ok = [FakeGPhoto2.GP_ERROR_CAMERA_BUSY, FakeGPhoto2.GP_OK]
    fake_gp = FakeGPhoto2(busy_then_ok)
    camera = load_m100(monkeypatch, fake_gp)()

    camera.close()

    assert fake_gp.exit_calls == 2


def test_close_raises_when_camera_stays_busy(monkeypatch):
    fake_gp = FakeGPhoto2([FakeGPhoto2.GP_ERROR_CAMERA_BUSY] * 10)
    camera = load_m100(monkeypatch, fake_gp)()

    with pytest.raises(RuntimeError, match="remained busy"):
        camera.close()

    assert fake_gp.exit_calls == 10
    assert camera._closed is False
