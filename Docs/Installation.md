# How to Install MABA

##MABA was created to run on windows

# 1: Python is required
To quickly have python running on your machine, download and install [Anaconda] (https://www.anaconda.com/products/distribution).

# 2: If you wish to use a GPU (Recommended), you need to also have CUDA and cuDNN installed.
Please note that CUDA systems only with NVIDIA GPUs, please check the support for your GPU.

# 3: Create a new environment
First, open Anaconda. Then, use the following command. 
```
conda create --name MABA
```
Now, activate the environment
```
conda activate MABA
```

# 4: Install pipreqs
```
pip install pipreqs
```

# 5: Clone the repository
You can clone the repository in any folder, but for organization purposes, we recommend you to clone the repository into the new environment. 
Go to the folder where your environment is located, by standard, it should be C:\Users\YourUserName\.conda\envs\MABA.
```
cd C:\Users\YourUserName\.conda\envs\MABA
```
Then, clone the repository.
```
git clone https://github.com/JuarezCulau/MABA
```

# 6: Install the final requirements
Enter MABA folder, where you have cloned the repository, and use the following command
```
pip install -r requirements.txt
```
Now, you have successfully installed MABA and are ready to use it!
Give a look at the remaining docs to learn how to use it, I can assure you that it will be a quick read.
