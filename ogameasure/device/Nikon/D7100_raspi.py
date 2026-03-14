from __future__ import print_function

import logging
from pathlib import Path

import gphoto2 as gp


class D7100(object):
    def _get_camera(self):
        camera_list = list(gp.Camera.autodetect())
        if not camera_list:
            raise RuntimeError("No camera detected by python-gphoto2")

        name, addr = camera_list[0]

        camera = gp.Camera()

        port_info_list = gp.PortInfoList()
        port_info_list.load()
        idx = port_info_list.lookup_path(addr)
        camera.set_port_info(port_info_list[idx])

        abilities_list = gp.CameraAbilitiesList()
        abilities_list.load()
        idx = abilities_list.lookup_model(name)
        camera.set_abilities(abilities_list[idx])

        return camera

    def capture(self, savepath):
        savepath = str(Path(savepath).expanduser())
        Path(savepath).parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            format="%(levelname)s: %(name)s: %(message)s",
            level=logging.WARNING,
        )
        gp.check_result(gp.use_python_logging())

        context = gp.Context()
        camera = self._get_camera()

        try:
            camera.init(context)

            config = camera.get_config(context)
            capture_target = config.get_child_by_name("capturetarget")
            capture_target.set_value("Internal RAM")
            camera.set_config(config, context)

            print("Capturing image")
            file_path = camera.capture(gp.GP_CAPTURE_IMAGE, context)

            downloaded_path = file_path
            for _ in range(20):
                event_type, event_data = camera.wait_for_event(500, context)
                if event_type == gp.GP_EVENT_FILE_ADDED:
                    downloaded_path = event_data
                    break
                if event_type == gp.GP_EVENT_TIMEOUT:
                    continue

            camera_file = camera.file_get(
                downloaded_path.folder,
                downloaded_path.name,
                gp.GP_FILE_TYPE_NORMAL,
            )

            camera_file.save(savepath)

            return "Shooting completed"

        finally:
            try:
                camera.exit(context)
            except gp.GPhoto2Error:
                pass
