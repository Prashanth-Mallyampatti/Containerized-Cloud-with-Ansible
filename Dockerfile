FROM ubuntu:18.04
ENV container docker

MAINTAINER Prashanth_M

ARG DEBIAN_FRONTEND=noninteractive

RUN \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install ubuntu-server && \
    apt-get install -y build-essential && \
    apt-get install -y software-properties-common && \
    apt-get install -y git vim wget python openssh-server openssh-client && \
    apt-get install -y iperf3 iproute2 iputils-ping && \
    apt-get install -y tcpdump wireshark && \
    apt-get install -y locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/lib/dpkg/lock* && \
    rm -rf /var/cache/apt/archives/lock && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8

RUN cd /lib/systemd/system/sysinit.target.wants/ \
    && ls | grep -v systemd-tmpfiles-setup | xargs rm -f $1

RUN rm -f /lib/systemd/system/multi-user.target.wants/* \
    /etc/systemd/system/*.wants/* \
    /lib/systemd/system/local-fs.target.wants/* \
    /lib/systemd/system/sockets.target.wants/*udev* \
    /lib/systemd/system/sockets.target.wants/*initctl* \
    /lib/systemd/system/basic.target.wants/* \
    /lib/systemd/system/anaconda.target.wants/* \
    /lib/systemd/system/plymouth* \
    /lib/systemd/system/systemd-update-utmp*

RUN systemctl set-default multi-user.target
ENV init /lib/systemd/systemd
VOLUME [ "/sys/fs/cgroup" ]
WORKDIR "/root"

CMD ["/sbin/init"]

