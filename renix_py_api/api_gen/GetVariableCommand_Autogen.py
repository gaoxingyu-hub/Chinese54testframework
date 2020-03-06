"""
Auto-generated File 
Create Time: 2019-12-27 02:33:26
"""
from .ROMEnum_Autogen import *
from renix_py_api.renix_common_api import *
from renix_py_api import rom_manager
from .ROMCommand_Autogen import ROMCommand


@rom_manager.rom
class GetVariableCommand(ROMCommand):
    def __init__(self, VariableName=None, VariableType=None, **kwargs):
        self._VariableName = VariableName  # Variable Name
        self._VariableValue = '0'  # Variable Value, not editable
        self._VariableType = VariableType  # Variable Type

        properties = kwargs.copy()
        if VariableName is not None:
            properties['VariableName'] = VariableName
        if VariableType is not None:
            properties['VariableType'] = VariableType

        # call base class function, and it will send message to renix server to create a class.
        super(GetVariableCommand, self).__init__(**properties)

    @property
    def VariableName(self):
        """
        get the value of property _VariableName
        """
        return self._VariableName

    @property
    def VariableValue(self):
        """
        get the value of property _VariableValue
        """
        return self._VariableValue

    @property
    def VariableType(self):
        """
        get the value of property _VariableType
        """
        return self._VariableType

    @VariableName.setter
    def VariableName(self, value):
        self._VariableName = value

    @VariableType.setter
    def VariableType(self, value):
        self._VariableType = value

    def _set_variablename_with_str(self, value):
        self._VariableName = value

    def _set_variablevalue_with_str(self, value):
        self._VariableValue = value

    def _set_variabletype_with_str(self, value):
        seperate = value.find(':')
        exec('self._VariableType = EnumVariableType.%s' % value[:seperate])

    def _set_output_property(self, value):
        self._set_variablevalue_with_str(value)

