"""
Auto-generated File 
Create Time: 2019-12-27 02:33:25
"""
from .ROMEnum_Autogen import *
from renix_py_api.renix_common_api import *
from renix_py_api import rom_manager
from .CreateChartResultViewCommand_Autogen import CreateChartResultViewCommand


@rom_manager.rom
class CreateChartResultViewExCommand(CreateChartResultViewCommand):
    def __init__(self, **kwargs):
        self._ResultSeriesHandles = None  # Result Series, not editable

        properties = kwargs.copy()

        # call base class function, and it will send message to renix server to create a class.
        super(CreateChartResultViewExCommand, self).__init__(**properties)

    @property
    def ResultSeriesHandles(self):
        """
        get the value of property _ResultSeriesHandles
        """
        return self._ResultSeriesHandles

    def _set_resultserieshandles_with_str(self, value):
        tmp_value = value.strip()
        if tmp_value.startswith('{'):
            tmp_value = tmp_value[1:-1]
        self._ResultSeriesHandles = tmp_value.split()

    def _set_output_property(self, value):
        self._set_resultserieshandles_with_str(value)

