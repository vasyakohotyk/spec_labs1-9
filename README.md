# Project Overview

This project consists of several subapplications, each fulfilling specific functionalities like generating ASCII art, handling calculators, running tests, interacting with APIs, and visualizing data.

## SubApplications

### Functional calculator

Includes operations and functionalities essential for a basic calculator.

### Class calculator

Implements calculator functionalities using classes and methods for better structure and reusability.

### ASCII generator with pyfiglet and colorama

Generates ASCII art using the Pyfiglet library and colors the output with the Colorama library.

### ASCII generator with custom generator

Custom implementation for generating ASCII art, providing flexibility for various artistic representations.

### ASCII 3D generator with PyOpenGL usage

Creates 3D ASCII scenes and uses PyOpenGL for rendering and visualizing the scenes.

### Run test for calculator

Automates the testing of calculator functionalities, ensuring accuracy and reliability.

### Usage of Google Books API

Interacts with the Google Books API to fetch and display book information based on user queries.

### Visualizing sleep and active data

Utilizes data visualization libraries to represent sleep and active data graphically, offering insights into user activities.

### Documentation

Provides comprehensive documentation for all modules, ensuring clarity and ease of use for developers and users.

## Requirements

```plaintext
Requests==2.32.3
colorama~=0.4.6
pyfiglet~=1.0.2
PyOpenGL~=3.1.7
numpy~=2.1.2
pillow~=11.0.0
jsonpickle~=3.3.0
pathlib~=1.0.1
Pygments~=2.18.0
python-dotenv~=1.0.1
tabulate~=0.9.0
PyAutoGUI~=0.9.54
mpld3~=0.5.10
pandas~=2.2.3
matplotlib~=3.9.2
```

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    ```
2. Change to the project directory:
    ```bash
    cd <project_directory>
    ```
3. Install the necessary packages:
    ```bash
    pip install -r requirements.txt
    ```
4. For visualization, you can export data from Zepp Life or any other source in the following format:

```csv
# src/data/activity.csv
date,steps,distance,runDistance,calories
yyyy-mm-dd,int,int,int,int
```

```csv
# src/data/sleep.csv
date,deepSleepTime,shallowSleepTime,wakeTime,start,stop,REMTime,naps
yyyy-mm-dd,int,int,int,yyyy-mm-dd hh:mm:ss+0000,yyyy-mm-dd hh:mm:ss+0000,int,None or Any
```

## Usage

To start the application, run the following command:
```bash
python runner.py
```

## License

This project is licensed under the MIT License.