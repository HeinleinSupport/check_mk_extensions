#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def bake_updater_hostname(opsys, conf, conf_dir, plugins_dir):
    if conf:
        target_dir = plugins_dir
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copy2(cmk.utils.paths.local_agents_dir + "/plugins/updater_hostname", target_dir + "/updater_hostname")

bakery_info["updater_hostname"] = {
    "bake_function" : bake_updater_hostname,
    "os"            : [ "linux", ],
}
