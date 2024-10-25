# Poker-Preflop-Trainer

This is a standalone web application built with Flask that helps train poker pre-flop ranges. The app randomly generates two poker cards, and the user must guess the correct bucket (classification) of the hand based on pre-defined classifications.

![screenshot](screenshots/screenshot.png)

## Features

- **Random Poker Hand Generation**: Generates two poker cards, which the user has to classify.
- **Bucket Classification**: The user enters a bucket for the generated hand, and the app checks if it's correct.
- **Web Interface**: A simple and intuitive web interface, automatically opened in the browser.
- **Standalone Application**: The app is bundled as a single executable using PyInstaller, so no external Python installation is required.

## Installation and Usage:

  1.  From the releases, download the binary suitable for your operating system. (Only available for linux at the moment)
  2.  Run the downloaded executable file: PreFlopTrainer.
  3.  The app will automatically open in your browser. If it doesn’t, open your browser and navigate to http://127.0.0.1:5000.
  4.  Click "Generate Hand" to start, and enter the bucket you think the hand belongs to.


## Running the python code and building the app

### Requirements

- **Python 3.x**
- **Flask**
- **Pillow**
- **Pandas**
- **Numpy**
- **PyInstaller** (if you want to package the app into a standalone executable)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/poker-preflop-trainer.git
    cd poker-preflop-trainer
    ```

2. Set up a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. Run the Flask app:
    ```bash
    python PreFlopTrainer.py
    ```

2. The app will automatically open in your web browser. If it doesn't, manually open your browser and navigate to `http://127.0.0.1:5000`.

3. Click **Generate Hand** to generate two poker cards. Guess the bucket and submit your answer.

### Bundling the App with PyInstaller

To create a standalone executable:

1. Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2. Run the following command to bundle the app into a single executable:
    ```bash
    pyinstaller --onefile --add-data "data:data" --add-data "templates:templates" PreFlopTrainer.py
    ```

3. The executable will be created in the `dist/` directory. You can now run the app without requiring a Python installation:
    ```bash
    ./dist/PreFlopTrainer
    ```

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgements
  - **Flask** - A lightweight WSGI web application framework.
  - **PyInstaller** - A tool to bundle Python applications into standalone executables.
  - **5-Card_Poker_Hand_Simulator_and_Visualizer** The cards images and code to generate 2-cards visualization was inspired by the following project : https://github.com/SJMagaziner/5-Card_Poker_Hand_Simulator_and_Visualizer
