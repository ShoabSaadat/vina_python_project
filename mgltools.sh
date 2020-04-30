mypwd="$PWD"
cd $HOME
wget https://de.cyverse.org/dl/d/A304B111-2CF4-48B4-A2E0-46B2875764C4/mgltools_x86_64Linux2_1.5.7.tar_.gz
sudo tar -zxvf ./mgltools_x86_64Linux2_1.5.7.tar_.gz
mv ./mgltools_x86_64Linux2_1.5.7/ ./mgltools
cd mgltools
sudo chmod +x ./install.sh
sudo sh ./install.sh
export PATH=$HOME/mgltools/bin:$PATH
echo "MGL TOOLS Installed. Now taking you back to your early directory at: $mypwd"
alias obabel="/usr/bin/obabel" #Just resetting obabel alias just in case
cd "$mypwd"; ls


#.bashrc
#alias pmv='$HOME/mgltools/bin/pmv'
#alias adt='$HOME/mgltools/bin/adt'
#alias vision='$HOME/mgltools/bin/vision'
#alias pythonsh='$HOME/mgltoolsin/pythonsh'
#OR
#source $HOME/mgltools/initMGLtools.sh (bash)
#USE THIS source CURRENTVINADIR/mgltoolspath.sh