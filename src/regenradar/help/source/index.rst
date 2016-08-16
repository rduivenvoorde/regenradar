.. RegenRadar documentation master file, created by
   sphinx-quickstart on Sun Feb 12 17:11:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation
=============

Contents:

.. toctree::
   :maxdepth: 2


What does it do
---------------

The RegenRadar plugin is a plugin which:

- loads a configured WMS-T service layer (typically the KNMI precipitation) for the last x (where x is a setting) hours
- checks if TimeManager plugin is installed
- then configures the TimeManager plugin to start 'animating' the layer
- making QGIS retrieve the WMS images given the TimeManager properties and showing an 'animated' map

The plugin typically shows one layer.

Using the settings dialog you can instruct the plugin to use another WMS-T layer

Make it work
------------

Install both(!!!) the Regenradar plugin and the TimeManager plugin using QGIS Plugin Manager.

Make sure both plugins are active.

Click the little 'cloud' button

.. image:: _static/pluginbutton.png

to load the precipitation of last 2 hours in colors and start the animating.

Optionally change settings to use another WMS-T service via the SettingsDialog:
(/web/Regenradar/Show RainRadar Settings)

.. image:: _static/settingdialog.png


How does it work
----------------

RegenRadarSettings (regen_radar_settings.py)
............................................

The plugin makes use of the generic 'Settings' framework of https://github.com/3nids/qgissettingmanager.
That is it uses the `RegenRadarSettings` class to both define the settings to be used, as to define the type and
name of the settings. This framework also makes sure that the settings are made persistent by saving them to the
QSettings (as /plugins/RegenRadar/wms-t/xxx)

RegenRadar (regenradar.py)
..........................

The actual plugin class, which inits the gui and makes loading in QGIS as a plugin possible.

It instantiates one RegenRadarControl instance which is actually the working horse and does the work.

RegenRadarControl (regenradar_control.py)
.........................................

This class checks if the TimeManager plugin (https://github.com/anitagraser/TimeManager) is available and
active by checking the plugins['timemanager'] context.
Without this plugin the RegenRadar plugin is not started.

It will create a WMS-raster layer (using the settings) in QGIS and add it to the layer list.

It will configure the TimeManager with appropriate values and start animation of that layer.

RegenRadarSettingsDialog (regenradar_settings_dialog.py)
........................................................

The python class that creates the settings dialog. Note that this also has `SettingDialog` as base class,
needed to make the QgisSettingManager work.

RegenRadarDialog (regenradar_dialog.py)
.......................................

Python class used to initiate a dialog here (not used in this plugin)

Future work
-----------

Currently it works in fixed (5 minute) timesteps (because that is what KNMI currently uses).

We work around a TimeManager plugin issue which make the plugin start several threads loading images when you
move the time slider.

The TimeManager plugin reacts to every pixel move of the time slider, while in the case of (often slower)
WMS services it is probably better to use only the event on the end of the movement.


