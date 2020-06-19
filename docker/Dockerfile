# Minimum docker image for demo purposes
# prebuilt-image: tvmai/demo-cpu
FROM ubuntu:20.04

RUN apt-get update --fix-missing

COPY install/ubuntu_install_core.sh /install/ubuntu_install_core.sh
RUN bash /install/ubuntu_install_core.sh

# Python dependencies.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-dev python3-pip vim pkg-config
COPY install/requirements.txt /install/requirements.txt
RUN pip3 install -r /install/requirements.txt

# LLVM
RUN echo deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-6.0 main \
     >> /etc/apt/sources.list.d/llvm.list && \
     wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add - && \
     apt-get update && apt-get install -y --force-yes llvm-6.0

# Build TVM
COPY install/install_tvm_cpu.sh /install/install_tvm_cpu.sh
RUN bash /install/install_tvm_cpu.sh

# GraphIt dependencies
RUN apt-get install -y libncurses-dev
# GraphIt
RUN git clone https://github.com/GraphIt-DSL/graphit && \
	cd graphit && \
	git checkout 576f9ca7ab20e627ea5548db6d0ac536dd8de1a2 && \
	mkdir -p build && \
	cd build && \
	cmake .. && \
	make -j 16
ENV GRAPHIT_BUILD_DIRECTORY "/graphit/build"
ENV GRAPHIT_SOURCE_DIRECTORY "/graphit"
ENV CXX_COMPILER "c++"

# HBPintool
COPY install/hbpintool-release.tar.gz /install/hbpintool-release.tar.gz
RUN tar zxf /install/hbpintool-release.tar.gz && \
	cd /hbpintool-release && \
	./configure

RUN apt-get install -y python less curl
RUN apt-get install -y linux-tools-common linux-tools-generic linux-tools-`uname -r`

# Test script.
COPY test.sh /test.sh
RUN chmod a+x /test.sh

ENV MALLOC_CHECK_ 1 # temporary work around for GraphIt runtime bug
ENTRYPOINT sudo echo 0 > /proc/sys/kernel/yama/ptrace_scope && /bin/bash

# Environment variables
ENV PYTHONPATH "/usr/tvm/python:/usr/tvm/topi/python:/usr/tvm/nnvm/python/:/usr/tvm/vta/python:/graphit/src/python"

# Add performance estimation tool.
COPY perf-energy-tool /perf-energy-tool
