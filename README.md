Anim2JS
-------
A simple tool to convert Unity .anim AnimationClips to Three.JS AnimationClips.

After converted, you can use them like below
```js
THREE.AnimationClip.parse(anim_AnimationClipName())
```
in your JS script.

Usage
-----
From command line:

    $ python anim2js.py
    Usage: anim2js.py [options] AnimationClipFile1.anim [AnimationClipFile2.anim [...]]
    A simple tool to convert Unity .anim AnimationClips to Three.JS
    AnimationClips. After converted, you can use them like
    "THREE.AnimationClip.parse(anim_AnimationClipName())" in your JS script.

    Options:
        -h, --help            show this help message and exit
        -o OUT_FILE, --outfile=OUT_FILE
                        where to save the generated .js
        -p PREFIX, --prefix=PREFIX
                        prefix of JS function to get the AnimationClip,
                        default value is "anim_"

Example
-----

Convert ```Hello001.anim``` and ```Hello002.anim``` to ```hello.js```

```sh
python anim2js.py examples/Hello001.anim examples/Hello002.anim -o hello.js
```

And after import ```hello.js``` you can use them as below

```js
var clip_hello001 = THREE.AnimationClip.parse(anim_Hello001())
var clip_hello002 = THREE.AnimationClip.parse(anim_Hello002())
```

Requirements
-----

```
ruamel.yaml
```

install them via

```sh
pip install ruamel.yaml
```

License
-----

LGPL v3.0
