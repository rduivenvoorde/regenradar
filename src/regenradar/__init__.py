# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RegenRadar
                                 A QGIS plugin
 This plugin loads and shows WMS-T service from KNMI in TimeManager plugin
                             -------------------
        begin                : 2016-07-05
        copyright            : (C) 2016 by Marnix de Ridder
        email                : marnix@rivm.nl
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

from qgissettingmanager import *

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load RegenRadar class from file RegenRadar.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .regenradar import RegenRadar
    return RegenRadar(iface)
