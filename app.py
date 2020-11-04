#!/usr/bin/env python3
import os

from aws_cdk import core

from openedx_native.openedx_native_stack import OpenedxNativeStack

dirname = os.path.dirname(__file__)
setup_script_path = os.path.join(dirname, "config.sh")
install_script_path = os.path.join(dirname, "edx.platform-install.sh")

app = core.App()

open_edx = OpenedxNativeStack(
    app,
    os.environ["APP_ID"],
    env={"region": os.environ["AWS_DEFAULT_REGION"]},
    setup_script_path=setup_script_path,
    install_script_path=install_script_path,
    ami_id=os.environ["AMI_ID"],
    key_name=os.environ["KEY_NAME"],
    ssh_allowed_ip=os.environ["LOCAL_IP"],
)

core.Tags.of(open_edx).add("AutoOff", "True")
core.Tags.of(open_edx).add("Owner", "Sofiane")

app.synth()
