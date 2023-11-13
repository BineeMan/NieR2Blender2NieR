import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
import os

from .motImporter import *

class ImportNierMot(bpy.types.Operator, ImportHelper):
    """Import a Nier Animation mot file"""
    bl_idname = "import_scene.mot"
    bl_label = "Import Nier Animation Data"
    bl_options = {'UNDO'}

    bulkImport: bpy.props.BoolProperty(name="Bulk Import", description="Import all mot files in the folder", default=False)
    bulkFbxConvert: bpy.props.BoolProperty(name="Bulk Fbx Conversion", description="Convert all the .mot files to fbx in the directory", default=False)
    bFixRotation: bpy.props.BoolProperty(name="Fix Rotation", description="[Bulk Fbx] Tick true if you want to apply rotation wrapper in exported fbx files", default=False)
    filename_ext = ".mot"
    filter_glob: bpy.props.StringProperty(default="*.mot", options={'HIDDEN'})

    def execute(self, context):
        from .motImporter import importMot

        if not self.bulkImport and not self.bulkFbxConvert:
            importMot(self.filepath, True, not self.bulkImport)
        elif self.bulkImport and not self.bulkFbxConvert:
            path = self.filepath if os.path.isdir(self.filepath) else os.path.dirname(self.filepath)
            allMotFiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(".mot")]
            for i, file in enumerate(allMotFiles):
                print(f"Importing {file} ({i+1}/{len(allMotFiles)})")
                importMot(os.path.join(path, file), True)
        elif self.bulkFbxConvert:
            head = os.path.split(self.filepath)[0]
            tail = os.path.split(self.filepath)[1]
            tailless_tail = tail[:-4]
            extract_dir = os.path.join(head, 'nier2blender_FbxExtracted')
            if not os.path.exists(extract_dir):
                os.mkdir(extract_dir)

            path = self.filepath if os.path.isdir(self.filepath) else os.path.dirname(self.filepath)
            allMotFiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(".mot")]
            for i, file in enumerate(allMotFiles):
                print(f"Exporting Fbx {file} ({i+1}/{len(allMotFiles)})")
                convertMotToFbx(os.path.join(path, file), extract_dir, self.bFixRotation, not self.bulkImport)

        if self.bulkImport:
            print(f"Imported {len(allMotFiles)} mot files from {path}")
            self.report({'INFO'}, f"Imported {len(allMotFiles)} mot files")
        else:
            self.report({'INFO'}, "Imported mot file")

        return {'FINISHED'}
