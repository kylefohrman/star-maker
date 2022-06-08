bl_info = \
    {
        "name" : "Star Plane Maker",
        "author" : "J Random Hacker <jrhacker@example.com>",
        "version" : (1, 0, 0),
        "blender" : (2, 5, 7),
        "location" : "View 3D > Edit Mode > Tool Shelf",
        "description" :
            "Generate a star planar mesh",
        "warning" : "",
        "wiki_url" : "https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Advanced_Tutorials/Python_Scripting/Separately_Installable_Addon",
        "tracker_url" : "",
        "category" : "Add Mesh",
    }
#wikibooks link is where I learned many of the scripting techniques below.
#any original code written by Kyle Fohrman while at the University of Florida

import math
import bpy
import mathutils

class MakeStar(bpy.types.Operator) :
    bl_idname = "mesh.make_star"
    bl_label = "Star"
    bl_options = {"REGISTER","UNDO"}
    
    star_outer_radius = bpy.props.FloatProperty \
      (
        name = "Outer Radius",
        description = "Distance from center of outer points",
        default = 1.00
      )
    star_inner_radius = bpy.props.FloatProperty \
      (
        name = "Inner Radius",
        description = "Distance from center of inner points",
        default = 0.50
      )
    star_scale_radius = bpy.props.FloatProperty \
      (
        name = "Scale",
        description = "Scale the star's size",
        default = 1.00
      )
    star_point_count = bpy.props.IntProperty \
      (
        name = "Points",
        description = "Number of outer points on the star",
        default = 5,
        min = 2
      )
    #end scene
    
    def draw(self, context):
        TheCol = self.layout.column(align=True)
        TheCol.prop(self, "star_outer_radius")
        TheCol.prop(self, "star_inner_radius")
        TheCol.prop(self, "star_scale_radius")
        TheCol.prop(self, "star_point_count")
    #end draw
    
    def action_common(self, context) :
        outer_rad = self.star_outer_radius
        inner_rad = self.star_inner_radius
        star_scale = self.star_scale_radius
        point_count = self.star_point_count
        xcoord = bpy.context.scene.cursor_location[0]
        ycoord = bpy.context.scene.cursor_location[1]
        zcoord = bpy.context.scene.cursor_location[2]
        pi = math.pi
        angle = 0
        Vertices = \
        [
        ]
        Faces = \
        [
        ]
        for i in range(0,2*point_count):
            if i%2 == 0:
                Vertices.append(mathutils.Vector((star_scale*outer_rad*math.sin(angle)+xcoord,star_scale*outer_rad*math.cos(angle)+ycoord,zcoord)))
            else:
                Vertices.append(mathutils.Vector((star_scale*inner_rad*math.sin(angle)+xcoord,star_scale*inner_rad*math.cos(angle)+ycoord,zcoord)))
            angle += (pi/point_count)
        Vertices.append(mathutils.Vector((xcoord,ycoord,zcoord)))
        for i in range(0,point_count):
            if(i == 0):
                Faces.append([1,0,2*point_count-1])
                Faces.append([2*point_count-1,2*point_count,1])
            else:
                Faces.append([(2*i+1),(2*i),(2*i-1)])
                Faces.append([2*i-1,2*point_count,2*i+1])
        StarMesh = bpy.data.meshes.new("Star")
        StarMesh.from_pydata \
            (
                Vertices,
                [],
                Faces
            )
        StarMesh.update()
        NewObj = bpy.data.objects.new("Star", StarMesh)
        context.scene.objects.link(NewObj)
        bpy.ops.object.select_all(action = "DESELECT")
        NewObj.select = True
        context.scene.objects.active = NewObj
        #end action_common

    def execute(self, context):
        self.action_common(context)
        return {"FINISHED"}
    #end execute
    
    def invoke(self, context, event):
        self.action_common(context)
        return {"FINISHED"}
    #end invoke
    
    #end MakeStar

def add_to_menu(self, context) :
    self.layout.operator("mesh.make_star", icon = "TRIA_UP")
#end add_to_menu

def register() :
    bpy.utils.register_class(MakeStar)
    bpy.types.INFO_MT_mesh_add.append(add_to_menu)
#end register

def unregister() :
    bpy.utils.unregister_class(MakeStar)
    bpy.types.INFO_MT_mesh_add.remove(add_to_menu)
#end unregister

if __name__ == "__main__" :
    register()
#end if
