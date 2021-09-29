#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def bake_xe_cpu_util(opsys, conf, conf_dir, plugins_dir):
    shutil.copy2(cmk.utils.paths.local_agents_dir + "/plugins/xe_cpu_util", plugins_dir + "/xe_cpu_util")

bakery_info["xe_cpu_util"] = {
    "bake_function" : bake_xe_cpu_util,
    "os"            : [ "linux", ],
}
