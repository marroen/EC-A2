
##### DOCS START             #####

- graph-tool: https://graph-tool.skewed.de/static/doc/quickstart.html#creating-graphs

##### DOCS END               #####



##### INSTALLING CONDA START #####

Ensure you have (ana)conda:

run `brew install anaconda`

(For Windows/Linux follow https://www.anaconda.com/download/)

If you needed to install conda, also add to path:

If you use zsh terminal, macOS:

run ``echo `export PATH="/usr/local/anaconda3/bin:$PATH"` >> ~/.zshrc``

run ``echo `export PATH="/opt/homebrew/anaconda3/bin:$PATH"` >> ~/.zshrc``

run `source ~/.zshrc`

If you use bash terminal, macOS:

run ``echo `export PATH="/usr/local/anaconda3/bin:$PATH"` >> ~/.bash_profile``

run ``echo `export PATH="/opt/homebrew/anaconda3/bin:$PATH"` >> ~/.bash_profile``

run `source ~/.bash_profile`

Try to run `conda` after this to verify it works, otherwise:

M1-based macOS:
run `/opt/homebrew/anaconda3/bin/conda init zsh`

Intel-based macOS:
run `/usr/local/anaconda3/bin/conda init zsh`

Give conda permission to install packages:

run `sudo chown -R $USER ~/.conda`

##### INSTALLING CONDA END #####



##### RUNNING CODE START   #####

To create a virtual environment (and installing graph-tool):

run `conda create --name gt -c conda-forge graph-tool`

Then, whenever you want to run the code:

run `conda activate gt`

If you are using PyCharm, add local environment path like this:

M1-based macOS:
/opt/homebrew/anaconda3/bin/anaconda

Intel-based macOS:
/usr/local/anaconda3/bin/conda

And then simply:

run `python3 main.py`

And to leave the virtual environment (only when you finish your coding session):

run `conda deactivate`

##### RUNNING CODE END     #####
