# Best Shot Labeling Software

This software is a hybrid application combining Flask (a web framework) and PyQt5 (a desktop GUI library) to create an interactive tool for labeling images efficiently. The application is designed to help users navigate through image directories, display images, and label them interactively. The labeled data is stored in CSV files for further processing or analysis.

## Features

- **Interactive GUI**: A PyQt5-based desktop interface with a built-in browser window for seamless interaction with the Flask web application.
- **Dynamic Image Loading**: Navigate through image directories and view images grouped by predefined naming conventions.
- **Image Labeling**: Click on images to label them and store the labels in a CSV file.
- **Data Persistence**: Automatically tracks and logs the labeling progress, resuming from the last labeled frame.
- **CSV Management**: Writes labeled data to a CSV file and maintains a log of the last labeled frame.

## Requirements

### Software Dependencies
Ensure the following are installed:
- Python 3.8+
- Flask
- PyQt5
- pandas

### Python Libraries
Install required libraries using pip:
```bash
pip install flask pyqt5 pandas
```

## Usage

### 1. Starting the Application
Run the script to start both the Flask server and the PyQt5 GUI:
```bash
python main.py
```

### 2. Directory Selection
- Enter the directory path containing the image files in the web interface.
- The application expects images to follow the naming convention `len{j}_screenshot_{frame:04d}.jpg` stored in subdirectories named `1`, `2`, ..., `6`.

### 3. Labeling Images
- The web interface displays the images.
- Click an image to label it. The label, frame, and file name will be stored in `label.csv`.

### 4. Navigating Images
- Use the **Next** button to load the next group of images.
- The progress is automatically logged in `log.csv`.

### 5. CSV Outputs
- `label.csv`: Contains labeled data with columns `frame`, `label`, and `name`.
- `log.csv`: Tracks the last labeled frame for resuming progress.

### 6. Accessing the Web Interface
The Flask server runs on `http://localhost:5000/`. The PyQt5 GUI includes a browser to interact with this server.

## File Structure

```plaintext
project/
├── main.py         # Main script
├── static/         # Directory containing images
├── label.csv       # Output file for labeled data
├── log.csv         # File tracking labeling progress
├── templates/      # Flask HTML templates
│   ├── index.html  # Main interface
│   ├── gallery.html # Image gallery view
```

## Code Overview

### Key Components

- **Flask Routes**:
  - `/`: Renders the main interface.
  - `/submit`: Processes directory input and loads images.
  - `/next_image`: Loads the next set of images for labeling.
  - `/image_click`: Captures image click events and logs labels.

- **Image Navigation**:
  - `chooseI(directory, frame)`: Locates images following the naming convention and updates the frame index.

- **CSV Management**:
  - `write_image_to_csv(filename)`: Appends labeled data to `label.csv`.
  - `csv_init()`: Initializes `log.csv` and `label.csv` if missing.

- **PyQt5 GUI**:
  - Hosts the Flask application in a browser widget for an integrated experience.

## Contributing

If you'd like to contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

## Troubleshooting

- **Flask Server Not Starting**: Ensure port 5000 is not in use.
- **Image Not Found**: Verify the directory structure and file naming conventions.
- **GUI Issues**: Ensure PyQt5 is correctly installed and configured.

## License

This software is distributed under the MIT License. Feel free to use, modify, and distribute it as needed.

---

For questions or issues, please contact the developer or open an issue in the repository.

