# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RegenRadarSettingsDialog
                                 A QGIS plugin
 This plugin loads and shows WMS-T service from KNMI in TimeManager plugin
                             -------------------
        begin                : 2016-07-05
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Marnix de Ridder
        email                : marnix@rivm.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from qgissettingmanager import SettingDialog
from regenradar_settings import RegenRadarSettings

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'regenradar_settings_dialog_base.ui'))


class RegenRadarSettingsDialog(QtGui.QDialog, FORM_CLASS, SettingDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(RegenRadarSettingsDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.settings = RegenRadarSettings()
        SettingDialog.__init__(self, self.settings)