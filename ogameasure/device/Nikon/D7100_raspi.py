from __future__ import print_function
import logging
from pathlib import Path
import gphoto2 as gp


class d7100(object):
    def capture(self, savepath):
        savedir = savepath

        logging.basicConfig(
            format="%(levelname)s: %(name)s: %(message)s", level=logging.WARNING
        )
        gp.check_result(gp.use_python_logging())

        camera = gp.check_result(gp.gp_camera_new())
        context = gp.gp_context_new()

        try:
            gp.check_result(gp.gp_camera_init(camera, context))

            # Nikon では RAM 保存のほうが通りやすい
            config = gp.check_result(gp.gp_camera_get_config(camera, context))
            capture_target = gp.check_result(
                gp.gp_widget_get_child_by_name(config, "capturetarget")
            )
            gp.check_result(gp.gp_widget_set_value(capture_target, "Internal RAM"))
            gp.check_result(gp.gp_camera_set_config(camera, config, context))

            print("Capturing image")
            file_path = gp.check_result(
                gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE, context)
            )

            # Nikon は capture 直後に file_get すると不安定なことがあるので少し待つ
            # FILE_ADDED イベントが来たらそのファイルを使う
            downloaded_path = file_path
            for _ in range(20):
                event_type, event_data = gp.check_result(
                    gp.gp_camera_wait_for_event(camera, 500, context)
                )
                if event_type == gp.GP_EVENT_FILE_ADDED:
                    downloaded_path = event_data
                    break
                if event_type == gp.GP_EVENT_TIMEOUT:
                    continue

            camera_file = gp.check_result(
                gp.gp_camera_file_get(
                    camera,
                    downloaded_path.folder,
                    downloaded_path.name,
                    gp.GP_FILE_TYPE_NORMAL,
                    context,
                )
            )

            gp.check_result(gp.gp_file_save(camera_file, savedir))

            return "Shooting completed"

        finally:
            gp.check_result(gp.gp_camera_exit(camera, context))
