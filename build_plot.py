#!/usr/bin/python

import sys
from json import load
from pprint import pprint
import matplotlib.pyplot as plt

AVE_BPP = 'ave_all_frame_bpp'
AVE_QUALITY = 'ave_all_frame_quality'

def main(args):
    #plot_me(args[1])
    correlate(args[1:])

def plot_me(inputs):
    aves, name = find_all_aves(load_json(inputs))
    pprint(aves)
    plot_old(aves)

def load_json(file_name: str):
    j = None
    with open(file_name, 'r') as jsonf:
        j = load(jsonf)
    return j


def correlate(all_files: [str]):
    aves = {}
    for f in all_files:
        averages, name = find_all_aves(load_json(f))
        for dataset, pths in averages.items():
            if dataset not in aves:
                aves[dataset] = {name: pths}
            else:
                aves[dataset][name] = pths
    for dataset, noisy in aves.items():
        plot(noisy, dataset)
    pprint(aves)
    



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
    name = ''
    for k, i in data.items():
        if k == 'name':
            name = i
            continue
        reVal[k] = find_all_for_steaps(i)
    return reVal, name


def plot(d: dict, dataset_name=''):
    '''
    Take a dictionary of datasets and plot each on a single graph.
    d : dictionary of type {dataset_name as str : {'pth':{'ave_all_frame_bpp': 0.000, 'ave_all_frame_quality': 0.00}...}...}
    dataset_name : string of what to make the plots title
    '''
    plots = plt.subplot(1,1,1)
    plots.set_title(dataset_name)
    plots.grid(True)
    colors = ['go', 'ro', 'bo', 'yo']
    for name, pths in d.items():
        bpp = []
        quality = []
        for pth, nums in pths.items():
            bpp.append(nums[AVE_BPP])
            quality.append(nums[AVE_QUALITY])
        plots.plot(bpp, quality, colors.pop(), linestyle='solid', label=name)
    plots.legend()
    plots.set_xlabel('BPP')
    plots.set_ylabel('MS-SSIM')
    plt.savefig(f'{dataset_name}-noisy.png', bbox_inches='tight')
    plt.clf()
    #plt.show()




def plot_old(d: dict, dataset_name=''):
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
