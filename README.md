# Public transport network simulation

## Installation

To download required dependencies go to folder with project and use:
```bash
pip install requirements.txt
```

## Usage
To run program, open terminal, go to project directory and use:
```bash
python one_line_sim.py
```

After setting bus frequency, bus size and traffic jams parameters press 'Start' button to start drawing lines.

Press 'Add line' button and write its name in text field. Press ENTER to accept.
Choose line color and press 'Ok' button to accept. After clicking on black background, 
write a name and press ENTER to add a new stop. Repeat until you are satisfied with your line.
To add more lines, simply repeat steps above.
You can also add already existing stops to other lines, by clicking them on the map.
When everything is set, click 'Start' button on the right bar and watch simulation.
The results can be seen in main window, after clicking 'Show plot' button a second window with plot shows up.
The second window displays plot with currently chosen statistic, to change this statistic use right side buttons.
The simulation can be paused and resumed any time. When simulation is stopped it is also possible to save statistics in `.csv` file
using 'Save statistics' button. Prepared network configuration can be saved into `.json` file using 'Save network' button. 
Previously saved networks can be loaded by click 'Load network' button.

## Examples

It is also possible to run prepared example by pressing 'Start' button without setting lines.
Other example that was used in our paper, can be found in `my_network` file. It can be loaded using 'Load network' button.

