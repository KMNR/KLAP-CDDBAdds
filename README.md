KLAP-CDDBAdds
====================

Provides windows context tools to make adding a physical disc a breeze
Requirements
====================

This needs the following python libraries

    * musicbrainzngs
    * python-discid
    * winshell
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
    
Acknowledgements
=======================

This software uses modified portions of code from CDDB.py. The file (CDDB.py) has its headers intact. Licensing information for CDDB can be found on its page (http://pycddb.sourceforge.net/). This repository also contains a copy of cdrdao (v1.1.9) which distributed under the GPLv3. A copy of the GPLv3 license is included with this software.

Changelog
=======================

v0.1 - Initial Release

v0.2
    * Added support for extracting data from CD-TEXT and queries on the FreeDB CDDB.
    * Added support for zlib compressing url to allow a greater amount of track data to be sent before the upper limit on url length is met.
    * Fixed handling of CD Stubs for musicbrainz results.
    * Fixed handling CD matches with no releases