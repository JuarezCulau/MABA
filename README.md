# MABA: Mice Automatic Behavior Analysis
![Juarez_mice_neuroscience_analysis_detailed_4k_Leonardo_da_Vince_3e6509d0-1f94-41a3-ad9e-202367f18c4c - Copia](https://user-images.githubusercontent.com/88636064/208974390-2abde440-4662-4b4d-a52a-a02bea20e5d4.png)

MABA (Mice Automatic Behavior Analysis) is a powerful bioinformatic tool designed to automate the analysis of visual behavior in mice and rats. It provides efficient and reliable analysis for various experiments, including Freezing State, Locomotion Graphs, Open Field, Novel Object Recognition, and Elevated Plus Maze.

# Key Features
**Batch Analysis:** MABA offers the functionality to analyze a batch of videos simultaneously, providing a significant advantage when working with extensive datasets. This feature allows for efficient analysis of lengthy recordings that span hours or even days. Rather than waiting for one analysis to conclude before proceeding to the next video, MABA enables concurrent analysis, saving valuable time and reducing the laborious nature of working with large datasets.

**Freezing State:** Detect freezing behavior in videos by utilizing multiple points and calculating the Euclidean distance across frames.

**Locomotion Graphs:** Track and analyze locomotion patterns, providing valuable insights into the movement behavior of mice.

**Open Field:** Analyze mouse behavior in an open field environment, enabling comprehensive exploration and activity assessment.

**Novel Object Recognition:** Determine the time spent close to objects and detect interactions with them, offering detailed insights into object exploration behavior.

**Elevated Plus Maze:** Analyze behavior in the elevated plus maze, including the detection of nose poking.

# Model Requirements
MABA utilizes a pre-trained TensorFlow model based on the ResNet50 architecture (PB File). However, custom-trained models using tools like DeepLabCut can also be incorporated into MABA. When using custom-trained models, it is important to follow the same points and annotations used in MABA to ensure compatibility.

# Installation
To install MABA, refer to our detailed installation guide available [here](https://github.com/JuarezCulau/MABA/blob/main/Docs/Installation.md). It provides step-by-step instructions to set up and configure the tool on your system.

# Documentation
Comprehensive documentation for MABA is available in the [Guides directory](https://github.com/JuarezCulau/MABA/tree/main/Docs/Guides) of the repository. The guides cover various aspects of using MABA and provide detailed instructions to help you maximize the tool's capabilities.

# Contributions and Feedback
We welcome contributions and feedback from the user community. If you have any suggestions, feature requests, or encounter any bugs or issues while using MABA, please feel free to submit them. Your patience is appreciated as we strive to address any concerns promptly.

We hope that MABA proves to be a valuable tool in your research and analysis endeavors. Enjoy using MABA to streamline and automate your visual behavior analysis tasks with ease!
