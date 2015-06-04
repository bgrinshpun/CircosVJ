#!/bin/sh

# MAKE A CIRCOS PLOT
# show help if no arguments are passed


function usage() {
    scriptname=`basename $0`
    echo >&2
    echo "$scriptname: Generate a circos plot of T cell V-J cassette usage" >&2
    echo >&2 
    echo USAGE: >&2
    echo "  " $scriptname [-t columnnames] [-i input_file] [-o output_name] [-d path to Circos installation ] [-v Vcassetteindex] [-j Jcassetteidex] [-n Countsindex] [-a output_level] [-c colormap]  >&2
    echo >&2
    echo >&2 "INPUTS"
    echo >&2 "\t-t: Include only if the first line of the file consits of column names"
    echo >&2
    echo >&2 "\t-i: Specify an input file containing at least three columns, one for V cassettes, one for J cassettes, and one for the counts. It is not necessary to merge counts if multiple identical V,J entries exist."	
    echo >&2
    echo >&2 "\t-o: Output name. A directory with this name will be created, and all created files will be based off of this name. Default [output]"
    echo >&2
    echo >&2 "\t-d: Path to the Circos installation. It is up to the user to have a working download of the Circos software"
    echo >&2
    echo >&2 "\t-v Column number of V cassettes"
    echo >&2
    echo >&2 "\t-j Column number of J cassettes"
    echo >&2
    echo >&2 "\t-n Column number of VJ usage counts"
    echo >&2
    echo >&2 "\t-a Output level:
	 	1: Keep only the Circos plot
		2: Keep karyotype and link files
		3: Keep all intermediate files"
    echo >&2
    echo >&2 "\t-c Make a new custom colormap for V and J cassettes.
		Input should be 'A' or 'B'."
    echo >&2
    echo >&2 "OUTPUTS:"
    echo >&2 "\tStandard png and svg files produced by Circos, as well as intermediate files based on the -a flag. All files contained in a folder with name specified by the -o flag."
    echo >&2
    echo >&2 "RUN DEMO"
    echo >&2 "./runcircos.sh -t -i demo.tsv -o demo_result -v 3 -j 4 -n 2 -d PATH_TO_CIRCOS_INSTALL" >&2
    echo >&2
    echo >&2
    echo "Author: Boris Grinshpun (bg2178@columbia.edu), 2015"
    echo >&2
}

if [ $# -lt 1 ] 
    then
    usage
    exit 1
fi

colnames=0
# process options
while getopts thi:o:d:v:j:n:a:c: opt
  do
  case "$opt" in
      t) colnames=1 ;;
      i) file=$OPTARG ;;
      o) output=$OPTARG ;;
      d) CIRCOS=$OPTARG ;;
      v) vpos=$OPTARG ;;
      j) jpos=$OPTARG ;;
      n) npos=$OPTARG ;;
      a) outlevel=$OPTARG ;;
      c) makecolor=$OPTARG ;;
      h) usage; exit 1 ;;
      ?) usage; exit 1 ;;
  esac
done

shift $((OPTIND - 1))

if [ -z $file ]; then
    echo "Missing input file"  >&2
    echo >&2
    echo "Run '`basename $0` -h'  for help" 
    echo >&2
    exit 1
fi

if [ ! -s $file ]; then
    echo "Cannot find input file "  >&2
    echo >&2
    echo "Run '`basename $0` -h' for help" 
    echo >&2
    exit 1
fi

if [ -z $CIRCOS ]; then
    echo "Need path to CIRCOS binary" >&2
    echo >&2
    echo "Run '`basename $0` -h' for help" 
    echo >&2
    exit 1
fi

if [ ! -x $CIRCOS ]; then
    echo "Cannot find CIRCOS binary" >&2
    echo >&2
    echo "Run '`basename $0` -h' for help" 
    echo >&2
    exit 1
fi

[ -z $output ] && output="output";

outpath=$output/$output
mkdir -p $output

colorfile="colors_fonts_patterns"
cp -r etc $output
if [ ! -z $makecolor ]; then
    if [ $makecolor == "A" ]; then
	python make_colors.py $file $[$vpos-1] $[$jpos-1] > $output/etc/rgb.userdefined.conf
	colorfile="colors_fonts_patterns_new"
    elif [ $makecolor == "B" ]; then
	python make_colors.py $file $[$vpos-1] $[$jpos-1] > $output/etc/rgb.userdefined.conf
	colorfile="colors_fonts_patterns_new"
    else
	echo "$makecolor is an INVALID OPTION"
	echo
	echo "Proceeding with default color definitions"
	echo
    fi
fi

# Generate VJ table, karyotype and link files
tablefile=$outpath.table.txt
karyotypefile=$outpath.karyo.txt
linkfile=$outpath.links.txt

# Generate necessary input files to Circos software
python make_table.py $file $[$vpos-1] $[$jpos-1] $[$npos-1] $colnames $tablefile
python make_circosfiles.py $tablefile $karyotypefile $linkfile

# Produce circos input file from templates
sed "s:%FILE%:$karyotypefile:" plotmain_template.conf | sed "s:%colorfile%:$colorfile:" > $output/plotmain.conf
sed "s:%FILE%:$linkfile:" links_template.conf > $output/links.conf

# Make the Circos
perl $CIRCOS -conf $output/plotmain.conf -outputfile $outpath


# Control output level
if [ ! -z $outlevel ]; then
	if [ $outlevel -eq 1 ]; then
		rm $output/plotmain.conf
		rm $output/links.conf
		rm $tablefile
		rm -r $output/etc
	elif [ $outlevel -eq 2 ]; then
		rm $output/plotmain.conf
		rm $output/links.conf
		rm $tablefile
		rm $linkfile
		rm $karyotypefile
		rm -r $output/etc
	fi
fi
