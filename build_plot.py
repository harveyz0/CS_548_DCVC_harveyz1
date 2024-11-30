#!/usr/bin/python

import sys
from json import load
from pprint import pprint
import matplotlib.pyplot as plt

AVE_BPP = 'ave_all_frame_bpp'
AVE_QUALITY = 'ave_all_frame_quality'

def main(args):
    inputs = args[1]
    j = None
    with open(inputs, 'r') as jsonf:
        j = load(jsonf)
    aves = find_all_aves(j)
    plot(aves)


def find_all_for_steaps(data: dict):
    steps = {}
    for _, pths in data.items():
        for pth, vals in pths.items():
            if pth not in steps:
                steps[pth] = {AVE_BPP: [], AVE_QUALITY: []}
            steps[pth][AVE_BPP].append(vals[AVE_BPP])
            steps[pth][AVE_QUALITY].append(vals[AVE_QUALITY])
    reVal = {}
    for pth, vals in steps.items():
        if pth not in reVal:
            reVal[pth] = {}
        reVal[pth][AVE_QUALITY] = sum(vals[AVE_QUALITY]) / len(vals[AVE_QUALITY])
        reVal[pth][AVE_BPP] = sum(vals[AVE_BPP]) / len(vals[AVE_BPP])

    return reVal

def find_all_aves(data: dict):
    reVal = {}
    for k, i in data.items():
        reVal[k] = find_all_for_steaps(i)
    return reVal


def plot(d: dict, dataset_name=''):
    p = 1
    for dataset, data in d.items():
        bpp = []
        quality = []
        for pth, d in data.items():
            for name, val in d.items():
                if name == AVE_QUALITY:
                    quality.append(val)
                elif name == AVE_BPP:
                    bpp.append(val)
                else:
                    raise ValueError(f'Got {name} for a named value')

        plots = plt.subplot(1, 2, p)
        p += 1
        plots.plot(bpp, quality, 'go', linestyle='solid')
        plots.set_title(dataset)

        plots.grid(True)
        if 'MCL-JCV' == dataset_name:
            plots.axis([0.03, 0.33, 0.950, 0.990])
        elif 'UVG' == dataset_name:
            plots.axis([0.04, 0.36, 0.950, 0.990])
        #plt.suptitle(dataset_name)
        #return plots
    plt.show()


def find_ave(data: dict):
    '''
    Loop through all the input video listed
    in the dictionary and get all the averages.
    data : dictionary of form
    {"VIDEO FILE": 
        {"model_dcvc_quality_N_...":
            {AVE_BPP: 0.9999, AVE_QUALITY: 0.999,...}...},
        ...}
    '''
    final_bpp = 0.0
    final_quality = 0.0
    key_len = len(data.keys())
    for _, v in data.items():
        last = sorted(v.keys(), reverse=True)[0]
        final_bpp += v[last][AVE_BPP]
        final_quality += v[last][AVE_QUALITY]
    return {AVE_BPP: final_bpp / key_len, AVE_QUALITY: final_quality / key_len}


if __name__ == "__main__":
    main(sys.argv)
