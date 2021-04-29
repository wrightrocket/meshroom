import bpy
import bmesh
import os
import mathutils
import math
import sys   # to get command line args
import argparse  # to parse options for us and print a nice help message
from math import radians

def main():
    argv = sys.argv

    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1:]  # get all args after "--"

    # When --help or no args are given, print this help
    usage_text = (
        "Run blender in background mode with this script:"
        "  blender --background --python " + __file__ + " -- [options]"
    )

    parser = argparse.ArgumentParser(description=usage_text)

    parser.add_argument(
        "--sfMData", dest="SFM_Data", metavar='FILE', required=True,
        help="These info carry the cloud point we need.",
    )

    parser.add_argument(
        "--sfMCameraPath", dest="SFM_cam_path", metavar='FILE', required=True,
        help="This text will be used to render an image",
    )
    
    parser.add_argument(
        "--undistortedImages", dest="undisto_images", metavar='FILE', required=True,
        help="Save the generated file to the specified path",
    )

    parser.add_argument(
        "--outputPath", dest="output_path", metavar='FILE', required=True,
        help="Render an image to the specified path",
    )

    args = parser.parse_args(argv)

    if not argv:
        parser.print_help()
        return

    if not args.SFM_cam_path:
        print("Error: --SFM_cam_path argument not given, aborting.")
        parser.print_help()
        return

    if not args.undisto_images:
        print("Error: --undisto_images argument not given, aborting.")
        parser.print_help()
        return

    if not args.output_path:
        print("Error: --output_path argument not given, aborting.")
        parser.print_help()
        return

    print(args.SFM_cam_path)


    #Clear Current Scene
    try:
        print(bpy.data.objects[0])
        print(bpy.data.objects[1])
        print(bpy.data.objects[2])
        for objects in bpy.data.objects:
            bpy.data.objects.remove(objects)
        print(bpy.data.objects)
    except:
        print("Error: While clearing current scene")


    #import abc (Animated Camera)

    try:
        bpy.ops.wm.alembic_import(filepath=args.SFM_cam_path)
        animated_cams = bpy.context.selected_editable_objects[:] #Contains ['animxform_RJBframe_SONY_ILCE-7M3', 'mvgCameras', 'mvgCamerasUndefined', 'mvgPointCloud', 'mvgCloud', 'mvgRoot']
        animated_cam_obj = animated_cams[1] ## scene.object
        animated_cam_RJB = animated_cams[0]
        for obj in animated_cams:
            if obj.data and obj.data.type == 'PERSP':	
                bpy.context.scene.collection.objects.link(obj)
                bpy.context.scene.camera = obj

    except:
        print("Error: while importing the alembic file (Animated Camera).")



    #import abc (Cloud Point)

    try:
        bpy.ops.wm.alembic_import(filepath=args.SFM_Data)
        all_abc_info = bpy.context.selected_editable_objects[:] #Contains ['mvgCameras', 'mvgCamerasUndefined', 'mvgPointCloud', 'mvgCloud', 'mvgRoot']
        pointCloud = all_abc_info[len(all_abc_info) - 3]
        for obj in all_abc_info:
            if obj.name == 'mvgPointCloud.001':
                bpy.context.scene.collection.objects.link(obj)

    except:
        print("Error: while importing the alembic file (sfm Data).")



    # import Undistorted Images

    undis_imgs = []
    try:
        files = os.listdir(args.undisto_images)
        for f in files :
            if f.endswith(".exr") :                
                undis_imgs.append(bpy.ops.image.open(filepath=args.undisto_images + '/' + f))
    except:
        print("Error: while importing the undistorted images.")


    cube = bpy.data.meshes['Cube']
    objects = bpy.data.objects.new(name="Cube", object_data=cube)
    bpy.context.scene.collection.objects.link(objects)


    ## Starts the rendering and launchs it with a blender animator player

    try:
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG' # Changes to video
        bpy.context.scene.render.filepath = args.output_path + '/render.mkv'
        bpy.ops.render.render(animation=True)
        bpy.ops.render.play_rendered_anim()
    except:
        print("Error: while rendering the scene.")
    


if __name__ == "__main__":
    main()