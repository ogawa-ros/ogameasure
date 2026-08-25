import logging
import threading
import time
from pathlib import Path

import gphoto2 as gp


class m100:
    def __init__(self):
        logging.basicConfig(
            format="%(levelname)s: %(name)s: %(message)s",
            level=logging.WARNING,
        )
        gp.check_result(gp.use_python_logging())

        self.camera = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_init(self.camera))
        self._lock = threading.RLock()
        self._closed = False

        print("Canon M100 connected")

    def capture(self, savepath):
        with self._lock:
            if self._closed:
                raise RuntimeError("Canon M100 camera session is closed")

            savepath = Path(savepath).expanduser()
            savepath.parent.mkdir(parents=True, exist_ok=True)

            print("Capturing image")

            file_path = gp.check_result(
                gp.gp_camera_capture(
                    self.camera,
                    gp.GP_CAPTURE_IMAGE,
                )
            )

            camera_file = gp.check_result(
                gp.gp_camera_file_get(
                    self.camera,
                    file_path.folder,
                    file_path.name,
                    gp.GP_FILE_TYPE_NORMAL,
                )
            )

            gp.check_result(gp.gp_file_save(camera_file, str(savepath)))

            # Drain the camera's post-capture events (e.g. file-added
            # notifications) so they don't linger and interfere with the next
            # capture on this same session.
            for _ in range(30):
                event_type, _ = gp.check_result(
                    gp.gp_camera_wait_for_event(
                        self.camera,
                        100,
                    )
                )
                if event_type == gp.GP_EVENT_TIMEOUT:
                    break

            print(f"Saved: {savepath}")
            return "Shooting completed"

    def close(self):
        with self._lock:
            if self._closed:
                return

            for _ in range(10):
                result = gp.gp_camera_exit(self.camera)

                if result >= gp.GP_OK:
                    self._closed = True
                    print("Canon M100 disconnected")
                    return

                if result != gp.GP_ERROR_CAMERA_BUSY:
                    gp.check_result(result)

                time.sleep(0.5)

            message = "Canon M100 camera remained busy during shutdown"
            raise RuntimeError(message)
