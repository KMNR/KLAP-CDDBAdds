KLAP-CDDBAdds
====================

Provides windows context tools to make adding a physical disc a breeze
Requirements
====================

This needs the following python libraries

    * musicbrainzngs
    * python-discid
    * py2exe
    
Creating the installer needs InnoSetup. python-discid needs a copy of the libdiscid dll (discid.dll) which is included with the source.

Creating The Installer
=====================
To create the installer, first run the following command

    python setup.py py2exe
    
Which creates the standalone executable.

Then use InnoSetup on the "installer.iss" to build the setup application

Using the setup utility will automatically create the shortcuts in windows explorer.

Using This Tool
======================

    1. Right click on a CD drive and choose "Add To KLAP"
    1. A window will open and report any problems. If there are no problems, it will close immediately.
    1. KLAP will open in your default browser and allow you to create the entry.
   
Limitations
=======================

    * For CDs with a limited number of tracks, or releases that suck, this tool may show incorrect information or won't find any at all.