"""
Auto-generated File 
Create Time: 2019-12-27 02:33:26
"""
from .ROMEnum_Autogen import *
from renix_py_api.renix_common_api import *
from renix_py_api import rom_manager
from .L47ProtocolConfig_Autogen import L47ProtocolConfig


@rom_manager.rom
class L47ClientConfig(L47ProtocolConfig):
    def delete(self):
        """
        call to delete itself
        """
        return self._finalize()

