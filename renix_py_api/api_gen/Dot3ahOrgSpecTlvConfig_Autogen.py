"""
Auto-generated File 
Create Time: 2019-12-27 02:33:27
"""
from .ROMEnum_Autogen import *
from renix_py_api.renix_common_api import *
from renix_py_api import rom_manager
from .ROMObject_Autogen import ROMObject


@rom_manager.rom
class Dot3ahOrgSpecTlvConfig(ROMObject):
    def __init__(self, OrgUniqueId=None, Data=None, **kwargs):
        self._OrgUniqueId = OrgUniqueId  # Organization Unique ID
        self._Data = Data  # Data

        properties = kwargs.copy()
        if OrgUniqueId is not None:
            properties['OrgUniqueId'] = OrgUniqueId
        if Data is not None:
            properties['Data'] = Data

        # call base class function, and it will send message to renix server to create a class.
        super(Dot3ahOrgSpecTlvConfig, self).__init__(**properties)

    def delete(self):
        """
        call to delete itself
        """
        return self._finalize()

    def edit(self, OrgUniqueId=None, Data=None, **kwargs):
        properties = kwargs.copy()
        if OrgUniqueId is not None:
            self._OrgUniqueId = OrgUniqueId
            properties['OrgUniqueId'] = OrgUniqueId
        if Data is not None:
            self._Data = Data
            properties['Data'] = Data

        super(Dot3ahOrgSpecTlvConfig, self).edit(**properties)

    @property
    def OrgUniqueId(self):
        """
        get the value of property _OrgUniqueId
        """
        if self.force_auto_sync:
            self.get('OrgUniqueId')
        return self._OrgUniqueId

    @property
    def Data(self):
        """
        get the value of property _Data
        """
        if self.force_auto_sync:
            self.get('Data')
        return self._Data

    @OrgUniqueId.setter
    def OrgUniqueId(self, value):
        self._OrgUniqueId = value
        self.edit(OrgUniqueId=value)

    @Data.setter
    def Data(self, value):
        self._Data = value
        self.edit(Data=value)

    def _set_orguniqueid_with_str(self, value):
        tmp_value = value.strip()
        if tmp_value.startswith('{'):
            tmp_value = tmp_value[1:-1]
        self._OrgUniqueId = []
        values = tmp_value.split()
        for str_value in values:
            try:
                self._OrgUniqueId.append(int(str_value))
            except ValueError:
                self._OrgUniqueId.append(hex(int(str_value, 16)))

    def _set_data_with_str(self, value):
        tmp_value = value.strip()
        if tmp_value.startswith('{'):
            tmp_value = tmp_value[1:-1]
        self._Data = []
        values = tmp_value.split()
        for str_value in values:
            try:
                self._Data.append(int(str_value))
            except ValueError:
                self._Data.append(hex(int(str_value, 16)))

