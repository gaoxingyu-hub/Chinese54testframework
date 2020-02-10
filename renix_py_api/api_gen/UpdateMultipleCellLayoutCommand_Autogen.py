"""
Auto-generated File 
Create Time: 2019-12-27 02:33:25
"""
from .ROMEnum_Autogen import *
from renix_py_api.renix_common_api import *
from renix_py_api import rom_manager
from .ROMCommand_Autogen import ROMCommand


@rom_manager.rom
class UpdateMultipleCellLayoutCommand(ROMCommand):
    def __init__(self, MultipleCellLayoutHandle=None, RowCount=None, ColumnCount=None, ResultViewNodeNames=None, ResultViewNodePaths=None, **kwargs):
        self._MultipleCellLayoutHandle = MultipleCellLayoutHandle  # Layout
        self._RowCount = RowCount  # Row Count
        self._ColumnCount = ColumnCount  # Column Count
        self._ResultViewNodeNames = ResultViewNodeNames  # Result View Node Names
        self._ResultViewNodePaths = ResultViewNodePaths  # Result View Node Paths

        properties = kwargs.copy()
        if MultipleCellLayoutHandle is not None:
            properties['MultipleCellLayoutHandle'] = MultipleCellLayoutHandle
        if RowCount is not None:
            properties['RowCount'] = RowCount
        if ColumnCount is not None:
            properties['ColumnCount'] = ColumnCount
        if ResultViewNodeNames is not None:
            properties['ResultViewNodeNames'] = ResultViewNodeNames
        if ResultViewNodePaths is not None:
            properties['ResultViewNodePaths'] = ResultViewNodePaths

        # call base class function, and it will send message to renix server to create a class.
        super(UpdateMultipleCellLayoutCommand, self).__init__(**properties)

    @property
    def MultipleCellLayoutHandle(self):
        """
        get the value of property _MultipleCellLayoutHandle
        """
        return self._MultipleCellLayoutHandle

    @property
    def RowCount(self):
        """
        get the value of property _RowCount
        """
        return self._RowCount

    @property
    def ColumnCount(self):
        """
        get the value of property _ColumnCount
        """
        return self._ColumnCount

    @property
    def ResultViewNodeNames(self):
        """
        get the value of property _ResultViewNodeNames
        """
        return self._ResultViewNodeNames

    @property
    def ResultViewNodePaths(self):
        """
        get the value of property _ResultViewNodePaths
        """
        return self._ResultViewNodePaths

    @MultipleCellLayoutHandle.setter
    def MultipleCellLayoutHandle(self, value):
        self._MultipleCellLayoutHandle = value

    @RowCount.setter
    def RowCount(self, value):
        self._RowCount = value

    @ColumnCount.setter
    def ColumnCount(self, value):
        self._ColumnCount = value

    @ResultViewNodeNames.setter
    def ResultViewNodeNames(self, value):
        self._ResultViewNodeNames = value

    @ResultViewNodePaths.setter
    def ResultViewNodePaths(self, value):
        self._ResultViewNodePaths = value

    def _set_multiplecelllayouthandle_with_str(self, value):
        self._MultipleCellLayoutHandle = value

    def _set_rowcount_with_str(self, value):
        try:
            self._RowCount = int(value)
        except ValueError:
            self._RowCount = hex(int(value, 16))

    def _set_columncount_with_str(self, value):
        try:
            self._ColumnCount = int(value)
        except ValueError:
            self._ColumnCount = hex(int(value, 16))

    def _set_resultviewnodenames_with_str(self, value):
        tmp_value = value.strip()
        if tmp_value.startswith('{'):
            tmp_value = tmp_value[1:-1]
        self._ResultViewNodeNames = tmp_value.split()

    def _set_resultviewnodepaths_with_str(self, value):
        tmp_value = value.strip()
        if tmp_value.startswith('{'):
            tmp_value = tmp_value[1:-1]
        self._ResultViewNodePaths = tmp_value.split()

