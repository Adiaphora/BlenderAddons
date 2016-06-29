#Outliner popup --------------
bl_info = {
  "name": "Jump2Object",
  "author": "k",
  "version": (1, 5, 0),
  "blender": (2, 7, 0),
  "location": "View3D Popup -> Jump to",
  "description": "Lists all objects",
  "wiki_url": "http://zorg.xyz/duo/",
  "category": "3D View"
}

import bpy

class VIEW3D_MT_Outliner_menu(bpy.types.Menu):
  """Tooltip"""
  bl_label = "Jump to:"
  # bl_label = "Outliner (Hold shift to make active)"
  # bl_options = {'HIDE_HEADER'}
  def draw(self, context):
    layout = self.layout
    msh = []
    scn = {}
    #props = col.operator("slct.objects", text=format("[%s]%s"%(obj.type,obj.name)))
    #another types
    icons = {
      'ARMATURE':'OUTLINER_OB_ARMATURE',
      'CURVE':'CURVE_BEZCURVE', # .type = 'PLAIN_AXE'
      'CAMERA':'OUTLINER_OB_CAMERA',
      'MESH':'MESH_CUBE',
      'EMPTY':'OUTLINER_OB_EMPTY',
      'LAMP':'OUTLINER_DATA_LAMP',
      'META':'META_BALL',
      'SURFACE':'SURFACE_NSURFACE',
      'FONT': 'OUTLINER_OB_FONT'
      #{'FIELD':'FORCE_WIND'} #'EMPTY' i.field.type != 'NONE'
    }
    #todo count every type, split if needed
    for i in bpy.data.objects:
      if (i.type == "MESH"):
        msh.append(i.name)
      else:
        scn[i.name] = icons[i.type]
    spl = layout.split()

    col = spl.column()
    col.operator_context = 'INVOKE_DEFAULT'
    col.label('Meshes', icon="MESH_ICOSPHERE")
    for m in msh:
      props = col.operator("slct.objects", text=m)
      props.val = m

    col = spl.column()
    col.operator_context = 'INVOKE_DEFAULT'
    col.label('Other') #, icon='SCENE')
    for s in scn:
      props = col.operator("slct.objects", text=s, icon=scn[s])
      props.val = s

    col = spl.column()
    col.label('Global') #, icon='WORLD')
    props = col.operator("view3d.view_all", text="View All")
    props.center = True #centered

class slctObjects(bpy.types.Operator):
  bl_idname = "slct.objects"
  bl_label = "Select operator"
  bl_options = {'REGISTER', 'UNDO'}
 
  val = bpy.props.StringProperty()
  nojump = False #Hold shift to prevent jumping
  isolate = False #Hold ctrl to get to the localview

  def execute(self, context):
    scn = context.scene
    ob = scn.objects[self.val]
    scn.objects.active = ob
    if self.isolate:
      bpy.ops.view3d.localview()
      return {'FINISHED'}
    if not self.nojump:
      self.deselect_all_objects(scn)
      scn.objects.active = ob
      ob.select = True;
      scn.layers = ob.layers
      bpy.ops.view3d.view_selected()
    #bpy.ops.view3d.view_selected(use_all_regions=False)
    return {'FINISHED'}

  def invoke(self, context, event):
    if event.ctrl:
      self.isolate = True
    if event.shift:
      self.nojump = True

    return self.execute(context)

  def deselect_all_objects(self,scene):
    for obj in scene.objects:
      obj.select = False

def register():
  bpy.utils.register_module(__name__)

  wm = bpy.context.window_manager
  kc = wm.keyconfigs.addon
  if kc:
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.call_menu', 'BACK_SLASH', 'PRESS', shift=True)
    kmi.properties.name = "VIEW3D_MT_Outliner_menu"


def unregister():
  bpy.utils.unregister_module(__name__)

  wm = bpy.context.window_manager
  kc = wm.keyconfigs.addon
  if kc:
    km = kc.keymaps['3D View']
    for kmi in km.keymap_items:
      if kmi.idname == 'wm.call_menu':
        if kmi.properties.name == "VIEW3D_MT_Outliner_menu":
          km.keymap_items.remove(kmi)
          break

if __name__ == "__main__":
  register()

