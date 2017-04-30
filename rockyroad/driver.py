import errno
import glob
import platform
import re
import sys
import tempfile
import zipfile
from contextlib import contextmanager
from distutils.version import StrictVersion

import os
import requests
from xml.etree import ElementTree

IS_64_BIT = sys.maxsize > 2**32

IS_LINUX = platform.system().lower() == 'linux'

IS_WINDOWS = platform.system().lower() == 'windows'

IS_MAC = platform.system().lower() == 'darwin'

UNKNOWN_PLATFORM = not IS_LINUX and not IS_WINDOWS

REPO_DIR = os.path.join(os.path.expanduser('~'), '.rockyroad')


@contextmanager
def download_file(url):
    """
    Download a remote file to a temporary location.
    :param url: the file url
    """
    resp = requests.get(url, stream=True)
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        name = fp.name
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fp.write(chunk)
    yield name
    fp.close()


def _mkdirp(dirpath):
    try:
        os.makedirs(dirpath)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dirpath):
            pass


def _get_xml_ns(uri):
    m = re.match(r'\{.*?\}', uri)
    return m.group(0) if m else ''


class Driver:
    version = None
    bit = None
    repo_dir = os.path.join(os.path.expanduser('~'), '.rockyroad')

    def __init__(self, version=None, bit=None):
        if version:
            self.version = str(version)

        if not bit:
            self.bit = '64' if IS_64_BIT else '32'
        else:
            self.bit = str(bit)

        if hasattr(self, 'setup'):
            self.setup()

    def download(self):
        """Download the driver binary"""
        raise NotImplementedError('You must implement download()')

    def binary_path(self):
        """The absolute path to the driver binary"""
        raise NotImplementedError('You must implement binary_path()')

    def path(self):
        """
        The absolute path to the driver
        :return: 
        """
        if not os.path.exists(self.binary_path()):
            self.download()

        return self.binary_path()


class ChromeDriver(Driver):

    versions = {}
    _bin_path = None

    def setup(self):
        url = 'https://chromedriver.storage.googleapis.com/'
        resp = requests.get(url)
        tree = ElementTree.fromstring(resp.content)
        ns = _get_xml_ns(tree.tag)
        for elem in tree.findall('%sContents' % ns):
            key = elem.find('%sKey' % ns)
            m = re.match('^([\d.]+?)/chromedriver_(linux|mac|win)(32|64)', key.text)
            if m:
                v = m.group(1)  # version
                p = m.group(2)  # platform
                b = m.group(3)  # bit

                if v not in self.versions:
                    self.versions[v] = {}
                if p not in self.versions[v]:
                    self.versions[v][p] = {}

                self.versions[v][p][b] = url + key.text

    @property
    def _platform(self):
        if IS_WINDOWS:
            return 'win'
        elif IS_LINUX:
            return 'linux'
        elif IS_MAC:
            return 'mac'
        else:
            raise RuntimeError('Unable to detect current platform')

    def binary_path(self):
        if self._bin_path:
            return self._bin_path

        if self.version and self.version not in self.versions:
            raise RuntimeError('Chromedriver %s does not exist' % self.version)

        if not self.version:
            numbers = list(self.versions.keys())
            numbers.sort(key=StrictVersion, reverse=True)
            self.version = numbers[0]

        bin_name = 'chromedriver.exe' if IS_WINDOWS else 'chromedriver'

        self._bin_path = os.path.join(REPO_DIR, 'chromedriver', '%s-%s%s' %
                                      (self.version, self._platform, self.bit,),
                                      bin_name)

        return self._bin_path

    def download(self):
        url = self.versions[self.version][self._platform][self.bit]
        destination_dir = ''.join(self._bin_path.split(os.pathsep))
        with download_file(url) as name:
            _mkdirp(destination_dir)
            z = zipfile.ZipFile(name, 'r')
            z.extractall(destination_dir)
            z.close()

        for filename in glob.iglob(destination_dir + '/*'):
            os.chmod(filename, 777)


def download_chromedriver(version=None, bit=None):
    """
    Download the chromedriver binary.
    
    If version is not set, then it will get the latest one. If the bit value is
    not set then it will use the same value as the current system
    """
    url = 'https://chromedriver.storage.googleapis.com/'
    resp = requests.get(url)
    tree = ElementTree.fromstring(resp.content)
    ns = _get_xml_ns(tree.tag)

    if version:
        version = str(version)

    if bit:
        bit = str(bit)
    else:
        bit = '64' if IS_64_BIT else '32'

    versions = {}

    for elem in tree.findall('%sContents' % ns):
        key = elem.find('%sKey' % ns)
        m = re.match('^([\d.]+?)/chromedriver_(linux|mac|win)(32|64)', key.text)
        if m:
            v = m.group(1)  # version
            p = m.group(2)  # platform
            b = m.group(3)  # bit

            if v not in versions:
                versions[v] = {}
            if p not in versions[v]:
                versions[v][p] = {}

            versions[v][p][b] = url + key.text

    if version and version not in versions:
        raise RuntimeError('Chromedriver %s is not a valid version' % version)

    if IS_WINDOWS:
        p = 'win'
    elif IS_LINUX:
        p = 'linux'
    elif IS_MAC:
        p = 'mac'
    else:
        raise RuntimeError('Unable to detect current platform')

    if version:
        if bit is None:
            download_url = versions[version][p][bit]
        elif bit not in versions[version][p]:
            raise RuntimeError('Invalid bit value %s' % bit)
        else:
            download_url = versions[version][p][bit]
    else:
        # get latest version
        numbers = list(versions.keys())
        numbers.sort(key=StrictVersion, reverse=True)
        version = numbers[0]
        download_url = versions[version][p][bit]

    destination_dir = os.path.join(REPO_DIR, 'chromedriver',
                                   '%s-%s%s' % (version, p, bit,))

    if os.path.isdir(destination_dir):
        return destination_dir

    # download an unzip to repo directory
    with download_file(download_url) as name:
        _mkdirp(destination_dir)
        z = zipfile.ZipFile(name, 'r')
        z.extractall(destination_dir)
        z.close()

    for filename in glob.iglob(destination_dir + '/*'):
        os.chmod(filename, 777)

    return destination_dir


def get_binary(name, arch=None, version=None):
    """
    Get the driver binary.
    
    This will check the cache location to see if it has already been downloaded
    and return its path. If it is not in the cache then it will be downloaded.
    :param name: the binary name chromedriver, 
    :param arch: 
    :param version: 
    :return: 
    """