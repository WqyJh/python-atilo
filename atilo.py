import os
import platform

from plumbum import local, colors, cli, FG
from plumbum.cmd import rm, chmod, echo, uname


support_linux = {
    'alpine': {
        'url': 'http://dl-cdn.alpinelinux.org/alpine/v{version}/releases/{arch}/alpine-minirootfs-{version}.0-aarch64.tar.gz',
        'zip': 'zx',
        'update': 'apk update && apk upgrade',
        'latest': 'latest-stable',
        'aarch64': {
            'versions': ['3.9', 'latest-stable'],
        },
        'arm': {
            'arch': 'armhf',
            'versions': ['3.9', 'latest-stable'],
        },
        'amd64': {
            'arch': 'x86_64',
            'versions': ['2.7', '3.9', 'latest-stable'],
        },
        'i386': {
            'arch': 'x86',
            'versions': ['2.7', '3.9', 'latest-stable'],
        },
    },
    'arch': {
        'url': 'http://os.archlinuxarm.org/os/ArchLinuxARM-{arch}-{version}.tar.gz',
        'zip': 'pzx',
        'update': 'pacman-key --init && pacman-key --populate archlinuxarm && pacman -Sy',
        'latest': 'latest',
        'aarch64': {
            'versions': ['latest'],
        },
        'arm': {
            'arch': 'armv7',
            'versions': ['latest'],
        },
    },
    'centos': {
        'url': 'https://raw.githubusercontent.com/CentOS/sig-cloud-instance-images/CentOS-{version}{arch}/docker/centos-{version}{arch}-docker.tar.xz',
        'zip': 'Jx',
        'update': 'yum makecache',
        'latest': '7',
        'aarch64': {
            'arch': 'arm64',
            'versions': ['7'],
            'url': 'https://raw.githubusercontent.com/CentOS/sig-cloud-instance-images/CentOS-{version}-aarch64/docker/centos-{version}arm64-docker.tar.xz',
        },
        'arm': {
            'arch': 'armhf',
            'versions': ['7'],
        },
        'amd64': {
            'arch': '',
            'versions': ['7'],
        },
        'i386': {
            'versions': ['7'],
        },
    },
    'debian': {
        'url': 'https://github.com/debuerreotype/docker-debian-artifacts/raw/dist-{arch}/{version}/slim/rootfs.tar.xz',
        'zip': 'Jx',
        'update': 'apt update && apt upgrade',
        'latest': 'stable',
        'aarch64': {
            'arch': 'arm64v8',
            'versions': ['stretch', 'buster', 'stable'],
        },
        'arm': {
            'arch': 'arm32v7',
            'versions': ['jessie', 'stretch', 'buster', 'stable'],
        },
        'amd64': {
            'versions': ['jessie', 'stretch', 'buster', 'stable'],
        },
        'i386': {
            'versions': ['jessie', 'stretch', 'buster', 'stable'],
        },
    },
    'fedora': {
        'url': 'https://dl.fedoraproject.org/pub/fedora/linux/releases/{version}/Container/{arch}/images/Fedora-Container-Base-{version}-1.2.{arch}.tar.xz',
        'zip': 'Jx',
        'update': 'dnf makecache',
        'latest': '30',
        'aarch64': {
            'versions': ['30'],
        },
        'arm': {
            'arch': 'armhfp',
            'versions': ['28'],
            'url': 'https://dl.fedoraproject.org/pub/fedora/linux/releases/{version}/Container/{arch}/images/Fedora-Container-Minimal-Base-{version}-1.1.{arch}.tar.xz',
        },
        'amd64': {
            'arch': 'x86_64',
            'versions': ['30'],
        },
    },
    'kali': {
        'url': 'https://raw.githubusercontent.com/EXALAB/AnLinux-Resources/master/Rootfs/Kali/{arch}/kali-rootfs-{arch}.tar.gz',
        'zip': 'zx',
        'update': 'apt update && apt upgrade',
        'latest': '',
        'aarch64': {
            'arch': 'arm64',
            'versions': [''],
        },
        'arm': {
            'arch': 'armhf',
            'versions': [''],
        },
        'amd64': {
            'versions': [''],
        },
        'i386': {
            'versions': [''],
        },
    },
    'opensuse': {
        'url': 'http://download.opensuse.org/ports/{arch}/distribution/leap/{version}/appliances/openSUSE-Leap-{version}-ARM-JeOS.{arch}-rootfs.{arch}.tar.xz',
        'zip': 'Jx',
        'update': 'zypper up',
        'latest': '15.1',
        'aarch64': {
            'versions': ['15.1'],
        },
    },
    'parrot': {
        'url': 'https://raw.githubusercontent.com/EXALAB/AnLinux-Resources/master/Rootfs/Parrot/{arch}/parrot-rootfs-{arch}.tar.gz',
        'zip': 'zx',
        'update': 'apt update && apt upgrade',
        'latest': '',
        'aarch64': {
            'arch': 'arm64',
            'versions': [''],
        },
        'arm': {
            'arch': 'armhf',
            'versions': [''],
        },
        'amd64': {
            'versions': [''],
        },
        'i386': {
            'versions': [''],
        },
    },
    'ubuntu': {
        'url': 'https://partner-images.canonical.com/core/{version}/current/ubuntu-{version}-core-cloudimg-{arch}-root.tar.gz',
        'zip': 'zx',
        'update': 'apt update && apt upgrade',
        'latest': 'bionic',
        'aarch64': {
            'arch': 'arm64',
            'versions': ['trusty', 'xenial', 'bionic'],
        },
        'arm': {
            'arch': 'armhf',
            'versions': ['trusty', 'xenial', 'bionic'],
        },
        'amd64': {
            'versions': ['trusty', 'xenial', 'bionic'],
        },
        'i386': {
            'versions': ['trusty', 'xenial', 'bionic'],
        },
    },
}


name_servers = '''nameserver 1.1.1.1
nameserver 1.0.0.1
nameserver 8.8.8.8
nameserver 8.8.4.4
'''


start_script = '''#!/data/data/com.termux/files/usr/bin/bash
cd $HOME/.atilo/
unset LD_PRELOAD
command="proot"
#command+=" -0"
command+=" -S {release_name}"
#command+=" -b /system"
command+=" -b /dev/"
#command+=" -b /sys/"
command+=" -b /proc/"
#uncomment the following line to have access to the home directory of termux
command+=" -w /root"
command+=" /usr/bin/env -i"
command+=" HOME=/root"
command+=" LANG=C.UTF-8"
command+=" PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin:/usr/local/sbin"
command+=" TERM=xterm-256color"
command+=" /bin/{sh} --login"
export PROOT_NO_SECCOMP=1
com="$@"
if [ -z "$1" ];then
    exec $command
else
    $command -c "$com"
fi'''


atilo_home = '{home}/.atilo'.format(home=local.env['HOME'])
atilo_tmp = '{atilo_home}/tmp'.format(atilo_home=atilo_home)
prefix = local.env.get('PREFIX', '')


def tip(s: str) -> None:
    with colors.green:
        print(s)


def warn(s: str) -> None:
    with colors.orange4:
        print(s)


def fatal(s: str) -> None:
    with colors.red:
        print(s)
    exit(1)


def check_req() -> None:
    tip('[ Checking for requirements ... ]')

    reqs = ('tar', 'proot', 'pv', 'curl', 'grep')
    installs = []

    for cmd in reqs:
        try:
            local[cmd]
        except:
            installs.append(cmd)

    pkg = local['apt']
    pkg['install', installs]()


def check_arch() -> str:
    arch = platform.machine()

    if arch == 'aarch64':
        time_arch = 'arm64'
    elif 'arm' in arch:
        time_arch = 'armhf'
    elif arch == 'i686':
        time_arch = 'i386'
    elif arch == 'x86_64':
        time_arch = 'amd64'
    else:
        fatal('[ Unsupported architecture {}'.format(arch))

    return time_arch


def format_url(dist: str, arch: str, version: str) -> str:
    if not dist in support_linux:
        fatal('Disttribution {dist} is not supported'.format(dist))

    distinfo = support_linux[dist]

    if not arch in distinfo:
        fatal('{arch} is not supported for {dist}'.format(dist=dist, arch=arch))

    if not version in distinfo[arch]['versions']:
        warn('{version} is no supported for {dist} {arch}, use {latest} instead'.format(
            dist=dist, arch=arch, version=version, latest=distinfo['latest']))
        version = distinfo['latest']

    return distinfo, distinfo['url'].format(arch=arch, version=version), version


def create_start_script(release_name) -> str:
    execname = 'start' + release_name

    filename = prefix + '/bin/' + execname
    script = start_script.format(release_name=release_name, sh='bash')
    (echo[script] > filename)()
    chmod['+x', filename]()

    return execname


def install_linux(dist: str, arch: str, version: str = ''):
    from plumbum.cmd import tar, proot, pv, curl, grep, bash

    distinfo, url, version = format_url(dist, arch, version)

    os.chdir(atilo_tmp)
    release_name = dist + version
    root = os.path.join(atilo_home, release_name)
    os.makedirs(root, exist_ok=True)

    tip('[ Downloading ... ]')
    if os.path.exists(release_name):
        tip('[ Skip download ]')
    else:
        print(url)
        curl[url, '-o', release_name, '--progress', '-L', '-C', '-'] & FG

    tip('[ Extracting ... ]')
    if 'fedora' in release_name:
        tar['xf', release_name, '--skip-components=1',
            '--exclude', 'json', '--exclude', 'VERSION'] & FG
        (pv['layer.tar'] | proot['tar', 'xpC', root]) & FG
        rm['-f', 'layer.tar'] & FG
        chmod['+w', root] & FG
    else:
        tararg = '{}C'.format(distinfo['zip'])
        (pv[release_name] | proot['tar', tararg, root]) & FG

    tip('[ Configuring ... ]')
    resolvconf = os.path.join(root, 'etc/resolv.conf')
    (echo[name_servers] > resolvconf)()
    profile = os.path.join(root, 'etc/profile')
    (echo['export USER=root'] >> profile)()

    script = create_start_script(release_name)

    tip('[ Updating ... ]')
    bash[script, distinfo['update']] & FG

    tip('[ All done ... ]')
    tip('{} To start'.format(script))


def cmd_install(dist, version):
    # Create dirs
    os.makedirs(atilo_tmp, exist_ok=True)

    arch = check_arch()
    check_req()

    install_linux(dist, arch, version)


class AtiloApp(cli.Application):
    VERSION = '0.1.0'

    def main(self, *args):
        if args:
            print('Unknown command {0!r}'.format(args[0]))
            return 1
        if not self.nested_command:
            print('No command given')
            return 1


@AtiloApp.subcommand('install')
class AtiloInstall(cli.Application):

    def main(self, distribution, version=''):
        cmd_install(distribution, version)


def main():
    AtiloApp.run()


if __name__ == '__main__':
    main()
