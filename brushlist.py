#Brushlist popup menu --------------
bl_info = {
  "name": "BrushList popup",
  "author": "K",
  "version": (1, 0, 0),
  "blender": (2, 5, 0),
  "location": "Sculpt Mode: View popup binded to Shift + \" ",
  "description": "Lists all sculpt brushes",
  "wiki_url": "http://zorg.xyz/duo/",
  "category": "3D View"
}

import bpy

class VIEW3D_MT_Brushlist_menu(bpy.types.Menu):
  """Tooltip"""
  bl_label = "Sculpt Brushes"
  hk = {}
  def __init__(self):
    km = bpy.context.window_manager.keyconfigs['Blender User'].keymaps['Sculpt']
    for kmi in km.keymap_items:
    pre = 'S+' if kmi.shift else ''
    if kmi.idname == 'paint.brush_select':
      if kmi.properties.paint_mode == "SCULPT":
      self.hk[kmi.properties.sculpt_tool] = pre + kmi.type

  def draw(self, context):
    layout = self.layout
    spl = layout.split()
    if context.mode == 'SCULPT':
      c = 0
      for brush in bpy.data.brushes:
        if brush.sculpt_tool != 'DRAW':
          if not c % 7: col = spl.column()
          c += 1
          bicon = 'BRUSH_'+brush.sculpt_tool
          if brush.name.upper() in self.hk:
            # lbl = '{0:.<22}{1:.>3}'.format(brush.name, self.hk[brush.name.upper()])
            lbl = '{0}  [{1}]'.format(brush.name, self.hk[brush.name.upper()])
          else:
            lbl = brush.name
          props = col.operator("wm.context_set_id", text = lbl, icon= bicon)
          props.data_path = "tool_settings.sculpt.brush"
          props.value = brush.name

def register():
  bpy.utils.register_module(__name__)

  wm = bpy.context.window_manager
  kc = wm.keyconfigs.addon
  if kc:
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.call_menu', 'QUOTE', 'PRESS', shift=True)
    kmi.properties.name = "VIEW3D_MT_Brushlist_menu"


def unregister():
  bpy.utils.unregister_module(__name__)

  wm = bpy.context.window_manager
  kc = wm.keyconfigs.addon
  if kc:
    km = kc.keymaps['3D View']
    for kmi in km.keymap_items:
      if kmi.idname == 'wm.call_menu':
        if kmi.properties.name == "VIEW3D_MT_Brushlist_menu":
          km.keymap_items.remove(kmi)
          break

if __name__ == "__main__":
  register()


