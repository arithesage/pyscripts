#!/usr/bin/env python

import gradle
from stdio import print_va

version = gradle.version ()

print_va ("Gradle version $[0]", version)

