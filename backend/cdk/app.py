#!/usr/bin/env python3
import aws_cdk as cdk
from stack import CardyStack

app = cdk.App()
CardyStack(app, "cardy-backend")
app.synth()
