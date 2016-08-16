from qgissettingmanager import *

# Working with: https://github.com/3nids/qgissettingmanager
# learning from: https://github.com/3nids/wincan2qgep
# https://github.com/3nids/quickfinder

# KNMI services:

class RegenRadarSettings(SettingManager):

    def __init__(self):

        plugin_name = "RegenRadar/wms-t"

        SettingManager.__init__(self, plugin_name)

        # DEZE WERKT NIET !!!!  (?? zelfde probleem als eerder??)
        url = "http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi?SERVICE=WMS"
        # DEZE WERKT WEL !!!!
        url = "http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi"

        self.add_setting(String("name", Scope.Global, "KNMI regen"))
        self.add_setting(String("url", Scope.Global,
                                "http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi"))
        self.add_setting(String("layers", Scope.Global, "RADNL_OPER_R___25PCPRR_L3_COLOR"))
        self.add_setting(String("styles", Scope.Global, ""))
        self.add_setting(String("imgformat", Scope.Global, "image/png"))
        self.add_setting(String("crs", Scope.Global, "EPSG:28992"))
