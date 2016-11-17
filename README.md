![](docs/images/slide.png)

## What?

A CruftFest 2016 project / an assignment to the Interactive Digital Multimedia Techniques (ESC742P) module, Media and Arts Technology, Queen Mary University of London.

## The task

_cruft: accumulated physical or virtual junk._

Save a small amount of cruft from the dump by repurposing it as a digital media interface.

## More info

- [Demos](http://www.tomgurion.me/tapeless-cassettes.html).
- [Full conceptual / technical report about the project](docs/report.md).

## How to run the project

- Connect the cassettes to the arduino.
- Upload the `read_wheel/read_wheel.ino` sketch to arduino.
- Install the python requirements for the project with `pip install -r wheel_speed_analyser/requirements.txt` (preferably in a virtual environment).
- Run the `wheel_speed_analyser/wheel_speed_analyser.py` script. Run with `--help` to see the available options.
- Optionally run the `osc_spectogram/osc_spectogram.pde` processing monitoring sketch.
- Run the `player/player.pd` patch.
