# pyric
Reduced input compiler for simple pyunrealsdk extensions - one cpp file to one pyd file.

Pyric is essentially just a wrapper around CMake, it sets up a simple project linking against the
required libraries, then copies in your individual source files when it's time to compile them. It
relies on `file(GLOB ... CONFIGURE_DEPENDS)` to detect new source files - you must use a generator
supporting it.

## External Requirements
There are a few external requirements to run pyric - though you'll likely already have them if
developing for the sdk.
- git must be on your path.
- CMake must be on your path.
- CMake must be able to find a compatible generator and compiler.
- You must have permission to create symlinks - on Windows either enable dev mode or run as admin.

## Installation
The recommended way to install is from the git url, via pipx.
```sh
pipx install git+ssh://git@github.com:bl-sdk/pyunrealsdk.git
```

## Usage
### Initalization
First, initalize the CMake project. There are two ways pyric gets the copy of pyunrealsdk to link
against:

1. Automatically download the latest version from git - this is the default behaviour.
   ```sh
   pyric init --py-version 3.11.4 msvc-ue4-x64
   ```
   When doing this, it also downloads the python dev libraries. This defaults to the same version as
   that of the python intepreter running it, or you can use the `--py-version` arg to specify an
   exact version.

2. Symlink it from another folder - useful when doing dev work.
   ```sh
   pyric init --pyunrealsdk /path/to/pyunrealsdk msvc-ue4-x64
   ```
   You can also point this at any other pyric project dir to symlink the install it uses.

You may re-init a directory to change which preset it is built with, or to change CMake settings.
This will *not* fetch a new version of pyunrealsdk, it will keep whatever's already in the folder.

### Building
After initalization, you can start building.
```sh
pyric build example.cpp
```
This will build an `example.pyd`, and copy it back right next to the source file.

If required, you may specify multiple files.
```sh
pyric build example.cpp mylib/lib.h mylib/lib.cpp
```

Note that directories are flattened when the files are copied for building - meaning in this case
`example.cpp` should contain:
```c
#include "lib.h"
```
