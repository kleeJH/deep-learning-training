# Object (somewhat) Localisation
## How to install
### Conda Environment
  - Install Anaconda3 or Miniconda
  - Open Command Palette, type Python: Create Environment command
  - Select Conda, then select Python version
  - It will then create a .conda folder

#### Possible problems
- Make sure Conda is configured in your PATH environment variables
- Do `conda init` when starting it for the first time

### Setting up your packages
#### Setting up Tensorflow GPU (optional)
Use `conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0` for GPU support. <br>
Else go to requirements.txt and change to `tensorflow-cpu` for the CPU-only package.

#### Setting up packages using pip
Do `pip install -r requirements.txt`

#### Sequence of files to run
- Run prediction_model.ipynb
- Run xy_locate.ipynb
- Run results.ipynb (will generate results.csv in the root directory)

#### Problems
- Some folders might be missing