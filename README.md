# Skyrim SKSE plugin example

This has been adapted from [this example](https://github.com/xanderdunn/skaar/releases/tag/plugin3). It has a simple build script to hopefully simplify the build process. It's also been tidied up a bit, it's clearer on the requirements, and it's been updated to use Visual Studio 2017.


## Requirements

- Skyrim\*
    - The Creation Kit\*
- [Python 3](https://www.python.org/downloads/) for the build script
- [Visual Studio 2017](https://visualstudio.microsoft.com/vs/express/)
    - "VC++ 2017 version 15.8 v14.15 latest v141 tools"
    - "Windows Universal CRT SDK"

__\*__ The build script is currently quite naive about all the different locations Skyrim and Visual Studio can be installed in, so you may need to edit some of the paths in it, particularly if you're not installing with Steam on a 64-bit machine.


## Getting Started

Ignore the `common` and `skse` directories, they are included from SKSE and are required for the plugin to compile. The directory of interest for your plugin is `plugin`. To compile, run:

```
python build.py
```

This will compile the plugin and the associated Papyrus script to the `Debug` directory. When you have finished developing and are ready to compile the final version, run the following:

```
python build.py release
```

Which will compile to the `Release` directory.

Otherwise follow [this guide](https://github.com/xanderdunn/skaar/wiki/SKSE%3A-Getting-Started).
