__version__ = "1.0"

from meshroom.core import desc
import os.path

currentDir = os.path.dirname(os.path.abspath(__file__))

class RenderAnimatedCamera(desc.CommandLineNode):
    commandLine = '{blenderPathValue} -b --python {scriptPathValue} -- {allParams}'

    inputs = [
        desc.File(
            name='blenderPath',
            label='Blender Path',
            description='''Path to blender binary.''',
            value=os.environ.get('BLENDER',"C:/Program Files/Blender Foundation/Blender 2.91/blender.exe"),
            uid=[],
            group='',
        ),
        desc.File(
            name='scriptPath',
            label='Script Path',
            description='''Path to blender binary.''',
            value=os.path.join(currentDir, 'scripts' ,'camera_support.py'),
            uid=[],
            group='',
        ),
        desc.File(
            name='sfMCameraPath',
            label='Camera Path',
            description='''Input Camera path from the sfm.''',
            value='',
            uid=[0],
        ),
        desc.File(
            name='sfMData',
            label='SFM Data',
            description='''Input the previously used SFM Data.''',
            value='',
            uid=[0],
        ),
        desc.File(
            name='undistortedImages',
            label='Images Folder',
            description='''Input the processed images.''',
            value='',
            uid=[0],
        ),
    ]

    outputs = [
        desc.File(
            name='outputPath',
            label='Output Video',
            description='''Output folder.''',
            value=desc.Node.internalFolder, # PLACE HOLDER TO CHANGE
            uid=[],
        )
    ]