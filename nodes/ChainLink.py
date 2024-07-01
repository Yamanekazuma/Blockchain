import datetime as date
import requests
from urllib.parse import urlparse
import base64
from enum import Enum
from abc import ABCMeta, abstractmethod

from Block import Block

class LinkType(Enum):
    BLOCK = 1
    BRANCH = 2

class ChainLink(metaclass=ABCMeta):
    pass

class ChainLinkBlock(ChainLink):
    def __init__(self, block: Block) -> None:
        self.type = LinkType.BLOCK
        self.blocks = [block]
    
class ChainLinkBranch(ChainLink):
    def __init__(self, blockA: Block, blockB: Block) -> None:
        self.type = LinkType.BRANCH
        self.blocks = [blockA, blockB]
