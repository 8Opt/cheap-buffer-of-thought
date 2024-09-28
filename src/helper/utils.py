"Building helper functions"

import io
import os
import json
import logging
import binascii
import urllib
import ipaddress

from os import PathLike
from pathlib import Path
from typing import Any, Union, Optional
from base64 import b64encode, b64decode

from src.helper.schema import RequestError


def json_read(path): 
    "Reading json files"
    allowed_tails = ['json,', 'jsonl']
    path_tail = path.split('.')[-1]
    if path_tail in allowed_tails: 
        result = json.loads(open(path, 'r',  encoding="utf-8"))
        return result
    
class DualHandler(logging.Handler):
    "Setup configuration for logger"
    def __init__(self, dir:str='log',filename=None, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self.console_handler = logging.StreamHandler()
        self.file_handler = logging.FileHandler(os.path.join(dir, filename), mode='a')
        self.formatter = logging.Formatter('[%(asctime)s] - %(levelname)7s --- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.console_handler.setFormatter(self.formatter)
        self.file_handler.setFormatter(self.formatter)

    def emit(self, record):
        self.console_handler.emit(record)
        self.file_handler.emit(record)

def set_logger(provider:str, model_name:str, level:int=logging.DEBUG) -> logging.Logger:
    "Build logger"
    logger = logging.getLogger(__name__)
    logger.handlers.clear() # Clear existing handlers
    logger.setLevel(level)

    file_path = f"{provider}_{model_name}.log"
    dual_handler = DualHandler(file_path)
    logger.addHandler(dual_handler)

    return logger


def _encode_image(image) -> str:
    if p := _as_path(image):
        return b64encode(p.read_bytes()).decode('utf-8')

    try:
        b64decode(image, validate=True)
        return image if isinstance(image, str) else image.decode('utf-8')
    except (binascii.Error, TypeError):
        ...

    if b := _as_bytesio(image):
        return b64encode(b.read()).decode('utf-8')

    raise RequestError('image must be bytes, path-like object, or file-like object')


def _as_path(s: Optional[Union[str, PathLike]]) -> Union[Path, None]:
  if isinstance(s, str) or isinstance(s, Path):
    try:
      if (p := Path(s)).exists():
        return p
    except Exception:
      ...
  return None


def _as_bytesio(s: Any) -> Union[io.BytesIO, None]:
  if isinstance(s, io.BytesIO):
    return s
  elif isinstance(s, bytes):
    return io.BytesIO(s)
  return None

def _parse_host(host:Optional[str]) -> str: 
    host, port = host or '', 11434
    scheme, _, hostport = host.partition('://')
    if not hostport:
        scheme, hostport = 'http', host
    elif scheme == 'http':
        port = 80
    elif scheme == 'https':
        port = 443

    split = urllib.parse.urlsplit('://'.join([scheme, hostport]))
    host = split.hostname or '127.0.0.1'
    port = split.port or port

    # Fix missing square brackets for IPv6 from urlsplit
    try:
        if isinstance(ipaddress.ip_address(host), ipaddress.IPv6Address):
            host = f'[{host}]'
    except ValueError:
        ...

    if path := split.path.strip('/'):
        return f'{scheme}://{host}:{port}/{path}'

    return f'{scheme}://{host}:{port}'