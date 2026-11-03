FROM debian:trixie-slim

# Passed by the build workflow; declaring it before the RUN busts the layer
# cache so every new version re-pulls current Debian packages.
ARG BUILD_VERSION

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      corosync-qnetd openssh-server jq tzdata \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /run/sshd \
 && id coroqnetd

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]
