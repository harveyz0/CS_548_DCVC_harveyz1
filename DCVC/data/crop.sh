#!/bin/bash
set -x

NAME="$0"

function convert {
    orig_video="$1"
    if [ ! -f "$orig_video" ] ; then
        echo "ERROR : Can not find video $orig_video"
        return
    fi
    name="$2"
    out_dir="${3}/${name}_1920x1024_120fps_420_8bit_YUV"
    noise="$4"

    out_video="${out_dir}/${name}_1920x1024_50.yuv"
    if [ ! -d "$out_dir" ] ; then
        mkdir -p "$out_dir"
    fi
    case $noise in
        "1")
            lite_noise "$orig_video" "${out_video}"
            ;;
        "2")
            high_noise "$orig_video" "${out_video}"
            ;;
        "3")
            rolling_noise "$orig_video" "${out_video}"
            ;;
        *)
            ffmpeg -pix_fmt yuv420p  -s 1920x1080 -i "$orig_video" -vf crop=1920:1024:0:0 "$out_video"
            ;;
    esac
    ffmpeg -pix_fmt yuv420p -s 1920x1024 -i "${out_video}" -f image2 "${out_dir}/im%05d.png"
}

function lite_noise {
    ffmpeg -pix_fmt yuv420p -s 1920x1080 -i $1 -vf crop=1920:1024:0:0 -bsf:v noise=100 $2
}
function high_noise {
    ffmpeg -pix_fmt yuv420p -s 1920x1080 -i $1 -vf crop=1920:1024:0:0 -bsf:v noise=10 $2
}

function rolling_noise {
    echo "ROLLING NOTHING"
    #ffmpeg -pix_fmt yuv420p -s 1920x1080 -i $1 -bsf:v noise $2
    ffmpeg -pix_fmt yuv420p -s 1920x1024 -i $1 -codec:v copy "${2}"
    #ffmpeg -pix_fmt yuv420p  -s 1920x1080 -i "$2" -vf crop=1920:1024:0:0 "${1}_cropped_noise.yuv"
}

function main {
    # https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash
    # Because I can never remember how to do this in bash
    OUTDIR=""
    INDIR=""
    NOISE_LEVEL="0"
    while [[ $# -gt 0 ]]; do
        case $1 in
            -o|--outdir)
                OUTDIR="$2"
                shift
                shift
                ;;
            -i|--indir)
                INDIR="$2"
                shift
                shift
                ;;
            -n|--noise)
                NOISE_LEVEL="$2"
                shift
                shift
                ;;
            -*|--*|*)
                echo "Unknown argument $1"
                help $NAME
                ;;
        esac
    done
    if [ "x$OUTDIR" = "x" ] ; then
        echo "ERROR : No output directory specified"
        help
    elif [ "x$INDIR" = "x" ] ; then
        echo "ERROR : No input directory specified"
        help
    fi
    for f in ${INDIR}/*.yuv
    do
        name=$(basename "$f" | cut -d _ -f 1)
        convert "$f" "$name" "$OUTDIR" "$NOISE_LEVEL"
    done
}

function help {
    echo "Usage $0"
    echo "      $0 --outdir output_directory --indir input_directory [--noise 1-3]"
    echo "  --outdir output_directory : The directory to write the converted videos too"
    echo "  --indir input_directory : The directory containing matching *.yuv files"
    echo "  --noise 1-3 : How much noise to build, 1 is lite, 2 is high, 3 is a high rolling noise"
    echo "                If noise is absent then only the cropping will be applied"
    exit 1
}

main $*
