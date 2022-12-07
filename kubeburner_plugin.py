#!/usr/bin/env python3

import sys
import typing
from dataclasses import dataclass, field
from arcaflow_plugin_sdk import plugin, validation,schema
from typing import List,Dict
import subprocess
import datetime
import yaml
from kubeburner_schema import KubeBurnerInputParams, SuccessOutput, ErrorOutput, kube_burner_output_schema, kube_burner_input_schema



@plugin.step(
    id="kube-burner",
    name="Kube-Burner Workload",
    description="Kube-burner Workload which stresses the cluster by creating sleep pods. Creates a single namespace with a number of Deployments proportional to the calculated number of pod.",
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def RunKubeBurner(params: KubeBurnerInputParams ) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:

    print("==>> Running Kube Burner {} Workload ...".format(params.workload))
    
    try:
        cmd=['./kube-burner', 'ocp', str(params.workload), '--uuid='+str(params.uuid) ]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "error", ErrorOutput(error.returncode,"{} failed with return code {}:\n{}".format(error.cmd[0],error.returncode,error.output))

    output = process_out.decode("utf-8")

    print("==>> Kube Burner {} Workload complete!".format(params.workload))    
    return "success", SuccessOutput(params.uuid,output)



if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                # List your step functions here:
                RunKubeBurner,
            )
        )
    )