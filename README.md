# ERAN + softmax abstract transformer.
### Gabriel Hishida, Soumen Sinha, Vladimir Petkov


This project was implemented as an extension of ERAN (https://github.com/eth-sri/eran) and ELINA (https://github.com/eth-sri/ELINA).

Our contribution to this project can be mostly seen in `ELINA/fppoly/softmax_approx.c`, `ELINA/fppoly/softmax_approx.h`, `ELINA/python_interface/fppoly.py`, `tf_verify`, `plot_results.py`, `train_onnx.py` and pretty much every mention of `softmax()`.


In order to install and run all necessary components, follow the original installation guide appended in this README file.

We personally recommend a Linux system and conda environment with Python3.6.
This can be made with ```conda create --name py36 python=3.6```

Extra packages required:
```
sudo apt-get install libglpk-dev
sudo apt install liblapacke-dev
```

Usage: Instructions for compilation and running an evaluation of an onnx model:

```
cd elina/fppoly
make clean
make

cd .. (elina)
make
sudo make install

cd ../tf_verify
python3 . --netname ../mnist_simplest_softmax.onnx --epsilon 0.005 --domain deeppoly --dataset mnist
```


# ERAN Original installation guide

Requirements 
------------
GNU C compiler, ELINA, Gurobi's Python interface,

python3.6 or higher, tensorflow 1.11 or higher, numpy.

On Ubuntu systems they can be installed using:
```
sudo apt-get install m4
sudo apt-get install build-essential
sudo apt-get install autoconf
sudo apt-get install libtool
sudo apt-get install texlive-latex-base
```
Consult https://cmake.org/cmake/help/latest/command/install.html for the install of cmake or use:
```
wget https://github.com/Kitware/CMake/releases/download/v3.19.7/cmake-3.19.7-Linux-x86_64.sh
sudo bash ./cmake-3.19.7-Linux-x86_64.sh
sudo rm /usr/bin/cmake
sudo ln -s ./cmake-3.19.7-Linux-x86_64/bin/cmake /usr/bin/cmake
```


The steps following from here can be done automatically using `sudo bash ./install.sh`

Install gmp:
```
wget https://gmplib.org/download/gmp/gmp-6.1.2.tar.xz
tar -xvf gmp-6.1.2.tar.xz
cd gmp-6.1.2
./configure --enable-cxx
make
make install
cd ..
rm gmp-6.1.2.tar.xz
```

Install mpfr:
```
wget https://files.sri.inf.ethz.ch/eran/mpfr/mpfr-4.1.0.tar.xz
tar -xvf mpfr-4.1.0.tar.xz
cd mpfr-4.1.0
./configure
make
make install
cd ..
rm mpfr-4.1.0.tar.xz
```

Install cddlib:
```
wget https://github.com/cddlib/cddlib/releases/download/0.94m/cddlib-0.94m.tar.gz
tar zxf cddlib-0.94m.tar.gz
rm cddlib-0.94m.tar.gz
cd cddlib-0.94m
./configure
make
make install
cd ..
```

Install Gurobi:
```
wget https://packages.gurobi.com/9.1/gurobi9.1.2_linux64.tar.gz
tar -xvf gurobi9.1.2_linux64.tar.gz
cd gurobi912/linux64/src/build
sed -ie 's/^C++FLAGS =.*$/& -fPIC/' Makefile
make
cp libgurobi_c++.a ../../lib/
cd ../../
cp lib/libgurobi91.so /usr/local/lib
python3 setup.py install
cd ../../
```

Update environment variables:
```
export GUROBI_HOME="$PWD/gurobi912/linux64"
export PATH="$PATH:${GUROBI_HOME}/bin"
export CPATH="$CPATH:${GUROBI_HOME}/include"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:${GUROBI_HOME}/lib
```

Install ELINA:
```
cd ELINA
./configure -use-deeppoly -use-gurobi -use-fconv -use-cuda
cd ./gpupoly/
cmake .
cd ..
make
make install
cd ..
```

Install DeepG (note that with an already existing version of ERAN you have to start at step Install Gurobi):
```
git clone https://github.com/eth-sri/deepg.git
cd deepg/code
mkdir build
make shared_object
cp ./build/libgeometric.so /usr/lib
cd ../..
```

We also provide scripts that will install ELINA and all the necessary dependencies. One can run it as follows (remove the `-use-cuda` argument on machines without GPU):

```
sudo ./install.sh -use-cuda
source gurobi_setup_path.sh
```


Note that to run ERAN with Gurobi one needs to obtain an academic license for gurobi from https://user.gurobi.com/download/licenses/free-academic.
If you plan on running ERAN on Windows WSL2, you might prefer requesting a cloud-based academic license at [https://license.gurobi.com](https://license.gurobi.com), in order to avoid [this issue](https://github.com/microsoft/WSL/issues/5352) with early-expiring licenses.

To install the remaining python dependencies (numpy and tensorflow), type:

```
pip3 install -r requirements.txt
```

ERAN may not be compatible with older versions of tensorflow (we have tested ERAN with versions >= 1.11.0), so if you have an older version and want to keep it, then we recommend using the python virtual environment for installing tensorflow.

If gurobipy is not found despite executing `python setup.py install` in the corresponding gurobi directory, 
gurobipy can alternatively be installed using conda with:
```
conda config --add channels http://conda.anaconda.org/gurobi
conda install gurobi
```


-------------
ERAN ORIGINAL License and Copyright
---------------------

* Copyright (c) 2020 [Secure, Reliable, and Intelligent Systems Lab (SRI), Department of Computer Science ETH Zurich](https://www.sri.inf.ethz.ch/)
* Licensed under the [Apache License](https://www.apache.org/licenses/LICENSE-2.0)
