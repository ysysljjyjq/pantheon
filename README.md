[![Build Status](https://travis-ci.org/StanfordLPNG/pantheon.svg?branch=master)]
(https://travis-ci.org/StanfordLPNG/pantheon)

# Disclaimer:
This is unfinished research software. Multiple scripts run commands as root to install prerequisite programs, update package lists, etc. Our scripts will write to the filesystem in the pantheon folder and in /tmp/. We have not implemented most of the programs run by our wrappers. Those programs may write to the filesytem (for example, Verus will write files like `client_45191.out` into the current working directory when it is called). We never run third party programs as root, but we can not guarantee they will never try to escalate privaledge to root.

Run at your own risk.

# Pantheon of Congestion Control
The Pantheon has wrappers for many popular and research congestion control schemes. It allows them to run over a common interface and has tools to benchmark and compare their performance.
Pantheon tests can be run locally over an emulated link using [mahimahi](http://mahimahi.mit.edu/) or over the internet to a remote machine.

## Preparation
Many of the tools and programs run by the Pantheon are git submodules in the `third_party` folder.
To clone this repository, including submodules, run:

```
git clone --recursive https://github.com/StanfordLPNG/pantheon.git
```

To add submodules after cloning, run:
```
git submodule update --init
```


And before perorming analysis run:
```
analysis/analysis_pre_setup.py
```

## Running the Pantheon
Currently supported schemes can be found in `src/`. Running:

```
test/run.py
```

Will setup and run all congestion control schemes in the Pantheon locally (and remotely if the `-r` flag is used). Multiple flows can be run simultaneously with `-f`. The running time of each scheme can be specified with `-t` and the entire experiment can be run multiple times using `--run-times`. Logs of all packets sent and recieved will be written to `test/` for later analysis.


Run `test/run.py -h` for detailed usage and additional optional arguments.

## Running a single congestion control scheme
Before performing experiments individually run:
```
test/pre_setup.py
```

To make and install the `sprout` and it's dependencies run:

```
test/setup.py sprout
```

Run `test/setup.py -h` for detailed usage and additional optional arguments.

To test `sprout` over an emulated link run:
```
test/test.py [-t RUNTIME] [-f FLOWS] congestion-control
```

To setup and test `sprout` over the wide area to a remote machine run:
```
test/pre_setup.py -r REMOTE:PANTHEON-DIR
test/setup.py -r REMOTE:PANTHEON-DIR sprout
test/test.py -r REMOTE:PANTHEON-DIR [-t RUNTIME] [-f FLOWS] sprout
```

Run `test/test.py -h` for detailed usage and additional optional arguments.


`-f 0` indicates that no tunnels would be created in the tests; otherwise,
there will be `FLOWS` tunnels created to run a congestion control scheme.
Notice that if `-r` is given, `FLOWS` must be positive.

Alternatively, run

```
./run.py [-r REMOTE:PANTHEON-DIR] [-t RUNTIME] [-f FLOWS]
```

## Usage of Individual Scheme
Change directory to `src` first.

```
# print the dependencies required to be installed
./<congestion-control>.py deps

# perform build commands for scheme
./<congestion-control>.py build

# run initialize commands after building and before running
./<congestion-control>.py init

# find running order for scheme
./<congestion-control>.py who_goes_first

# find friendly name of scheme
./<congestion-control>.py friendly_name
```

Depending on the output of `who_goes_first`, run

```
# Receiver first
./<congestion-control>.py receiver
./<congestion-control>.py sender IP port
```

or

```
# Sender first
./<congestion-control>.py sender
./<congestion-control>.py receiver IP port
```
