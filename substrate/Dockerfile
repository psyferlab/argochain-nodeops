FROM ubuntu as builder

ARG PROFILE=release
ARG GIT_REPO=https://github.com/devolved-ai/argochain.git
ARG GIT_BRANCH=frontier-integration
ARG BINARY_NAME=argochain
ARG FLAGS="--dev"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    clang \
    cmake \
    curl \
    git \
    libssl-dev \
    pkg-config \
    protobuf-compiler

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    export PATH=$PATH:$HOME/.cargo/bin && \
    git clone ${GIT_REPO} source && \
    cd source && \
    rustup default stable && \
    rustup toolchain install nightly && \	
    rustup target add wasm32-unknown-unknown --toolchain nightly && \
    cargo build --${PROFILE} ${FLAGS} && \
    cp target/${PROFILE}/${BINARY_NAME} /argochain_node

# ===== SECOND STAGE ======

FROM ubuntu

COPY --from=builder /node /usr/local/bin

# install curl in the event we want to interact with the local rpc
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y curl
RUN useradd --create-home runner

USER runner
EXPOSE 30333 9933 9944

ENTRYPOINT ["argochain_node"]
