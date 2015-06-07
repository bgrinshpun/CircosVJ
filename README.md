# CircosVJ
Custom Circos to visualize V-J cassette usage in T Cell Receptor Repertoire.

The Circos software package can be downloaded from http://circos.ca/
Krzywinski, M. et al. Circos: an Information Aesthetic for Comparative Genomics. Genome Res (2009) 19:1639-1645


Author: Boris Grinshpun, 2015

###### TO RUN DEMO ######
./runcircos.sh -t -i demo.tsv -o demo_result -v 3 -j 4 -n 2 -d PATH_TO_CIRCOS_INSTALL

Results are stored in a newly created demo_result directory


###### FOR HELP WITH OPTIONS #####
./runcircos.sh -h


###### OTHER FILES ######
VJbackground.png <- Custom black background

make_table.py <- Generates a usage counts table from V, J and counts columns

make_circosfiles.py <- Prepare karyotype and link files

etc/ <- This directory contains various circos default layout settings, as well as prebuilt custom color definitions for cassettes : rgb.fulldefA.conf, rgb.fulldefB.conf ; These custom color definitions are included in colors.conf

make_colors.py <- Used to generate custom color maps if needed. Switches to colors_fonts_patterns_new.conf.
colors_fonts_patterns_new.conf reads from colors_new.conf which read from rgb.userdefined.txt








