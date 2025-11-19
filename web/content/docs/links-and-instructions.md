+++
title = "Links and Instructions"
weight = 3
keywords = ['treetime', 'tree time', 'data manager', 'principles', 'get treetime', 'run treetime', 'source code', 'bugs', 'licensing']
+++

## Documentation ##

[TreeTime Documentation](https://treetime-data-manager.readthedocs.io/en/latest) on readthedocs.io is constantly being kept up to date.

## Get TreeTime ##

{{% tabs %}}
{{% tab "Python / PyPi" %}}
{{% steps %}}
1. Install python3
2. Install PyQt6 -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type:
    `pip install PyQt6`
3. Install _TreeTime_ -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type:
    `pip install treetime`
{{% /steps %}}
{{% /tab %}}
{{% tab "Precompiled Binaries" %}}
{{% steps %}}
1. Go to [codeberg.org/jkanev/treetime/releases/tag/2025.3](https://codeberg.org/jkanev/treetime/releases/tag/2025.3) and download a zipped package for Windows 10, 64 bit, or for Linux 64 bit from there.
2. Unzip it into your program directory (or wherever you like).
3. Unzip the data package too. Add the program folder to your path.
4. Run _TreeTime_ or _TreeTime.exe_ from the new folder.
Executable bundles have been created with pyinstaller ([www.pyinstaller.org](http://www.pyinstaller.org)).
{{% /steps %}}
{{% /tab %}}
{{% tab "Source Code / Linux" %}}
{{% steps %}}
1. Install python3
2. Install PyQt6 -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type: `pip install PyQt6`
3. Download this project from GitHub as a zip file (https://github.com/jkanev/treetime/archive/master.zip) and unzip
4. On the command line, cd into the main directory, then type:
       `python3 setup.py build`  
       `sudo python3 setup.py install`  
{{% /steps %}}
{{% /tab %}}
{{% tab "Source Code / Windows" %}}
{{% steps %}}
1. Install python3
2. Install PyQt6 -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type: `pip install PyQt6`
3. Download this project from GitHub as a zip file (https://github.com/jkanev/treetime/archive/master.zip) and unzip
4. On the command line, cd into the main directory, then type:
       `py setup.py build`  
       `py setup.py install`  
{{% /steps %}}
{{% /tab %}}
{{% /tabs %}}

Note: _TreeTime_ has recently moved to [codeberg.org](https://codeberg.org). Releases before Novebmer 2025 are here: [github.com/jkanev/treetime/releases](https://github.com/jkanev/treetime/releases).
## Run TreeTime

- Windows: Hit the Windows key and type "TreeTime", then click the "run command treetime" that comes up.
- Linux, Mac: On the command line, type "TreeTime". You can also start this any other way your operating system supports. Plus, there's a .desktop file (for KDE and Gnome) in the data directory to create desktop or menu link.

## Bugs and Problems ##

A list of bugs can be found [here](https://github.com/jkanev/treetime/issues).

## Source Code

Source code can be found on [codeberg.org](https://codeberg.org/jkanev/treetime#readme).

## Licensing and Payment ##

_TreeTime_ is free, both in the _price_ and in the _freedom_ sense. The source code is published under a GPL 3.0 license. If you want to contribute code or join the project, you're highly welcome.

