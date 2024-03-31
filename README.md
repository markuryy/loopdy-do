# Loopdy-do

Loopdy-do is an advanced tool for creating perfectly looping videos and GIFs from regular video files. It utilizes computer vision techniques and deep learning models to automatically detect and extract the best loop segments within a video, allowing users to preview and save them as seamless loops. This project was developed by markuryy as a utility for creating diffusion animations and was created with the assistance of Claude, an AI assistant.

![A screenshot of the Loopdy-do application GUI](/images/preview.png)

## Features

- Automatically detects and suggests the best loop segments in a video using a pre-trained ResNet-50 model for feature extraction and cosine similarity for comparing frame similarities.
- Supports both video (MP4) and GIF output formats, with customizable parameters for GIF creation, such as downscaling to a maximum dimension of 800 pixels and resampling to 20 FPS.
- Allows users to preview selected loop segments before saving, enabling them to choose the most suitable loop for their needs.
- Provides an express mode for faster processing by skipping frames, which can be useful for longer videos or when a quick preview is desired.
- Re-encodes the output files using OpenCV for videos and Pillow for GIFs to ensure better compatibility with various applications, especially with the ComfyUI diffusion animation tool.
- Offers a simple and intuitive user interface built with PyQt5, making it easy for users to navigate and interact with the application.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/markuryy/loopdy-do.git
   ```

2. Navigate to the project directory:

   ```
   cd loopdy-do
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:

   ```
   python main.py
   ```

2. Click on the "Select Video" button to choose a video file for processing.
3. Click on the "Process Video" button to analyze the video and find potential loop segments. The application will use the pre-trained ResNet-50 model to extract features from each frame and compare their similarities using cosine similarity.
4. Once the processing is complete, select a loop segment from the dropdown menu. The menu will display the start and end times of each suggested loop segment.
5. Click on the "Preview Loop" button to preview the selected loop segment. This will help you determine if the chosen segment is suitable for your needs.
6. Choose the desired output format (Video or GIF) using the radio buttons.
   - If you select the video format, the output will be saved as an MP4 file.
   - If you select the GIF format, the output will be saved as a GIF file. The GIF will be downscaled to a maximum dimension of 800 pixels and resampled to 20 FPS to optimize file size and playback performance.
7. Click on the "Save Loop" button to save the selected loop segment in the chosen format. The application will re-encode the output file using OpenCV for videos and Pillow for GIFs to ensure better compatibility with other applications, particularly the ComfyUI diffusion animation tool.

## Project Structure

The project is structured as follows:

- `main.py`: The main entry point of the application, which initializes and runs the GUI.
- `gui/`: A directory containing the GUI-related files.
  - `main_window.py`: Defines the main window of the application and handles user interactions.
  - `video_player.py`: Implements the video player component for previewing loop segments.
- `utils/`: A directory containing utility functions.
  - `video_utils.py`: Contains functions for finding loop segments, extracting and saving loop segments, and creating GIFs.
- `models/`: A directory containing the deep learning model.
  - `feature_extractor.py`: Defines the feature extractor using a pre-trained ResNet-50 model.
- `requirements.txt`: A file listing the project dependencies.
- `README.md`: The project README file.

## Known Issues

- The loop preview functionality is currently broken and needs further investigation and fixes.
- The GUI has some limitations and may benefit from additional enhancements and polish to improve the user experience.

## Requirements

- Python 3.x
- PyQt5 for building the graphical user interface
- OpenCV (cv2) for video processing and re-encoding
- NumPy for numerical operations
- Pillow for GIF creation and re-encoding
- PyTorch and torchvision for the pre-trained ResNet-50 model used in feature extraction

## Acknowledgments

- This tool was developed by markuryy as a utility for creating diffusion animations.
- The project was created with the assistance of Claude, an AI assistant developed by Anthropic, using code from the Claude 3 Opus.
- Special thanks to the open-source community for their valuable contributions and libraries that made this project possible.

## Contributing

Contributions to Loopdy-do are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, please feel free to submit a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact markuryy via GitHub or email.

---

Thank you for using Loopdy-do! We hope this tool enhances your diffusion animation workflow and helps you create stunning seamless loops.
