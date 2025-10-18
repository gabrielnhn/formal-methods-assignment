#!/bin/bash
export GUROBI_HOME="$HOME/formal-methods-assignment/gurobi912/linux64"
export PATH="$PATH:${GUROBI_HOME}/bin"
export CPATH="$CPATH:${GUROBI_HOME}/include"
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$CONDA_PREFIX/lib:/usr/lib/wsl/lib:$LD_LIBRARY_PATH:/usr/local/lib:${GUROBI_HOME}/lib
export GRB_LICENSE_FILE=$HOME/gurobi/gurobi.lic
