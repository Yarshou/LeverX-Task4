import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml


class FileDump(ABC):

    @abstractmethod
    def dump(self, data):
        pass


class JSONDump(FileDump):

    def dump(self, data):
        return json.dumps(data, sort_keys=True, indent=2)


class XMLDump(FileDump):

    def dump(self, data):
        result = dicttoxml(data, custom_root='Rooms', attr_type=False)
        return parseString(result).toprettyxml()
