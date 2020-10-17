#!/usr/bin/env python3

from aws_cdk import core

from openedx_native.openedx_native_stack import OpenedxNativeStack


app = core.App()
OpenedxNativeStack(app, "openedx-native")

app.synth()
