# Minimum docker image for demo purposes
# prebuilt-image: tvmai/demo-cpu
FROM ubuntu:16.04

RUN apt-get update --fix-missing

COPY install/ubuntu_install_core.sh /install/ubuntu_install_core.sh
RUN bash /install/ubuntu_install_core.sh

# Python: basic dependencies
RUN apt-get update && apt-get install -y python3-dev python3-pip vim
RUN pip3 install numpy nose-timer cython decorator scipy

# LLVM
RUN echo deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-6.0 main \
     >> /etc/apt/sources.list.d/llvm.list && \
     wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add - && \
     apt-get update && apt-get install -y --force-yes llvm-6.0

# Jupyter notebook.
RUN pip3 install matplotlib Image Pillow jupyter[notebook]

# Deep learning frameworks
RUN pip3 install mxnet tensorflow keras

# Pytorch 1.0
RUN pip3 install torch torchvision

# Build TVM
COPY install/install_tvm_cpu.sh /install/install_tvm_cpu.sh
RUN bash /install/install_tvm_cpu.sh


# GraphIt dependencies
RUN apt-get install -y libncurses-dev 
# GraphIt
RUN git clone https://github.com/GraphIt-DSL/graphit && \
	cd graphit && \
	git checkout 4758c2e7e027e0f1e14c7cc66a3dfaf5f8877ccf && \
	mkdir -p build && \
	cd build && \
	cmake .. && \
	make -j 16

# HBPintool
COPY install/hbpintool-release.tar.gz /install/hbpintool-release.tar.gz
RUN tar zxf /install/hbpintool-release.tar.gz && \
	cd /hbpintool-release && \
	./configure 

RUN apt-get install -y python less

# Test script.
COPY test.sh /test.sh

ENTRYPOINT sudo echo 0 > /proc/sys/kernel/yama/ptrace_scope && /bin/bash

# Environment variables
ENV PYTHONPATH "/usr/tvm/python:/usr/tvm/topi/python:/usr/tvm/nnvm/python/:/usr/tvm/vta/python"
