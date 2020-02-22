import bpy, bmesh, math
from blender2nier.util import *
from blender2nier.generate_data import *
from blender2nier.wmb.wmb_header import *
from blender2nier.wmb.wmb_bones import *
from blender2nier.wmb.wmb_boneIndexTranslateTable import *
from blender2nier.wmb.wmb_vertexGroups import *
from blender2nier.wmb.wmb_batches import *
from blender2nier.wmb.wmb_lods import *
from blender2nier.wmb.wmb_meshMaterials import *
from blender2nier.wmb.wmb_boneMap import *
from blender2nier.wmb.wmb_meshes import *
from blender2nier.wmb.wmb_materials import *
from blender2nier.wmb.wmb_boneSet import *
from blender2nier.wmb.wmb_colTreeNodes import *
from blender2nier.wmb.wmb_unknownWorldData import *

normals_flipped = False

def flip_all_normals():
    normals_flipped = True
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.data.flip_normals()
    print('Flipped normals of all meshes.')

def purge_unused_materials():
    for material in bpy.data.materials:
        if not material.users:
            print('Purging unused material:', material)
            bpy.data.materials.remove(material)

def prepare_blend():
    print('Preparing .blend File:')
    bpy.ops.object.mode_set(mode='OBJECT')
    print('Triangulating meshes:')
    for obj in bpy.data.objects:
        if obj.type == 'MESH':

            # Triangulate meshes
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_add(type='TRIANGULATE')
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Triangulate")

        if obj.type not in ['MESH', 'ARMATURE']:
            print('[-] Removed ', obj)
            bpy.data.objects.remove(obj)

def restore_blend(normals_flipped):
    print('Restoring .blend File:')
    if normals_flipped:
        print(' - Flipping back normals.')
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.data.flip_normals()
    print('EXPORT COMPLETE. :D')
    return {'FINISHED'}

def main(filepath):
    prepare_blend()
    
    wmb_file = create_wmb(filepath)

    generated_data = c_generate_data()

    print('-=# All Data Generated. Writing WMB... #=-')

    create_wmb_header(wmb_file, generated_data)

    print('Writing bones.')
    if generated_data.bones is not None:
        create_wmb_bones(wmb_file, generated_data)

    print('Writing boneIndexTranslateTable.')
    if hasattr(generated_data, 'boneIndexTranslateTable'):
        create_wmb_boneIndexTranslateTable(wmb_file, generated_data)

    print('Writing vertexGroups.')
    create_wmb_vertexGroups(wmb_file, generated_data)

    print('Writing batches.')
    create_wmb_batches(wmb_file, generated_data)
    
    print('Writing LODs.')
    create_wmb_lods(wmb_file, generated_data)

    print('Writing meshMaterials.')
    create_wmb_meshMaterials(wmb_file, generated_data)

    if generated_data.colTreeNodes is not None:
        print('Writing colTreeNodes.')
        create_wmb_colTreeNodes(wmb_file, generated_data)

    print('Writing boneSets.')
    if hasattr(generated_data, 'boneSet'):
        create_wmb_boneSet(wmb_file, generated_data)

    if generated_data.boneMap is not None:
        print('Writing boneMap.')
        create_wmb_boneMap(wmb_file, generated_data)

    print('Writing meshes.')
    create_wmb_meshes(wmb_file, generated_data)

    print('Writing materials.')
    create_wmb_materials(wmb_file, generated_data)

    if generated_data.unknownWorldData is not None:
        print('Writing unknownWorldData.')
        create_wmb_unknownWorldData(wmb_file, generated_data)

    print('Finished writing. Closing file..')
    close_wmb(wmb_file)
    
    return {'FINISHED'}