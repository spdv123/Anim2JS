# coding=utf-8
from __future__ import print_function
import sys
import json
#from collections.abc import Mapping, Sequence
#from collections import OrderedDict
import ruamel.yaml
from ruamel.yaml.error import YAMLError
import uuid
import optparse


#input_file = '../anims/skill004.anim'
#output_file = './skill004.js'
yaml = ruamel.yaml.YAML()


class ClipTrack:
    def __init__(self):
        self.name = ""
        self.times = []
        self.values = []
        self.type = ""

    @staticmethod
    def get_three_js_track_type(curve_type):
        return {
            "scale": "vector",
            "quaternion": "quaternion",
            "position": "vector",
        }.get(curve_type, "")

    def parse_unity_curve(self, curve, curve_type):
        self.type = self.get_three_js_track_type(curve_type)
        self.name = curve['path'].split('/')[-1] + '.' + curve_type
        for cc in curve['curve']['m_Curve']:
            self.times.append(cc['time'])

            if curve_type == "quaternion":
                self.values.append(cc['value']['x'])
                self.values.append(-cc['value']['y'])
                self.values.append(-cc['value']['z'])
                self.values.append(cc['value']['w'])
            elif curve_type == "position":
                self.values.append(-cc['value']['x'])
                self.values.append(cc['value']['y'])
                self.values.append(cc['value']['z'])
            else:
                self.values.append(cc['value']['x'])
                self.values.append(cc['value']['y'])
                self.values.append(cc['value']['z'])
        return self

    def to_dict(self):
        return {
            "name": self.name,
            "times": self.times,
            "values": self.values,
            "type": self.type
        }


class AnimationClip:
    def __init__(self):
        self.name = ""
        self.duration = 0
        self.tracks = []
        self.uuid = str(uuid.uuid1()).upper()

    def parse_unity_anim(self, anim_data):
        self.duration = anim_data['AnimationClip']['m_AnimationClipSettings']['m_StopTime']\
            - anim_data['AnimationClip']['m_AnimationClipSettings']['m_StartTime']
        self.name = anim_data['AnimationClip']['m_Name']

        for curve in anim_data['AnimationClip']['m_ScaleCurves']:
            self.tracks.append(ClipTrack().parse_unity_curve(curve, "scale"))
        for curve in anim_data['AnimationClip']['m_RotationCurves']:
            self.tracks.append(
                ClipTrack().parse_unity_curve(curve, "quaternion"))
        for curve in anim_data['AnimationClip']['m_PositionCurves']:
            self.tracks.append(
                ClipTrack().parse_unity_curve(curve, "position"))

        return self

    def to_dict(self):
        tracks = []
        for tr in self.tracks:
            tracks.append(tr.to_dict())
        return {
            "name": self.name,
            "duration": self.duration,
            "uuid": self.uuid,
            "tracks": tracks,
        }


def load_anim(anim_fn):
    with open(anim_fn, 'r') as stream:
        try:
            datamap = yaml.load(stream)
            datamap = dict(datamap)
        except YAMLError as exc:
            print(exc)
            exit(-1)
    return datamap


def main():
    hstr = '%prog [options] AnimationClipFile1.anim [AnimationClipFile2.anim [...]]'
    parser = optparse.OptionParser(hstr, description='A simple tool to convert Unity .anim AnimationClips to Three.JS AnimationClips. After converted, you can use them like \"THREE.AnimationClip.parse(anim_AnimationClipName())\" in your JS script.')
    parser.add_option('-o', '--outfile',
                      action="store", dest="out_file",
                      help="where to save the generated .js", default="animations.js")
    parser.add_option('-p', '--prefix',
                      action="store", dest="prefix",
                      help="prefix of JS function to get the AnimationClip, default value is \"anim_\"", default="anim_")

    options, args = parser.parse_args()

    if not args:
        print(parser.format_help())
        exit(0)

    f = open(options.out_file, 'w')
    for in_file in args:
        print("[*] Parsing {}".format(in_file))
        anim_data = load_anim(in_file)
        clip = AnimationClip().parse_unity_anim(anim_data)

        f.write("function " + options.prefix + clip.name + "() {return")
        f.write(json.dumps(clip.to_dict()).replace(' ', ''))
        f.write('}\n')
    f.close()


if __name__ == '__main__':
    main()
