
from PyQt4.QtCore import QObject, QTimer, QDateTime

from qgis.core import QgsVectorLayer, QgsMapLayerRegistry
from qgis.gui import QgsMessageBar
from qgis.utils import plugins

from regenradar_settings import RegenRadarSettings

class RegenRadarControl(QObject):

    def __init__(self, iface):
        """initialize the plugin control. Function gets called even when plugin is inactive"""
        QObject.__init__(self)
        self.iface = iface

    def load(self):
        pass

    def load_knmi(self):
        # KNMI
        # http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi?SERVICE=WMS&&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&LAYERS=RADNL_OPER_R___25PCPRR_L3_COLOR&WIDTH=886&HEIGHT=603&CRS=EPSG%3A3857&BBOX=-725.7203842048766,6434348.070664023,1220725.7203842048,7265651.929335977&STYLES=default&FORMAT=image/png&TRANSPARENT=TRUE&time=2016-06-15T08%3A30%3A00Z
        # http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi?TIME=2016-06-14T09:25:02Z/2016-06-14T10:25:02Z&&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=41607.58263816371618,373175.3892402839847,308340.3808564461069,650052.614857714274&CRS=EPSG:28992&WIDTH=1451&HEIGHT=1507&LAYERS=RADNL_OPER_R___25PCPRR_L3_COLOR&STYLES=&FORMAT=image/png&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi:96&TRANSPARENT=TRUE

        # http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi?SERVICE=WMS&&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&LAYERS=RADNL_OPER_R___25PCPRR_L3_COLOR&WIDTH=886&HEIGHT=603&CRS=EPSG%3A3857&BBOX=-725.7203842048766,6434348.070664023,1220725.7203842048,7265651.929335977&STYLES=default&FORMAT=image/png&TRANSPARENT=TRUE
        # Timestart en end
        # 2016-06-13T18:00:00Z
        # 2016-06-15T18:00:00Z

        if not 'timemanager' in plugins:
            self.iface.messageBar().pushWarning ("Warning!!", "No TimeManger plugin, we REALLY need that. Please install via Plugin Manager first...")
            return

        # development: remove the knmi layer from mapcanvas
        for l in QgsMapLayerRegistry.instance().mapLayersByName("knmi"):
            QgsMapLayerRegistry.instance().removeMapLayer(l)

        tm = plugins['timemanager']

        # TODO try catch this
        from timemanager.layer_settings import LayerSettings
        from timemanager.raster.wmstlayer import WMSTRasterLayer
        #from timemanager.tmlogging import info

        #TODO click on button if not enabled
        if not tm.getController().getTimeLayerManager().isEnabled():
            tm.getController().getGui().dock.pushButtonToggleTime.click()

        # for testing: just remove all timelayers
        tm.getController().timeLayerManager.clearTimeLayerList()

        # # DEZE WERKT NIET !!!!  (?? zelfde probleem als eerder??)
        # url = "http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi?SERVICE=WMS"
        # # DEZE WERKT WEL !!!!
        # url = "http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi"
        # layers = "RADNL_OPER_R___25PCPRR_L3_COLOR"
        # styles = ""
        # imgformat = "image/png"
        # crs = "EPSG:28992"

        settings = RegenRadarSettings()
        name = settings.value("name")
        url = settings.value("url")
        layers = settings.value("layers")
        styles = settings.value("styles")
        imgformat = settings.value("imgformat")
        crs = settings.value("crs")

        # IgnoreGetMapUrl=1&contextualWMSLegend=0&crs=EPSG:28992&dpiMode=7&featureCount=10&format=image/png&layers=RADNL_OPER_R___25PCPRR_L3_COLOR&styles=&url=http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi?

        uri = "crs=" + crs + "&layers=" + layers + "&styles=" + styles + "&format=" + imgformat + "&url=" + url;
        layer = self.iface.addRasterLayer(uri, name, "wms")

        tlayer_settings = LayerSettings()

        # endTimeAttribute !!! NOT toTimeAttribute
        #settings.startTimeAttribute = unicode("2016-06-13T18:00:00Z")
        #settings.endTimeAttribute = unicode("2016-06-15T18:00:00Z")
        DEFAULT_DATE_FORMAT = 'yyyy-MM-ddTHH:mm:ssZ'
        end = QDateTime.currentDateTime().toUTC() # now in UTC
        # prefer 05:00
        time = end.time()
        minute = time.minute()
        time.setHMS(time.hour(), minute-minute%5, 0, 0)
        end.setTime(time)
        tlayer_settings.endTimeAttribute = end.toString(DEFAULT_DATE_FORMAT)
        start = end.addSecs(-2*60*60).toString(DEFAULT_DATE_FORMAT)
        tlayer_settings.startTimeAttribute = start
        # NOK
        # http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi?TIME=2016-07-05T13:45:00Z/2016-07-05T13:50:00Z&&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=-145108.7003207547241,299063.8299999999581,436757.3003207547008,626788.5699999999488&CRS=EPSG:28992&WIDTH=941&HEIGHT=530&LAYERS=RADNL_OPER_R___25PCPRR_L3_COLOR&STYLES=&FORMAT=image/png&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi:96&TRANSPARENT=TRUE

        # OK
        # http://geoservices.knmi.nl/cgi-bin/RADNL_OPER_R___25PCPRR_L3.cgi?TIME=2016-06-13T18:05:00Z/2016-06-13T18:10:00Z&&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=-145108.7003207547241,299063.8299999999581,436757.3003207547008,626788.5699999999488&CRS=EPSG:28992&WIDTH=941&HEIGHT=530&LAYERS=RADNL_OPER_R___25PCPRR_L3_COLOR&STYLES=&FORMAT=image/png&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi:96&TRANSPARENT=TRUE
        #settings.startTimeAttribute = unicode("2016-06-13T18:00:00Z")
        #settings.endTimeAttribute = unicode("2016-06-15T18:00:00Z")

        tlayer_settings.layer = layer

        timelayer = WMSTRasterLayer(tlayer_settings, self.iface)

        # ??
        # iface.mapCanvas().mapCanvasRefreshed.disconnect(tm.getController().waitAfterRenderComplete)
        # iface.mapCanvas().mapCanvasRefreshed.connect(tm.getController().waitAfterRenderComplete)

        # print timelayer
        # print timelayer.getTimeExtents()

        # tm.getController().refreshGuiTimeExtents([
        #    QtCore.QDateTime.fromString("2016-06-13T18:00:00Z", 'yyyy-MM-ddTHH:mm:ssZ'),
        #    QtCore.QDateTime.fromString("2016-06-15T18:00:00Z", 'yyyy-MM-ddTHH:mm:ssZ')])

        animationFrameLength = 2000
        frame_type = 'minutes'
        frame_size = 5
        tm.getController().setPropagateGuiChanges(False)
        tm.getController().setAnimationOptions(animationFrameLength, False, False)

        tm.getController().timeLayerManager.registerTimeLayer(timelayer)

        tm.getController().getGui().setTimeFrameType(frame_type)
        tm.getController().getGui().setTimeFrameSize(frame_size)

        # set layer to zero
        tm.getController().getGui().dock.horizontalTimeSlider.setValue(0)

        # tm.getController().timeLayerManager.refreshTimeRestrictions()

        # tm.getController().getGui().dock.pushButtonPlay.click()

        # plugins['timemanager'].getController().getGui().dock.pushButtonPlay.click()

        QTimer.singleShot(5000, tm.getController().getGui().dock.pushButtonPlay.click)
        #tm.getController().getGui().dock.pushButtonPlay.click()

