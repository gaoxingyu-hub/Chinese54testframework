"""
Auto-generated File 
Create Time: 2019-12-27 02:33:28
"""
from .ROMEnum_Autogen import *
from renix_py_api.renix_common_api import *
from renix_py_api import rom_manager
from .WizardConfigBase_Autogen import WizardConfigBase


@rom_manager.rom
class MplsVpnWizardConfig(WizardConfigBase):
    def delete(self):
        """
        call to delete itself
        """
        return self._finalize()

