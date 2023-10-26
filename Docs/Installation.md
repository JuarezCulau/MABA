# How to Install MABA

MABA was created to run on windows

# 1: Python is required
To quickly have python running on your machine, download [Anaconda](https://www.anaconda.com/products/distribution) and [Python](https://www.python.org/downloads/)

# 2: If you wish to use a GPU (Recommended), you need to also have CUDA and cuDNN installed.
Please be aware that CUDA is compatible only with NVIDIA GPUs. Check the support for your GPU.  
It needs to be compatible with TensorFlow 2.10.0. For development, CUDA 11.7 is currently being used.  
Ensure that you have the appropriate version of cuDNN installed, which is compatible with your current CUDA version.  
If you are using CUDA 11.x, it is recommended to install cuDNN version 8.9.5.

# 3: Create a new environment
First, open Anaconda Terminal. Then, use the following command. 
```
conda create --name MABA
```
Now, activate the environment
```
conda activate MABA
```

# 4: Install pip
If pip is not already installed on your machine, please install it using the following command:
```
conda install pip
```

# 5: Install pipreqs
```
pip install pipreqs
```

# 6: Clone the repository
You can clone the repository in any folder, but for organization purposes, we recommend you to clone the repository into the new environment. 
Go to the folder where your environment is located, by standard, it should be C:\Users\YourUserName\.conda\envs\MABA.
```
cd C:\Users\YourUserName\.conda\envs\MABA
```
Then, clone the repository.
```
git clone https://github.com/JuarezCulau/MABA
```

# 7: Install the final requirements
Navigate to the 'MABA' folder, where you have cloned the repository, using the following command:

```
cd MABA
```

Then, use the following command:
```
pip install -r requirements.txt
```
You have now completed the installation of MABA and are prepared to begin using it.

Should you encounter any issues during the installation process, I encourage you to report them by opening an issue.

To launch MABA, simply execute the following command:
```
python GUI.py
```

Kindly ensure that you are in the correct directory when you run MABA in the future.
In the terminal, you can change directories using the 'cd' command followed by the 'folder_path.' For example, in this context, the command would be:
```
cd C:\Users\YourUserName\.conda\envs\MABA\MABA
```

Give a look at the remaining docs to learn how to use it, I can assure you that it will be a quick read.