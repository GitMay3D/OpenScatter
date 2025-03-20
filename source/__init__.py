# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "OpenScatter",
    "author" : "May3D", 
    "description" : "OpenScatter is a free and open-source Blender addon for advanced scattering",
    "blender" : (4, 2, 0),
    "version" : (1, 0, 5),
    "location" : "",
    "warning" : "",
    "doc_url": "https://github.com/GitMay3D/OpenScatter", 
    "tracker_url": "https://github.com/GitMay3D/OpenScatter/issues", 
    "category" : "3D View" 
}


import bpy
import bpy.utils.previews
import os
import random
from bpy.app.handlers import persistent
import requests
import re




def string_to_int(value):
    if value.isdigit():
        return int(value)
    return 0


def string_to_icon(value):
    if value in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys():
        return bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items[value].value
    return string_to_int(value)


addon_keymaps = {}
_icons = None
osgn_quick_scatter = {'sna_pattern_list': [], }


def display_collection_id(uid, vars):
    id = f"coll_{uid}"
    for var in vars.keys():
        if var.startswith("i_"):
            id += f"_{var}_{vars[var]}"
    return id


class SNA_UL_display_collection_list_29FCA(bpy.types.UIList):

    def draw_item(self, context, layout, data, item_29FCA, icon, active_data, active_propname, index_29FCA):
        row = layout
        row_C9477 = layout.row(heading='', align=False)
        row_C9477.alert = False
        row_C9477.enabled = True
        row_C9477.active = True
        row_C9477.use_property_split = False
        row_C9477.use_property_decorate = False
        row_C9477.scale_x = 0.20000000298023224
        row_C9477.scale_y = 1.0
        row_C9477.alignment = 'Left'.upper()
        row_C9477.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_C9477.prop(item_29FCA, 'colorlabel', text='', icon_value=0, emboss=True)
        row_46A09 = layout.row(heading='', align=False)
        row_46A09.alert = False
        row_46A09.enabled = True
        row_46A09.active = True
        row_46A09.use_property_split = False
        row_46A09.use_property_decorate = False
        row_46A09.scale_x = 1.0
        row_46A09.scale_y = 1.0
        row_46A09.alignment = 'Expand'.upper()
        row_46A09.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_46A09.prop(item_29FCA, 'label', text='', icon_value=0, emboss=False)
        row_F750B = row_46A09.row(heading='', align=True)
        row_F750B.alert = False
        row_F750B.enabled = True
        row_F750B.active = True
        row_F750B.use_property_split = False
        row_F750B.use_property_decorate = False
        row_F750B.scale_x = 1.0
        row_F750B.scale_y = 1.0
        row_F750B.alignment = 'Expand'.upper()
        row_F750B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_F750B.prop(bpy.data.objects[item_29FCA.name], 'hide_viewport', text='', icon_value=0, emboss=False)
        row_F750B.prop(bpy.data.objects[item_29FCA.name], 'hide_render', text='', icon_value=0, emboss=False)

    def filter_items(self, context, data, propname):
        flt_flags = []
        for item in getattr(data, propname):
            if not self.filter_name or self.filter_name.lower() in item.name.lower():
                if sna_filter_systems_0C7CB(item):
                    flt_flags.append(self.bitflag_filter_item)
                else:
                    flt_flags.append(0)
            else:
                flt_flags.append(0)
        return flt_flags, []


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


def sna_update_sna_emitter_object_7F6B0(self, context):
    sna_updated_prop = self.sna_emitter_object
    for i_0838F in range(len(bpy.context.scene.sna_scattersystemcollection)-1,-1,-1):
        if (bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[i_0838F].name].modifiers['GN_SCS_MOD']['Socket_178'] == bpy.context.scene.sna_emitter_object):
            bpy.context.scene.sna_active_index = i_0838F
            if bpy.context and bpy.context.screen:
                for a in bpy.context.screen.areas:
                    a.tag_redraw()


def sna_update_label_9ED9A(self, context):
    sna_updated_prop = self.label
    bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].name = sna_updated_prop
    bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name = sna_updated_prop
    bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name.update_tag(refresh={'DATA'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()


def sna_update_sna_instance_type_01FB7(self, context):
    sna_updated_prop = self.sna_instance_type
    bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_30'] = (sna_updated_prop == 'Multiple Instances')
    bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].update_tag(refresh={'DATA'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()


def sna_update_sna_proximity_type_69A01(self, context):
    sna_updated_prop = self.sna_proximity_type
    if (sna_updated_prop == 'Single Object'):
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_46'] = False
        bpy.context.active_object.update_tag(refresh={'DATA'}, )
    else:
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_46'] = True
        bpy.context.active_object.update_tag(refresh={'DATA'}, )


def sna_update_sna_curve_proximity_type_54F1E(self, context):
    sna_updated_prop = self.sna_curve_proximity_type
    if (sna_updated_prop == 'Single Curve'):
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_54'] = False
        bpy.context.active_object.update_tag(refresh={'DATA'}, )
    else:
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_54'] = True
        bpy.context.active_object.update_tag(refresh={'DATA'}, )


_item_map = dict()


def make_enum_item(_id, name, descr, preview_id, uid):
    lookup = str(_id)+"\0"+str(name)+"\0"+str(descr)+"\0"+str(preview_id)+"\0"+str(uid)
    if not lookup in _item_map:
        _item_map[lookup] = (_id, name, descr, preview_id, uid)
    return _item_map[lookup]


def random_integer(min, max, seed):
    random.seed(seed)
    return random.randint(int(min), int(max))


def sna_update_sna_surface_type_C9A72(self, context):
    sna_updated_prop = self.sna_surface_type
    if (sna_updated_prop == 'Emitter Object'):
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_179'] = False
        bpy.context.active_object.update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
    else:
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_179'] = True
        bpy.context.active_object.update_tag(refresh={'DATA'}, )
        if (sna_updated_prop == 'Multiple Surfaces'):
            bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_109'] = True
            bpy.context.active_object.update_tag(refresh={'DATA'}, )
            if bpy.context and bpy.context.screen:
                for a in bpy.context.screen.areas:
                    a.tag_redraw()
        else:
            bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_109'] = False
            bpy.context.active_object.update_tag(refresh={'DATA'}, )
            if bpy.context and bpy.context.screen:
                for a in bpy.context.screen.areas:
                    a.tag_redraw()


def sna_update_sna_image_mask_252C4(self, context):
    sna_updated_prop = self.sna_image_mask
    bpy.ops.image.open('INVOKE_DEFAULT', filepath=sna_updated_prop)
    bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_181'] = bpy.data.images[os.path.basename(sna_updated_prop)]
    bpy.context.active_object.update_tag(refresh={'DATA'}, )


class SNA_PT_OPENSCATTER_82501(bpy.types.Panel):
    bl_label = 'OpenScatter'
    bl_idname = 'SNA_PT_OPENSCATTER_82501'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'OpenScatter'
    bl_order = 2
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout_function = layout
        sna_func_emitter_0797E(layout_function, )
        if (bpy.context.scene.sna_emitter_object == None):
            pass
        else:
            box_F029B = layout.box()
            box_F029B.alert = False
            box_F029B.enabled = True
            box_F029B.active = True
            box_F029B.use_property_split = False
            box_F029B.use_property_decorate = False
            box_F029B.alignment = 'Expand'.upper()
            box_F029B.scale_x = 1.0
            box_F029B.scale_y = 1.0
            if not True: box_F029B.operator_context = "EXEC_DEFAULT"
            row_F853A = box_F029B.row(heading='', align=False)
            row_F853A.alert = False
            row_F853A.enabled = True
            row_F853A.active = True
            row_F853A.use_property_split = False
            row_F853A.use_property_decorate = False
            row_F853A.scale_x = 1.0
            row_F853A.scale_y = 1.0
            row_F853A.alignment = 'Left'.upper()
            row_F853A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_F853A.prop(bpy.context.scene, 'sna_display_system_list', text='System List', icon_value=string_to_icon('SYSTEM'), emboss=False)
            if bpy.context.scene.sna_display_system_list:
                row_C23C3 = box_F029B.row(heading='', align=True)
                row_C23C3.alert = False
                row_C23C3.enabled = True
                row_C23C3.active = True
                row_C23C3.use_property_split = False
                row_C23C3.use_property_decorate = False
                row_C23C3.scale_x = 1.0
                row_C23C3.scale_y = 1.0
                row_C23C3.alignment = 'Expand'.upper()
                row_C23C3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                coll_id = display_collection_id('29FCA', locals())
                row_C23C3.template_list('SNA_UL_display_collection_list_29FCA', coll_id, bpy.context.scene, 'sna_scattersystemcollection', bpy.context.scene, 'sna_active_index', rows=0)
                col_8104B = row_C23C3.column(heading='', align=True)
                col_8104B.alert = False
                col_8104B.enabled = True
                col_8104B.active = True
                col_8104B.use_property_split = False
                col_8104B.use_property_decorate = False
                col_8104B.scale_x = 1.0
                col_8104B.scale_y = 1.0
                col_8104B.alignment = 'Expand'.upper()
                col_8104B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                op = col_8104B.operator('sna.add_scatter_system_fbb77', text='', icon_value=string_to_icon('ADD'), emboss=True, depress=False)
                op = col_8104B.operator('sna.delete_scatter_layer_537d5', text='', icon_value=string_to_icon('REMOVE'), emboss=True, depress=False)
                col_8104B.separator(factor=1.0)
                op = col_8104B.operator('sna.move_up_aeedb', text='', icon_value=string_to_icon('TRIA_UP'), emboss=True, depress=False)
                op = col_8104B.operator('sna.move_down_fc101', text='', icon_value=string_to_icon('TRIA_DOWN'), emboss=True, depress=False)
                col_8104B.separator(factor=1.0)
                col_8104B.menu('SNA_MT_09C83', text='', icon_value=string_to_icon('DOWNARROW_HLT'))
        if (bpy.context.scene.sna_emitter_object == None):
            pass
        else:
            if (len(bpy.context.scene.sna_scattersystemcollection) > 0):
                layout_function = layout
                sna_func_surfacesample_80F42(layout_function, )
                layout_function = layout
                sna_func_instances_B4607(layout_function, )
                layout_function = layout
                sna_func_scattering_80211(layout_function, )
                layout_function = layout
                sna_func_scale_A798D(layout_function, )
                layout_function = layout
                sna_func_rotation_7C8F2(layout_function, )
                layout_function = layout
                sna_func_culling_CEC85(layout_function, )
                layout_function = layout
                sna_func_abiotic_1232B(layout_function, )
                layout_function = layout
                sna_func_proximity_773E1(layout_function, )
                layout_function = layout
                sna_func_ecosystem_883DD(layout_function, )
                layout_function = layout
                sna_func_texturemasks_641D8(layout_function, )
                layout_function = layout
                sna_func_dynamics_8A9D6(layout_function, )
                layout_function = layout
                sna_func_optimization_DB30B(layout_function, )


class SNA_OT_Add_Scatter_System_Fbb77(bpy.types.Operator):
    bl_idname = "sna.add_scatter_system_fbb77"
    bl_label = "Add Scatter System"
    bl_description = "Add a new scatter system to the scene"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if 'OBJECT'==bpy.context.mode:
            if (property_exists("bpy.data.node_groups", globals(), locals()) and 'GN_ScatterSystem' in bpy.data.node_groups):
                pass
            else:
                before_data = list(bpy.data.node_groups)
                bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'OpenScatterGN_01.blend') + r'\NodeTree', filename='GN_ScatterSystem', link=False)
                new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
                appended_57DDD = None if not new_data else new_data[0]
            bpy.ops.mesh.primitive_cube_add('INVOKE_DEFAULT', size=0.10000000149011612)
            bpy.context.active_object.name = 'ScatterSystem'
            sna_movetocollectionfunc_C2D7D('Scatter Systems')
            modifier_2CE6E = bpy.context.view_layer.objects.active.modifiers.new(name='GN_SCS_MOD', type='NODES', )
            bpy.context.active_object.modifiers.active.node_group = bpy.data.node_groups['GN_ScatterSystem']
            bpy.context.view_layer.objects.active.hide_select = True
            bpy.data.collections['Scatter Systems'].color_tag = 'COLOR_01'
            bpy.context.active_object.modifiers.active.show_expanded = False
            item_385C8 = bpy.context.scene.sna_scattersystemcollection.add()
            bpy.context.scene.sna_active_index = int(len(bpy.context.scene.sna_scattersystemcollection) - 1.0)
            item_385C8.name = bpy.context.active_object.name
            item_385C8.label = bpy.context.active_object.name
            item_385C8.colorlabel = (0.044308263808488846, 0.14697450399398804, 0.007629591040313244)
            item_385C8.scene = bpy.context.scene
            bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_178'] = bpy.context.scene.sna_emitter_object
            bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_8'] = bpy.context.preferences.addons[__package__].preferences.sna_default_density
            if bpy.context.preferences.addons[__package__].preferences.sna_bounding_box:
                bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_122'] = True
                bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_123'] = 0
            bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_21'] = bpy.context.preferences.addons[__package__].preferences.sna_align_to_surface
            bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_135'] = True
            bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_11'] = bpy.context.preferences.addons[__package__].preferences.sna_default_scale
            bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_13'] = bpy.context.preferences.addons[__package__].preferences.sna_random_scale
            bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_25'] = bpy.context.preferences.addons[__package__].preferences.sna_random_rotation
            sna_appendproxyobjectsfunc_389FE()
        else:
            bpy.ops.wm.call_panel(name="SNA_PT_cant_create_scatter_systems_in_this_mode_C1531", keep_open=False)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_movetocollectionfunc_C2D7D(CollectionName):
    collection_name = CollectionName

    def is_collection_in_scene(collection, scene):
        """Recursively check if the collection is in the scene's hierarchy."""

        def recurse(parent):
            if parent == collection:
                return True
            for child in parent.children:
                if recurse(child):
                    return True
            return False
        return recurse(scene.collection)
    # Set your desired collection name here
    collection_name = collection_name
    # Get the active object
    obj = bpy.context.active_object
    if obj is None:
        print("Error: No active object selected.")
    else:
        # Retrieve or create the collection
        collection = bpy.data.collections.get(collection_name)
        if collection is None:
            # Create new collection and link to active scene
            collection = bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(collection)
            print(f"Created new collection '{collection_name}' in active scene.")
        else:
            # Check if collection exists in active scene
            if not is_collection_in_scene(collection, bpy.context.scene):
                # Link existing collection to active scene
                bpy.context.scene.collection.children.link(collection)
                print(f"Linked existing collection '{collection_name}' to active scene.")
            else:
                print(f"Collection '{collection_name}' already in active scene.")
        # Unlink the object from all current collections
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        # Link the object to the target collection
        collection.objects.link(obj)
        print(f"Moved '{obj.name}' to collection '{collection_name}'.")


class SNA_OT_Delete_Scatter_Layer_537D5(bpy.types.Operator):
    bl_idname = "sna.delete_scatter_layer_537d5"
    bl_label = "Delete Scatter Layer"
    bl_description = "Deletes the active scatter layer"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.data.objects.remove(object=bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name], )
        if (int(len(bpy.context.scene.sna_scattersystemcollection) - 1.0) == bpy.context.scene.sna_active_index):
            if len(bpy.context.scene.sna_scattersystemcollection) > bpy.context.scene.sna_active_index:
                bpy.context.scene.sna_scattersystemcollection.remove(bpy.context.scene.sna_active_index)
            bpy.context.scene.sna_active_index = int(len(bpy.context.scene.sna_scattersystemcollection) - 1.0)
        else:
            if len(bpy.context.scene.sna_scattersystemcollection) > bpy.context.scene.sna_active_index:
                bpy.context.scene.sna_scattersystemcollection.remove(bpy.context.scene.sna_active_index)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SNA_OT_Move_Up_Aeedb(bpy.types.Operator):
    bl_idname = "sna.move_up_aeedb"
    bl_label = "Move Up"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_active_index == 0):
            pass
        else:
            bpy.context.scene.sna_scattersystemcollection.move(bpy.context.scene.sna_active_index, int(bpy.context.scene.sna_active_index - 1.0))
            item_5CFEA = bpy.context.scene.sna_scattersystemcollection[int(bpy.context.scene.sna_active_index - 1.0)]
            bpy.context.scene.sna_active_index = int(bpy.context.scene.sna_active_index - 1.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Move_Down_Fc101(bpy.types.Operator):
    bl_idname = "sna.move_down_fc101"
    bl_label = "Move Down"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_active_index == float(len(bpy.context.scene.sna_scattersystemcollection) - 1.0)):
            pass
        else:
            bpy.context.scene.sna_scattersystemcollection.move(bpy.context.scene.sna_active_index, int(bpy.context.scene.sna_active_index + 1.0))
            item_90A39 = bpy.context.scene.sna_scattersystemcollection[int(bpy.context.scene.sna_active_index + 1.0)]
            bpy.context.scene.sna_active_index = int(bpy.context.scene.sna_active_index + 1.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_filter_systems_0C7CB(Input):
    return (bpy.data.objects[Input.name].modifiers['GN_SCS_MOD']['Socket_178'] == bpy.context.scene.sna_emitter_object)


class SNA_PT_cant_create_scatter_systems_in_this_mode_C1531(bpy.types.Panel):
    bl_label = ''
    bl_idname = 'SNA_PT_cant_create_scatter_systems_in_this_mode_C1531'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = ''
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col_44D7A = layout.column(heading='', align=False)
        col_44D7A.alert = True
        col_44D7A.enabled = True
        col_44D7A.active = True
        col_44D7A.use_property_split = False
        col_44D7A.use_property_decorate = False
        col_44D7A.scale_x = 1.0
        col_44D7A.scale_y = 1.0
        col_44D7A.alignment = 'Expand'.upper()
        col_44D7A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_44D7A.label(text='Enter object mode first!', icon_value=string_to_icon('WARNING_LARGE'))


class SNA_MT_09C83(bpy.types.Menu):
    bl_idname = "SNA_MT_09C83"
    bl_label = "Scatter Menu"

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = "INVOKE_DEFAULT"
        op = layout.operator('sna.refresh_view_e4454', text='Refresh List', icon_value=647, emboss=True, depress=False)
        layout.separator(factor=1.0)
        layout.prop(bpy.context.preferences.addons[__package__].preferences, 'sna_auto_scene_switch_detection', text='Auto Refresh', icon_value=0, emboss=True)


def sna_func_abiotic_1232B(layout_function, ):
    box_BD057 = layout_function.box()
    box_BD057.alert = False
    box_BD057.enabled = True
    box_BD057.active = True
    box_BD057.use_property_split = False
    box_BD057.use_property_decorate = False
    box_BD057.alignment = 'Expand'.upper()
    box_BD057.scale_x = 1.0
    box_BD057.scale_y = 1.0
    if not True: box_BD057.operator_context = "EXEC_DEFAULT"
    col_38B80 = box_BD057.column(heading='', align=False)
    col_38B80.alert = False
    col_38B80.enabled = True
    col_38B80.active = True
    col_38B80.use_property_split = False
    col_38B80.use_property_decorate = False
    col_38B80.scale_x = 1.0
    col_38B80.scale_y = 1.0
    col_38B80.alignment = 'Expand'.upper()
    col_38B80.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_BA6C2 = col_38B80.row(heading='', align=False)
    row_BA6C2.alert = False
    row_BA6C2.enabled = True
    row_BA6C2.active = True
    row_BA6C2.use_property_split = False
    row_BA6C2.use_property_decorate = False
    row_BA6C2.scale_x = 1.0
    row_BA6C2.scale_y = 1.0
    row_BA6C2.alignment = 'Left'.upper()
    row_BA6C2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_BA6C2.prop(bpy.context.scene, 'sna_display_abiotic', text='Abiotic', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_abiotic else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_display_abiotic:
        col_121E1 = col_38B80.column(heading='', align=False)
        col_121E1.alert = False
        col_121E1.enabled = True
        col_121E1.active = True
        col_121E1.use_property_split = False
        col_121E1.use_property_decorate = False
        col_121E1.scale_x = 1.0
        col_121E1.scale_y = 1.0
        col_121E1.alignment = 'Expand'.upper()
        col_121E1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_4EAD8 = col_121E1.column(heading='', align=False)
        col_4EAD8.alert = False
        col_4EAD8.enabled = True
        col_4EAD8.active = True
        col_4EAD8.use_property_split = False
        col_4EAD8.use_property_decorate = False
        col_4EAD8.scale_x = 1.0
        col_4EAD8.scale_y = 1.0
        col_4EAD8.alignment = 'Expand'.upper()
        col_4EAD8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_4EAD8.separator(factor=1.0)
        row_A536B = col_4EAD8.row(heading='', align=True)
        row_A536B.alert = False
        row_A536B.enabled = True
        row_A536B.active = True
        row_A536B.use_property_split = False
        row_A536B.use_property_decorate = False
        row_A536B.scale_x = 1.0
        row_A536B.scale_y = 1.0
        row_A536B.alignment = 'Expand'.upper()
        row_A536B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_A536B.prop(bpy.context.scene, 'sna_display_slope_mask', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_slope_mask else string_to_icon('RIGHTARROW')), emboss=False)
        attr_8DDEE = '["' + str('Socket_33' + '"]') 
        row_A536B.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_8DDEE, text='Slope Mask', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_slope_mask:
            row_D7074 = col_4EAD8.row(heading='', align=False)
            row_D7074.alert = False
            row_D7074.enabled = True
            row_D7074.active = True
            row_D7074.use_property_split = False
            row_D7074.use_property_decorate = False
            row_D7074.scale_x = 1.0
            row_D7074.scale_y = 1.0
            row_D7074.alignment = 'Expand'.upper()
            row_D7074.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_D7074.label(text='', icon_value=string_to_icon('BLANK1'))
            col_D1111 = row_D7074.column(heading='', align=False)
            col_D1111.alert = False
            col_D1111.enabled = True
            col_D1111.active = True
            col_D1111.use_property_split = False
            col_D1111.use_property_decorate = False
            col_D1111.scale_x = 1.0
            col_D1111.scale_y = 1.0
            col_D1111.alignment = 'Expand'.upper()
            col_D1111.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_D1111.separator(factor=1.0)
            col_D1111.label(text='Cutoff:', icon_value=string_to_icon('MOD_DECIM'))
            attr_EA9C8 = '["' + str('Socket_171' + '"]') 
            col_D1111.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_EA9C8, text='Slope', icon_value=0, emboss=True)
            col_D1111.separator(factor=1.0)
            col_D1111.label(text='Falloff', icon_value=string_to_icon('SHARPCURVE'))
            attr_93F95 = '["' + str('Socket_173' + '"]') 
            col_D1111.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_93F95, text='Smooth Transition', icon_value=0, emboss=True)
            if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_173']:
                row_AD81B = col_D1111.row(heading='', align=False)
                row_AD81B.alert = False
                row_AD81B.enabled = True
                row_AD81B.active = True
                row_AD81B.use_property_split = False
                row_AD81B.use_property_decorate = False
                row_AD81B.scale_x = 1.0
                row_AD81B.scale_y = 1.0
                row_AD81B.alignment = 'Expand'.upper()
                row_AD81B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_AD81B.label(text='', icon_value=string_to_icon('BLANK1'))
                col_2044A = row_AD81B.column(heading='', align=False)
                col_2044A.alert = False
                col_2044A.enabled = True
                col_2044A.active = True
                col_2044A.use_property_split = False
                col_2044A.use_property_decorate = False
                col_2044A.scale_x = 1.0
                col_2044A.scale_y = 1.0
                col_2044A.alignment = 'Expand'.upper()
                col_2044A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_2044A.separator(factor=0.25)
                attr_F3334 = '["' + str('Socket_35' + '"]') 
                col_2044A.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_F3334, text='Transition', icon_value=0, emboss=True)
            col_D1111.separator(factor=1.0)
            attr_DFCAB = '["' + str('Socket_134' + '"]') 
            col_D1111.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_DFCAB, text='Invert', icon_value=string_to_icon('ARROW_LEFTRIGHT'), emboss=True)
        col_F78A1 = col_121E1.column(heading='', align=False)
        col_F78A1.alert = False
        col_F78A1.enabled = True
        col_F78A1.active = True
        col_F78A1.use_property_split = False
        col_F78A1.use_property_decorate = False
        col_F78A1.scale_x = 1.0
        col_F78A1.scale_y = 1.0
        col_F78A1.alignment = 'Expand'.upper()
        col_F78A1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_F78A1.separator(factor=1.0)
        row_A74F9 = col_F78A1.row(heading='', align=True)
        row_A74F9.alert = False
        row_A74F9.enabled = True
        row_A74F9.active = True
        row_A74F9.use_property_split = False
        row_A74F9.use_property_decorate = False
        row_A74F9.scale_x = 1.0
        row_A74F9.scale_y = 1.0
        row_A74F9.alignment = 'Expand'.upper()
        row_A74F9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_A74F9.prop(bpy.context.scene, 'sna_display_elevation_mask', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_elevation_mask else string_to_icon('RIGHTARROW')), emboss=False)
        attr_6BFA9 = '["' + str('Socket_41' + '"]') 
        row_A74F9.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_6BFA9, text='Elevation Mask', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_elevation_mask:
            row_84C29 = col_F78A1.row(heading='', align=False)
            row_84C29.alert = False
            row_84C29.enabled = True
            row_84C29.active = True
            row_84C29.use_property_split = False
            row_84C29.use_property_decorate = False
            row_84C29.scale_x = 1.0
            row_84C29.scale_y = 1.0
            row_84C29.alignment = 'Expand'.upper()
            row_84C29.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_84C29.label(text='', icon_value=string_to_icon('BLANK1'))
            col_96C4D = row_84C29.column(heading='', align=False)
            col_96C4D.alert = False
            col_96C4D.enabled = True
            col_96C4D.active = True
            col_96C4D.use_property_split = False
            col_96C4D.use_property_decorate = False
            col_96C4D.scale_x = 1.0
            col_96C4D.scale_y = 1.0
            col_96C4D.alignment = 'Expand'.upper()
            col_96C4D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_96C4D.separator(factor=1.0)
            col_96C4D.label(text='Cutoff:', icon_value=string_to_icon('MOD_DECIM'))
            attr_9CE8A = '["' + str('Socket_40' + '"]') 
            col_96C4D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_9CE8A, text='Height', icon_value=0, emboss=True)
            col_96C4D.separator(factor=1.0)
            col_96C4D.label(text='Falloff', icon_value=string_to_icon('SHARPCURVE'))
            attr_256E4 = '["' + str('Socket_38' + '"]') 
            col_96C4D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_256E4, text='Smooth Transition', icon_value=0, emboss=True)
            if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_38']:
                row_128C4 = col_96C4D.row(heading='', align=False)
                row_128C4.alert = False
                row_128C4.enabled = True
                row_128C4.active = True
                row_128C4.use_property_split = False
                row_128C4.use_property_decorate = False
                row_128C4.scale_x = 1.0
                row_128C4.scale_y = 1.0
                row_128C4.alignment = 'Expand'.upper()
                row_128C4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_128C4.label(text='', icon_value=string_to_icon('BLANK1'))
                col_BC249 = row_128C4.column(heading='', align=False)
                col_BC249.alert = False
                col_BC249.enabled = True
                col_BC249.active = True
                col_BC249.use_property_split = False
                col_BC249.use_property_decorate = False
                col_BC249.scale_x = 1.0
                col_BC249.scale_y = 1.0
                col_BC249.alignment = 'Expand'.upper()
                col_BC249.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_BC249.separator(factor=0.25)
                attr_8901E = '["' + str('Socket_39' + '"]') 
                col_BC249.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_8901E, text='Transition', icon_value=0, emboss=True)
            col_96C4D.separator(factor=1.0)
            attr_5B3F1 = '["' + str('Socket_37' + '"]') 
            col_96C4D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_5B3F1, text='Invert', icon_value=string_to_icon('ARROW_LEFTRIGHT'), emboss=True)
            col_96C4D.separator(factor=1.0)
            attr_72E42 = '["' + str('Socket_131' + '"]') 
            col_96C4D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_72E42, text='Randomize', icon_value=0, emboss=True)
            col_B67A7 = col_96C4D.column(heading='', align=False)
            col_B67A7.alert = False
            col_B67A7.enabled = bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_131']
            col_B67A7.active = bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_131']
            col_B67A7.use_property_split = False
            col_B67A7.use_property_decorate = False
            col_B67A7.scale_x = 1.0
            col_B67A7.scale_y = 1.0
            col_B67A7.alignment = 'Expand'.upper()
            col_B67A7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_B67A7.separator(factor=1.0)
            attr_AA275 = '["' + str('Socket_132' + '"]') 
            col_B67A7.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_AA275, text='Amount', icon_value=0, emboss=True)
            attr_BE6DF = '["' + str('Socket_133' + '"]') 
            col_B67A7.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_BE6DF, text='Scale', icon_value=0, emboss=True)
        col_04E22 = col_121E1.column(heading='', align=False)
        col_04E22.alert = False
        col_04E22.enabled = True
        col_04E22.active = True
        col_04E22.use_property_split = False
        col_04E22.use_property_decorate = False
        col_04E22.scale_x = 1.0
        col_04E22.scale_y = 1.0
        col_04E22.alignment = 'Expand'.upper()
        col_04E22.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_04E22.separator(factor=1.0)
        row_168BC = col_04E22.row(heading='', align=True)
        row_168BC.alert = False
        row_168BC.enabled = True
        row_168BC.active = True
        row_168BC.use_property_split = False
        row_168BC.use_property_decorate = False
        row_168BC.scale_x = 1.0
        row_168BC.scale_y = 1.0
        row_168BC.alignment = 'Expand'.upper()
        row_168BC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_168BC.prop(bpy.context.scene, 'sna_display_angle_mask', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_angle_mask else string_to_icon('RIGHTARROW')), emboss=False)
        attr_6AF5F = '["' + str('Socket_112' + '"]') 
        row_168BC.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_6AF5F, text='Angle Mask', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_angle_mask:
            row_A04F9 = col_04E22.row(heading='', align=False)
            row_A04F9.alert = False
            row_A04F9.enabled = True
            row_A04F9.active = True
            row_A04F9.use_property_split = False
            row_A04F9.use_property_decorate = False
            row_A04F9.scale_x = 1.0
            row_A04F9.scale_y = 1.0
            row_A04F9.alignment = 'Expand'.upper()
            row_A04F9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_A04F9.label(text='', icon_value=string_to_icon('BLANK1'))
            col_307E6 = row_A04F9.column(heading='', align=False)
            col_307E6.alert = False
            col_307E6.enabled = True
            col_307E6.active = True
            col_307E6.use_property_split = False
            col_307E6.use_property_decorate = False
            col_307E6.scale_x = 1.0
            col_307E6.scale_y = 1.0
            col_307E6.alignment = 'Expand'.upper()
            col_307E6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_307E6.separator(factor=1.0)
            col_307E6.label(text='Cutoff:', icon_value=string_to_icon('MOD_DECIM'))
            attr_02694 = '["' + str('Socket_113' + '"]') 
            col_307E6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_02694, text='Angle', icon_value=0, emboss=True)
            attr_18913 = '["' + str('Socket_114' + '"]') 
            col_307E6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_18913, text='Offset', icon_value=0, emboss=True)
            col_307E6.separator(factor=1.0)
            col_307E6.label(text='Falloff:', icon_value=string_to_icon('SHARPCURVE'))
            attr_24790 = '["' + str('Socket_174' + '"]') 
            col_307E6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_24790, text='Smooth Transition', icon_value=0, emboss=True)
            if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_174']:
                row_8C857 = col_307E6.row(heading='', align=False)
                row_8C857.alert = False
                row_8C857.enabled = True
                row_8C857.active = True
                row_8C857.use_property_split = False
                row_8C857.use_property_decorate = False
                row_8C857.scale_x = 1.0
                row_8C857.scale_y = 1.0
                row_8C857.alignment = 'Expand'.upper()
                row_8C857.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_8C857.label(text='', icon_value=string_to_icon('BLANK1'))
                col_A50DB = row_8C857.column(heading='', align=False)
                col_A50DB.alert = False
                col_A50DB.enabled = True
                col_A50DB.active = True
                col_A50DB.use_property_split = False
                col_A50DB.use_property_decorate = False
                col_A50DB.scale_x = 1.0
                col_A50DB.scale_y = 1.0
                col_A50DB.alignment = 'Expand'.upper()
                col_A50DB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_A50DB.separator(factor=0.25)
                attr_AF65E = '["' + str('Socket_115' + '"]') 
                col_A50DB.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_AF65E, text='Transition', icon_value=0, emboss=True)


def sna_appendproxyobjectsfunc_389FE():
    if (property_exists("bpy.data.collections", globals(), locals()) and 'OSGN_ProxyObjectsCollection' in bpy.data.collections):
        pass
    else:

        def set_active_collection(collection_name):
            view_layer = bpy.context.view_layer

            def find_layer_collection(layer_coll):
                if layer_coll.collection.name == collection_name:
                    return layer_coll
                for child in layer_coll.children:
                    found = find_layer_collection(child)
                    if found:
                        return found
                return None
            target_layer_coll = find_layer_collection(view_layer.layer_collection)
            if target_layer_coll:
                view_layer.active_layer_collection = target_layer_coll
                print(f"Active collection set to '{collection_name}'.")
            else:
                print(f"Collection '{collection_name}' not found in the current view layer.")
        # Set the active collection to "Scatter Systems"
        set_active_collection("Scatter Systems")
        before_data = list(bpy.data.collections)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'OpenScatterGN_01.blend') + r'\Collection', filename='OSGN_ProxyObjectsCollection', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.collections)))
        appended_EBAA7 = None if not new_data else new_data[0]
        bpy.data.collections['OSGN_ProxyObjectsCollection'].hide_viewport = True
        bpy.data.collections['OSGN_ProxyObjectsCollection'].hide_render = True
        for i_63E3F in range(len(bpy.data.collections['OSGN_ProxyObjectsCollection'].all_objects)):
            bpy.data.collections['OSGN_ProxyObjectsCollection'].all_objects[i_63E3F].hide_viewport = False
            bpy.data.collections['OSGN_ProxyObjectsCollection'].all_objects[i_63E3F].hide_render = False
    bpy.data.node_groups['Instance on Points'].nodes['Cone'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Cone']
    bpy.data.node_groups['Instance on Points'].nodes['Cube'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Cube']
    bpy.data.node_groups['Instance on Points'].nodes['Icosphere'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Icosphere']
    bpy.data.node_groups['Instance on Points'].nodes['Rock'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Rock']
    bpy.data.node_groups['Instance on Points'].nodes['Pebbles'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Pebbles']
    bpy.data.node_groups['Instance on Points'].nodes['Flower'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Flower']
    bpy.data.node_groups['Instance on Points'].nodes['Flower Clump'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Flower Clump']
    bpy.data.node_groups['Instance on Points'].nodes['Grass Clump 01'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Grass Clump 01']
    bpy.data.node_groups['Instance on Points'].nodes['Grass Clump 02'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Grass Clump 02']
    bpy.data.node_groups['Instance on Points'].nodes['Grass Clump 03'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Grass Clump 03']
    bpy.data.node_groups['Instance on Points'].nodes['Bush'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_OSGN_Bush']
    bpy.data.node_groups['Instance on Points'].nodes['Tree 01'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Tree 01']
    bpy.data.node_groups['Instance on Points'].nodes['Tree 02'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Tree 02']
    bpy.data.node_groups['Instance on Points'].nodes['Tree 03'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Tree 03']
    bpy.data.node_groups['Instance on Points'].nodes['Tree 04'].inputs[0].default_value = bpy.data.objects['OSGN_ProxyAsset_Tree 04']


def sna_func_culling_CEC85(layout_function, ):
    box_712C3 = layout_function.box()
    box_712C3.alert = False
    box_712C3.enabled = True
    box_712C3.active = True
    box_712C3.use_property_split = False
    box_712C3.use_property_decorate = False
    box_712C3.alignment = 'Expand'.upper()
    box_712C3.scale_x = 1.0
    box_712C3.scale_y = 1.0
    if not True: box_712C3.operator_context = "EXEC_DEFAULT"
    col_3E65B = box_712C3.column(heading='', align=False)
    col_3E65B.alert = False
    col_3E65B.enabled = True
    col_3E65B.active = True
    col_3E65B.use_property_split = False
    col_3E65B.use_property_decorate = False
    col_3E65B.scale_x = 1.0
    col_3E65B.scale_y = 1.0
    col_3E65B.alignment = 'Expand'.upper()
    col_3E65B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_F7D71 = col_3E65B.row(heading='', align=False)
    row_F7D71.alert = False
    row_F7D71.enabled = True
    row_F7D71.active = True
    row_F7D71.use_property_split = False
    row_F7D71.use_property_decorate = False
    row_F7D71.scale_x = 1.0
    row_F7D71.scale_y = 1.0
    row_F7D71.alignment = 'Left'.upper()
    row_F7D71.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_F7D71.prop(bpy.context.scene, 'sna_display_culling', text='Culling', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_culling else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_display_culling:
        col_707D3 = col_3E65B.column(heading='', align=False)
        col_707D3.alert = False
        col_707D3.enabled = True
        col_707D3.active = True
        col_707D3.use_property_split = False
        col_707D3.use_property_decorate = False
        col_707D3.scale_x = 1.0
        col_707D3.scale_y = 1.0
        col_707D3.alignment = 'Expand'.upper()
        col_707D3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_707D3.separator(factor=1.0)
        row_CA487 = col_707D3.row(heading='', align=True)
        row_CA487.alert = False
        row_CA487.enabled = True
        row_CA487.active = True
        row_CA487.use_property_split = False
        row_CA487.use_property_decorate = False
        row_CA487.scale_x = 1.0
        row_CA487.scale_y = 1.0
        row_CA487.alignment = 'Expand'.upper()
        row_CA487.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_CA487.prop(bpy.context.scene, 'sna_display_vertex_group', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_vertex_group else string_to_icon('RIGHTARROW')), emboss=False)
        attr_66529 = '["' + str('Socket_105' + '"]') 
        row_CA487.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_66529, text='Vertex Group', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_vertex_group:
            row_FCDBE = col_707D3.row(heading='', align=False)
            row_FCDBE.alert = False
            row_FCDBE.enabled = True
            row_FCDBE.active = True
            row_FCDBE.use_property_split = False
            row_FCDBE.use_property_decorate = False
            row_FCDBE.scale_x = 1.0
            row_FCDBE.scale_y = 1.0
            row_FCDBE.alignment = 'Expand'.upper()
            row_FCDBE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_FCDBE.label(text='', icon_value=string_to_icon('BLANK1'))
            col_BDF9A = row_FCDBE.column(heading='', align=False)
            col_BDF9A.alert = False
            col_BDF9A.enabled = True
            col_BDF9A.active = True
            col_BDF9A.use_property_split = False
            col_BDF9A.use_property_decorate = False
            col_BDF9A.scale_x = 1.0
            col_BDF9A.scale_y = 1.0
            col_BDF9A.alignment = 'Expand'.upper()
            col_BDF9A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_BDF9A.separator(factor=1.0)
            col_ED557 = col_BDF9A.column(heading='', align=False)
            col_ED557.alert = False
            col_ED557.enabled = True
            col_ED557.active = True
            col_ED557.use_property_split = False
            col_ED557.use_property_decorate = False
            col_ED557.scale_x = 1.0
            col_ED557.scale_y = 1.0
            col_ED557.alignment = 'Expand'.upper()
            col_ED557.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_5E09E = col_ED557.row(heading='', align=True)
            row_5E09E.alert = False
            row_5E09E.enabled = True
            row_5E09E.active = True
            row_5E09E.use_property_split = False
            row_5E09E.use_property_decorate = False
            row_5E09E.scale_x = 1.0
            row_5E09E.scale_y = 1.0
            row_5E09E.alignment = 'Expand'.upper()
            row_5E09E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_CE20D = row_5E09E.row(heading='', align=True)
            row_CE20D.alert = False
            row_CE20D.enabled = True
            row_CE20D.active = True
            row_CE20D.use_property_split = False
            row_CE20D.use_property_decorate = False
            row_CE20D.scale_x = 1.0
            row_CE20D.scale_y = 1.0
            row_CE20D.alignment = 'Expand'.upper()
            row_CE20D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if (bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].sna_surface_type == 'Emitter Object'):
                row_CE20D.prop_search(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], '["Socket_102"]', bpy.context.scene.sna_emitter_object, 'vertex_groups', text='', icon='GROUP_VERTEX')
            else:
                if (bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].sna_surface_type == 'Single Surface'):
                    row_CE20D.prop_search(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], '["Socket_102"]', bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_108'], 'vertex_groups', text='', icon='GROUP_VERTEX')
                else:
                    row_CE20D.prop_search(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], '["Socket_102"]', bpy.context.view_layer.objects.active, 'vertex_groups', text='', icon='GROUP_VERTEX')
            attr_77955 = '["' + str('Socket_139' + '"]') 
            row_CE20D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_77955, text='', icon_value=string_to_icon('ARROW_LEFTRIGHT'), emboss=True)
            op = row_CE20D.operator('sna.enter_weight_paint_mode_db6f9', text='', icon_value=string_to_icon('WPAINT_HLT'), emboss=True, depress=False)
            col_ED557.separator(factor=1.0)
            attr_1847C = '["' + str('Socket_192' + '"]') 
            col_ED557.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_1847C, text='Smooth Transition', icon_value=0, emboss=True)
            if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_192']:
                row_6D370 = col_ED557.row(heading='', align=False)
                row_6D370.alert = False
                row_6D370.enabled = True
                row_6D370.active = True
                row_6D370.use_property_split = False
                row_6D370.use_property_decorate = False
                row_6D370.scale_x = 1.0
                row_6D370.scale_y = 1.0
                row_6D370.alignment = 'Expand'.upper()
                row_6D370.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_6D370.label(text='', icon_value=string_to_icon('BLANK1'))
                col_445B8 = row_6D370.column(heading='', align=False)
                col_445B8.alert = False
                col_445B8.enabled = True
                col_445B8.active = True
                col_445B8.use_property_split = False
                col_445B8.use_property_decorate = False
                col_445B8.scale_x = 1.0
                col_445B8.scale_y = 1.0
                col_445B8.alignment = 'Expand'.upper()
                col_445B8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_445B8.separator(factor=0.5)
                attr_3E586 = '["' + str('Socket_104' + '"]') 
                col_445B8.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_3E586, text='Transition', icon_value=0, emboss=True)
                col_445B8.separator(factor=0.5)
            attr_939B0 = '["' + str('Socket_139' + '"]') 
            col_ED557.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_939B0, text='Invert', icon_value=0, emboss=True)


class SNA_OT_Enter_Weight_Paint_Mode_Db6F9(bpy.types.Operator):
    bl_idname = "sna.enter_weight_paint_mode_db6f9"
    bl_label = "Enter Weight Paint Mode"
    bl_description = "Enter weight paint mode to edit the VGroup"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='WEIGHT_PAINT', toggle=True)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_func_dynamics_8A9D6(layout_function, ):
    box_DA5F5 = layout_function.box()
    box_DA5F5.alert = False
    box_DA5F5.enabled = True
    box_DA5F5.active = True
    box_DA5F5.use_property_split = False
    box_DA5F5.use_property_decorate = False
    box_DA5F5.alignment = 'Expand'.upper()
    box_DA5F5.scale_x = 1.0
    box_DA5F5.scale_y = 1.0
    if not True: box_DA5F5.operator_context = "EXEC_DEFAULT"
    col_F128B = box_DA5F5.column(heading='', align=False)
    col_F128B.alert = False
    col_F128B.enabled = True
    col_F128B.active = True
    col_F128B.use_property_split = False
    col_F128B.use_property_decorate = False
    col_F128B.scale_x = 1.0
    col_F128B.scale_y = 1.0
    col_F128B.alignment = 'Expand'.upper()
    col_F128B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_D3E19 = col_F128B.row(heading='', align=False)
    row_D3E19.alert = False
    row_D3E19.enabled = True
    row_D3E19.active = True
    row_D3E19.use_property_split = False
    row_D3E19.use_property_decorate = False
    row_D3E19.scale_x = 1.0
    row_D3E19.scale_y = 1.0
    row_D3E19.alignment = 'Left'.upper()
    row_D3E19.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_D3E19.prop(bpy.context.scene, 'sna_display_dynamics', text='Dynamics', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_dynamics else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_display_dynamics:
        col_226C4 = col_F128B.column(heading='', align=False)
        col_226C4.alert = False
        col_226C4.enabled = True
        col_226C4.active = True
        col_226C4.use_property_split = False
        col_226C4.use_property_decorate = False
        col_226C4.scale_x = 1.0
        col_226C4.scale_y = 1.0
        col_226C4.alignment = 'Expand'.upper()
        col_226C4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_226C4.separator(factor=1.0)
        row_49A1C = col_226C4.row(heading='', align=True)
        row_49A1C.alert = False
        row_49A1C.enabled = True
        row_49A1C.active = True
        row_49A1C.use_property_split = False
        row_49A1C.use_property_decorate = False
        row_49A1C.scale_x = 1.0
        row_49A1C.scale_y = 1.0
        row_49A1C.alignment = 'Expand'.upper()
        row_49A1C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_49A1C.prop(bpy.context.scene, 'sna_display_wind', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_wind else string_to_icon('RIGHTARROW')), emboss=False)
        attr_C03F9 = '["' + str('Socket_144' + '"]') 
        row_49A1C.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_C03F9, text='Wind', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_wind:
            row_BDF4B = col_226C4.row(heading='', align=False)
            row_BDF4B.alert = False
            row_BDF4B.enabled = True
            row_BDF4B.active = True
            row_BDF4B.use_property_split = False
            row_BDF4B.use_property_decorate = False
            row_BDF4B.scale_x = 1.0
            row_BDF4B.scale_y = 1.0
            row_BDF4B.alignment = 'Expand'.upper()
            row_BDF4B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_BDF4B.label(text='', icon_value=string_to_icon('BLANK1'))
            col_A8EA6 = row_BDF4B.column(heading='', align=False)
            col_A8EA6.alert = False
            col_A8EA6.enabled = True
            col_A8EA6.active = True
            col_A8EA6.use_property_split = False
            col_A8EA6.use_property_decorate = False
            col_A8EA6.scale_x = 1.0
            col_A8EA6.scale_y = 1.0
            col_A8EA6.alignment = 'Expand'.upper()
            col_A8EA6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_A8EA6.separator(factor=1.0)
            col_A8EA6.label(text='Wind Settings:', icon_value=string_to_icon('FORCE_WIND'))
            col_A8EA6.separator(factor=0.25)
            attr_28135 = '["' + str('Socket_145' + '"]') 
            col_A8EA6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_28135, text='Strength', icon_value=0, emboss=True)
            attr_26CC5 = '["' + str('Socket_148' + '"]') 
            col_A8EA6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_26CC5, text='Speed', icon_value=0, emboss=True)
            attr_91EAD = '["' + str('Socket_146' + '"]') 
            col_A8EA6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_91EAD, text='Tilt', icon_value=0, emboss=True)
            attr_53222 = '["' + str('Socket_147' + '"]') 
            col_A8EA6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_53222, text='Direction', icon_value=0, emboss=True)
            attr_1CFFA = '["' + str('Socket_157' + '"]') 
            col_A8EA6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_1CFFA, text='Scale', icon_value=0, emboss=True)
            attr_3F30A = '["' + str('Socket_149' + '"]') 
            col_A8EA6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_3F30A, text='Z Offset', icon_value=0, emboss=True)
        col_226C4.separator(factor=1.0)
        row_032B1 = col_226C4.row(heading='', align=True)
        row_032B1.alert = False
        row_032B1.enabled = True
        row_032B1.active = True
        row_032B1.use_property_split = False
        row_032B1.use_property_decorate = False
        row_032B1.scale_x = 1.0
        row_032B1.scale_y = 1.0
        row_032B1.alignment = 'Expand'.upper()
        row_032B1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_032B1.prop(bpy.context.scene, 'sna_display_collision', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_collision else string_to_icon('RIGHTARROW')), emboss=False)
        attr_6B05A = '["' + str('Socket_151' + '"]') 
        row_032B1.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_6B05A, text='Collision', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_collision:
            row_015A5 = col_226C4.row(heading='', align=False)
            row_015A5.alert = False
            row_015A5.enabled = True
            row_015A5.active = True
            row_015A5.use_property_split = False
            row_015A5.use_property_decorate = False
            row_015A5.scale_x = 1.0
            row_015A5.scale_y = 1.0
            row_015A5.alignment = 'Expand'.upper()
            row_015A5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_015A5.label(text='', icon_value=string_to_icon('BLANK1'))
            col_CFC3F = row_015A5.column(heading='', align=False)
            col_CFC3F.alert = False
            col_CFC3F.enabled = True
            col_CFC3F.active = True
            col_CFC3F.use_property_split = False
            col_CFC3F.use_property_decorate = False
            col_CFC3F.scale_x = 1.0
            col_CFC3F.scale_y = 1.0
            col_CFC3F.alignment = 'Expand'.upper()
            col_CFC3F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_CFC3F.separator(factor=1.0)
            col_CFC3F.label(text='Collision Object', icon_value=string_to_icon('RADIOBUT_ON'))
            attr_8E90F = '["' + str('Socket_152' + '"]') 
            col_CFC3F.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_8E90F, text='', icon_value=0, emboss=True)
            col_CFC3F.separator(factor=1.0)
            col_CFC3F.label(text='Distance:', icon_value=string_to_icon('DRIVER_DISTANCE'))
            attr_6107F = '["' + str('Socket_153' + '"]') 
            col_CFC3F.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_6107F, text='Min', icon_value=0, emboss=True)
            attr_7E065 = '["' + str('Socket_154' + '"]') 
            col_CFC3F.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_7E065, text='Max', icon_value=0, emboss=True)


def sna_func_ecosystem_883DD(layout_function, ):
    box_045CF = layout_function.box()
    box_045CF.alert = False
    box_045CF.enabled = True
    box_045CF.active = True
    box_045CF.use_property_split = False
    box_045CF.use_property_decorate = False
    box_045CF.alignment = 'Expand'.upper()
    box_045CF.scale_x = 1.0
    box_045CF.scale_y = 1.0
    if not True: box_045CF.operator_context = "EXEC_DEFAULT"
    col_DE195 = box_045CF.column(heading='', align=False)
    col_DE195.alert = False
    col_DE195.enabled = True
    col_DE195.active = True
    col_DE195.use_property_split = False
    col_DE195.use_property_decorate = False
    col_DE195.scale_x = 1.0
    col_DE195.scale_y = 1.0
    col_DE195.alignment = 'Expand'.upper()
    col_DE195.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_8DA1A = col_DE195.row(heading='', align=False)
    row_8DA1A.alert = False
    row_8DA1A.enabled = True
    row_8DA1A.active = True
    row_8DA1A.use_property_split = False
    row_8DA1A.use_property_decorate = False
    row_8DA1A.scale_x = 1.0
    row_8DA1A.scale_y = 1.0
    row_8DA1A.alignment = 'Left'.upper()
    row_8DA1A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_8DA1A.prop(bpy.context.scene, 'sna_display_ecosystem', text='Ecosystem', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_ecosystem else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_display_ecosystem:
        col_973C2 = col_DE195.column(heading='', align=False)
        col_973C2.alert = False
        col_973C2.enabled = True
        col_973C2.active = True
        col_973C2.use_property_split = False
        col_973C2.use_property_decorate = False
        col_973C2.scale_x = 1.0
        col_973C2.scale_y = 1.0
        col_973C2.alignment = 'Expand'.upper()
        col_973C2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_973C2.separator(factor=1.0)
        col_96597 = col_973C2.column(heading='', align=False)
        col_96597.alert = False
        col_96597.enabled = True
        col_96597.active = True
        col_96597.use_property_split = False
        col_96597.use_property_decorate = False
        col_96597.scale_x = 1.0
        col_96597.scale_y = 1.0
        col_96597.alignment = 'Expand'.upper()
        col_96597.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_5BEDA = col_96597.row(heading='', align=True)
        row_5BEDA.alert = False
        row_5BEDA.enabled = True
        row_5BEDA.active = True
        row_5BEDA.use_property_split = False
        row_5BEDA.use_property_decorate = False
        row_5BEDA.scale_x = 1.0
        row_5BEDA.scale_y = 1.0
        row_5BEDA.alignment = 'Expand'.upper()
        row_5BEDA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_5BEDA.prop(bpy.context.scene, 'sna_display_attraction', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_attraction else string_to_icon('RIGHTARROW')), emboss=False)
        attr_70345 = '["' + str('Socket_161' + '"]') 
        row_5BEDA.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_70345, text='Attraction', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_attraction:
            row_DAB93 = col_96597.row(heading='', align=False)
            row_DAB93.alert = False
            row_DAB93.enabled = True
            row_DAB93.active = True
            row_DAB93.use_property_split = False
            row_DAB93.use_property_decorate = False
            row_DAB93.scale_x = 1.0
            row_DAB93.scale_y = 1.0
            row_DAB93.alignment = 'Expand'.upper()
            row_DAB93.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_DAB93.label(text='', icon_value=string_to_icon('BLANK1'))
            col_F101B = row_DAB93.column(heading='', align=False)
            col_F101B.alert = False
            col_F101B.enabled = True
            col_F101B.active = True
            col_F101B.use_property_split = False
            col_F101B.use_property_decorate = False
            col_F101B.scale_x = 1.0
            col_F101B.scale_y = 1.0
            col_F101B.alignment = 'Expand'.upper()
            col_F101B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_F101B.separator(factor=1.0)
            col_F101B.label(text='Scatter System:', icon_value=string_to_icon('SYSTEM'))
            col_F101B.prop_search(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], '["Socket_162"]', bpy.data.collections['Scatter Systems'], 'objects', text='', icon='COLLAPSEMENU')
            if (bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_162'] == bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name]):
                col_7581C = col_F101B.column(heading='', align=False)
                col_7581C.alert = True
                col_7581C.enabled = True
                col_7581C.active = True
                col_7581C.use_property_split = False
                col_7581C.use_property_decorate = False
                col_7581C.scale_x = 1.0
                col_7581C.scale_y = 1.0
                col_7581C.alignment = 'Expand'.upper()
                col_7581C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_7581C.label(text="Can't be the same as the current system!", icon_value=string_to_icon('WARNING_LARGE'))
            col_F101B.separator(factor=1.0)
            col_F101B.label(text='Attraction Properties', icon_value=0)
            attr_BE703 = '["' + str('Socket_163' + '"]') 
            col_F101B.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_BE703, text='Distance', icon_value=0, emboss=True)
            attr_715A6 = '["' + str('Socket_164' + '"]') 
            col_F101B.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_715A6, text='Smooth Transition', icon_value=0, emboss=True)
            if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_164']:
                row_49E5B = col_F101B.row(heading='', align=False)
                row_49E5B.alert = False
                row_49E5B.enabled = True
                row_49E5B.active = True
                row_49E5B.use_property_split = False
                row_49E5B.use_property_decorate = False
                row_49E5B.scale_x = 1.0
                row_49E5B.scale_y = 1.0
                row_49E5B.alignment = 'Expand'.upper()
                row_49E5B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_49E5B.label(text='', icon_value=string_to_icon('BLANK1'))
                col_91D2F = row_49E5B.column(heading='', align=False)
                col_91D2F.alert = False
                col_91D2F.enabled = True
                col_91D2F.active = True
                col_91D2F.use_property_split = False
                col_91D2F.use_property_decorate = False
                col_91D2F.scale_x = 1.0
                col_91D2F.scale_y = 1.0
                col_91D2F.alignment = 'Expand'.upper()
                col_91D2F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_91D2F.separator(factor=0.25)
                attr_09CF9 = '["' + str('Socket_165' + '"]') 
                col_91D2F.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_09CF9, text='Transition', icon_value=0, emboss=True)
        col_973C2.separator(factor=1.0)
        col_52C74 = col_973C2.column(heading='', align=False)
        col_52C74.alert = False
        col_52C74.enabled = True
        col_52C74.active = True
        col_52C74.use_property_split = False
        col_52C74.use_property_decorate = False
        col_52C74.scale_x = 1.0
        col_52C74.scale_y = 1.0
        col_52C74.alignment = 'Expand'.upper()
        col_52C74.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_4FD67 = col_52C74.row(heading='', align=True)
        row_4FD67.alert = False
        row_4FD67.enabled = True
        row_4FD67.active = True
        row_4FD67.use_property_split = False
        row_4FD67.use_property_decorate = False
        row_4FD67.scale_x = 1.0
        row_4FD67.scale_y = 1.0
        row_4FD67.alignment = 'Expand'.upper()
        row_4FD67.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_4FD67.prop(bpy.context.scene, 'sna_display_repulsion', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_repulsion else string_to_icon('RIGHTARROW')), emboss=False)
        attr_8878D = '["' + str('Socket_166' + '"]') 
        row_4FD67.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_8878D, text='Repulsion', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_repulsion:
            row_0BF98 = col_52C74.row(heading='', align=False)
            row_0BF98.alert = False
            row_0BF98.enabled = True
            row_0BF98.active = True
            row_0BF98.use_property_split = False
            row_0BF98.use_property_decorate = False
            row_0BF98.scale_x = 1.0
            row_0BF98.scale_y = 1.0
            row_0BF98.alignment = 'Expand'.upper()
            row_0BF98.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_0BF98.label(text='', icon_value=string_to_icon('BLANK1'))
            col_12930 = row_0BF98.column(heading='', align=False)
            col_12930.alert = False
            col_12930.enabled = True
            col_12930.active = True
            col_12930.use_property_split = False
            col_12930.use_property_decorate = False
            col_12930.scale_x = 1.0
            col_12930.scale_y = 1.0
            col_12930.alignment = 'Expand'.upper()
            col_12930.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_12930.separator(factor=1.0)
            col_12930.label(text='Scatter System:', icon_value=string_to_icon('SYSTEM'))
            col_12930.prop_search(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], '["Socket_167"]', bpy.data.collections['Scatter Systems'], 'objects', text='', icon='COLLAPSEMENU')
            if (bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_167'] == bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name]):
                col_0A7EE = col_12930.column(heading='', align=False)
                col_0A7EE.alert = True
                col_0A7EE.enabled = True
                col_0A7EE.active = True
                col_0A7EE.use_property_split = False
                col_0A7EE.use_property_decorate = False
                col_0A7EE.scale_x = 1.0
                col_0A7EE.scale_y = 1.0
                col_0A7EE.alignment = 'Expand'.upper()
                col_0A7EE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_0A7EE.label(text="Can't be the same as the current system!", icon_value=string_to_icon('WARNING_LARGE'))
            col_12930.separator(factor=1.0)
            col_12930.label(text='Repulsion Properties', icon_value=0)
            attr_3C695 = '["' + str('Socket_168' + '"]') 
            col_12930.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_3C695, text='Distance', icon_value=0, emboss=True)
            attr_01263 = '["' + str('Socket_169' + '"]') 
            col_12930.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_01263, text='Smooth Transition', icon_value=0, emboss=True)
            if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_169']:
                row_ADA99 = col_12930.row(heading='', align=False)
                row_ADA99.alert = False
                row_ADA99.enabled = True
                row_ADA99.active = True
                row_ADA99.use_property_split = False
                row_ADA99.use_property_decorate = False
                row_ADA99.scale_x = 1.0
                row_ADA99.scale_y = 1.0
                row_ADA99.alignment = 'Expand'.upper()
                row_ADA99.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_ADA99.label(text='', icon_value=string_to_icon('BLANK1'))
                col_F3368 = row_ADA99.column(heading='', align=False)
                col_F3368.alert = False
                col_F3368.enabled = True
                col_F3368.active = True
                col_F3368.use_property_split = False
                col_F3368.use_property_decorate = False
                col_F3368.scale_x = 1.0
                col_F3368.scale_y = 1.0
                col_F3368.alignment = 'Expand'.upper()
                col_F3368.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_F3368.separator(factor=0.25)
                attr_66837 = '["' + str('Socket_170' + '"]') 
                col_F3368.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_66837, text='Transition', icon_value=0, emboss=True)


def sna_func_emitter_0797E(layout_function, ):
    layout_function.prop(bpy.context.scene, 'sna_emitter_object', text='Emitter', icon_value=0, emboss=True)
    if (bpy.context.scene.sna_emitter_object == None):
        box_5E011 = layout_function.box()
        box_5E011.alert = False
        box_5E011.enabled = True
        box_5E011.active = True
        box_5E011.use_property_split = False
        box_5E011.use_property_decorate = False
        box_5E011.alignment = 'Expand'.upper()
        box_5E011.scale_x = 1.0
        box_5E011.scale_y = 1.0
        if not True: box_5E011.operator_context = "EXEC_DEFAULT"
        col_C61DC = box_5E011.column(heading='', align=True)
        col_C61DC.alert = False
        col_C61DC.enabled = True
        col_C61DC.active = True
        col_C61DC.use_property_split = False
        col_C61DC.use_property_decorate = False
        col_C61DC.scale_x = 1.0
        col_C61DC.scale_y = 1.0
        col_C61DC.alignment = 'Expand'.upper()
        col_C61DC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_A8147 = col_C61DC.row(heading='', align=True)
        row_A8147.alert = False
        row_A8147.enabled = True
        row_A8147.active = True
        row_A8147.use_property_split = False
        row_A8147.use_property_decorate = False
        row_A8147.scale_x = 1.0
        row_A8147.scale_y = 1.0
        row_A8147.alignment = 'Center'.upper()
        row_A8147.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_A8147.label(text='Choose an emitter object using the tool above!', icon_value=string_to_icon('INFO'))
        col_C61DC.separator(factor=1.0)
        row_3476A = col_C61DC.row(heading='', align=True)
        row_3476A.alert = False
        row_3476A.enabled = True
        row_3476A.active = True
        row_3476A.use_property_split = False
        row_3476A.use_property_decorate = False
        row_3476A.scale_x = 1.0
        row_3476A.scale_y = 1.0
        row_3476A.alignment = 'Center'.upper()
        row_3476A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_3476A.label(text='Emitter objects store info about your scatter systems', icon_value=0)
        row_0FD41 = col_C61DC.row(heading='', align=True)
        row_0FD41.alert = False
        row_0FD41.enabled = True
        row_0FD41.active = True
        row_0FD41.use_property_split = False
        row_0FD41.use_property_decorate = False
        row_0FD41.scale_x = 1.0
        row_0FD41.scale_y = 1.0
        row_0FD41.alignment = 'Center'.upper()
        row_0FD41.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_0FD41.label(text="and control where you'll scatter.", icon_value=0)
        col_C61DC.separator(factor=1.0)
        row_A77EA = col_C61DC.row(heading='', align=True)
        row_A77EA.alert = False
        row_A77EA.enabled = True
        row_A77EA.active = True
        row_A77EA.use_property_split = False
        row_A77EA.use_property_decorate = False
        row_A77EA.scale_x = 1.0
        row_A77EA.scale_y = 1.0
        row_A77EA.alignment = 'Center'.upper()
        row_A77EA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_A77EA.label(text='You can switch emitter at any time using the tool above!', icon_value=0)


def sna_func_instances_B4607(layout_function, ):
    box_1D440 = layout_function.box()
    box_1D440.alert = False
    box_1D440.enabled = True
    box_1D440.active = True
    box_1D440.use_property_split = False
    box_1D440.use_property_decorate = False
    box_1D440.alignment = 'Expand'.upper()
    box_1D440.scale_x = 1.0
    box_1D440.scale_y = 1.0
    if not True: box_1D440.operator_context = "EXEC_DEFAULT"
    col_BAF6D = box_1D440.column(heading='', align=False)
    col_BAF6D.alert = False
    col_BAF6D.enabled = True
    col_BAF6D.active = True
    col_BAF6D.use_property_split = False
    col_BAF6D.use_property_decorate = False
    col_BAF6D.scale_x = 1.0
    col_BAF6D.scale_y = 1.0
    col_BAF6D.alignment = 'Expand'.upper()
    col_BAF6D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_39AAE = col_BAF6D.row(heading='', align=False)
    row_39AAE.alert = False
    row_39AAE.enabled = True
    row_39AAE.active = True
    row_39AAE.use_property_split = False
    row_39AAE.use_property_decorate = False
    row_39AAE.scale_x = 1.0
    row_39AAE.scale_y = 1.0
    row_39AAE.alignment = 'Left'.upper()
    row_39AAE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_39AAE.prop(bpy.context.scene, 'sna_displayinstances', text='Instances', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_displayinstances else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_displayinstances:
        col_BAF6D.separator(factor=1.0)
        col_BAF6D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name], 'sna_instance_type', text='Type', icon_value=0, emboss=True)
        col_BAF6D.separator(factor=1.0)
        if (bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].sna_instance_type == 'Multiple Instances'):
            col_BAF6D.prop_search(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], '["Socket_31"]', bpy.context.scene.collection, 'children', text='', icon='OUTLINER_COLLECTION')
        else:
            attr_10A44 = '["' + str('Socket_29' + '"]') 
            col_BAF6D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_10A44, text='', icon_value=0, emboss=True)


def sna_func_optimization_DB30B(layout_function, ):
    box_583E3 = layout_function.box()
    box_583E3.alert = False
    box_583E3.enabled = True
    box_583E3.active = True
    box_583E3.use_property_split = False
    box_583E3.use_property_decorate = False
    box_583E3.alignment = 'Expand'.upper()
    box_583E3.scale_x = 1.0
    box_583E3.scale_y = 1.0
    if not True: box_583E3.operator_context = "EXEC_DEFAULT"
    col_E9069 = box_583E3.column(heading='', align=False)
    col_E9069.alert = False
    col_E9069.enabled = True
    col_E9069.active = True
    col_E9069.use_property_split = False
    col_E9069.use_property_decorate = False
    col_E9069.scale_x = 1.0
    col_E9069.scale_y = 1.0
    col_E9069.alignment = 'Expand'.upper()
    col_E9069.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_14FD4 = col_E9069.row(heading='', align=False)
    row_14FD4.alert = False
    row_14FD4.enabled = True
    row_14FD4.active = True
    row_14FD4.use_property_split = False
    row_14FD4.use_property_decorate = False
    row_14FD4.scale_x = 1.0
    row_14FD4.scale_y = 1.0
    row_14FD4.alignment = 'Left'.upper()
    row_14FD4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_14FD4.prop(bpy.context.scene, 'sna_display_optimization', text='Optimization', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_optimization else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_display_optimization:
        col_649E5 = col_E9069.column(heading='', align=False)
        col_649E5.alert = False
        col_649E5.enabled = True
        col_649E5.active = True
        col_649E5.use_property_split = False
        col_649E5.use_property_decorate = False
        col_649E5.scale_x = 1.0
        col_649E5.scale_y = 1.0
        col_649E5.alignment = 'Expand'.upper()
        col_649E5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_93E61 = col_649E5.column(heading='', align=False)
        col_93E61.alert = False
        col_93E61.enabled = True
        col_93E61.active = True
        col_93E61.use_property_split = False
        col_93E61.use_property_decorate = False
        col_93E61.scale_x = 1.0
        col_93E61.scale_y = 1.0
        col_93E61.alignment = 'Expand'.upper()
        col_93E61.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_93E61.separator(factor=1.0)
        row_A5FB1 = col_93E61.row(heading='', align=True)
        row_A5FB1.alert = False
        row_A5FB1.enabled = True
        row_A5FB1.active = True
        row_A5FB1.use_property_split = False
        row_A5FB1.use_property_decorate = False
        row_A5FB1.scale_x = 1.0
        row_A5FB1.scale_y = 1.0
        row_A5FB1.alignment = 'Expand'.upper()
        row_A5FB1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_A5FB1.prop(bpy.context.scene, 'sna_display_decrease_viewport_density', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_decrease_viewport_density else string_to_icon('RIGHTARROW')), emboss=False)
        attr_CFF68 = '["' + str('Socket_121' + '"]') 
        row_A5FB1.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_CFF68, text='Decrease Viewport Density', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_decrease_viewport_density:
            row_408EF = col_93E61.row(heading='', align=False)
            row_408EF.alert = False
            row_408EF.enabled = True
            row_408EF.active = True
            row_408EF.use_property_split = False
            row_408EF.use_property_decorate = False
            row_408EF.scale_x = 1.0
            row_408EF.scale_y = 1.0
            row_408EF.alignment = 'Expand'.upper()
            row_408EF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_408EF.label(text='', icon_value=string_to_icon('BLANK1'))
            col_6519E = row_408EF.column(heading='', align=False)
            col_6519E.alert = False
            col_6519E.enabled = True
            col_6519E.active = True
            col_6519E.use_property_split = False
            col_6519E.use_property_decorate = False
            col_6519E.scale_x = 1.0
            col_6519E.scale_y = 1.0
            col_6519E.alignment = 'Expand'.upper()
            col_6519E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_6519E.separator(factor=1.0)
            attr_5EF73 = '["' + str('Socket_141' + '"]') 
            col_6519E.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_5EF73, text='Viewport Density', icon_value=0, emboss=True)
        col_5E461 = col_649E5.column(heading='', align=False)
        col_5E461.alert = False
        col_5E461.enabled = True
        col_5E461.active = True
        col_5E461.use_property_split = False
        col_5E461.use_property_decorate = False
        col_5E461.scale_x = 1.0
        col_5E461.scale_y = 1.0
        col_5E461.alignment = 'Expand'.upper()
        col_5E461.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_5E461.separator(factor=1.0)
        row_11677 = col_5E461.row(heading='', align=True)
        row_11677.alert = False
        row_11677.enabled = True
        row_11677.active = True
        row_11677.use_property_split = False
        row_11677.use_property_decorate = False
        row_11677.scale_x = 1.0
        row_11677.scale_y = 1.0
        row_11677.alignment = 'Expand'.upper()
        row_11677.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_11677.prop(bpy.context.scene, 'sna_display_use_optimized_mesh', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_use_optimized_mesh else string_to_icon('RIGHTARROW')), emboss=False)
        attr_FD06A = '["' + str('Socket_122' + '"]') 
        row_11677.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_FD06A, text='Optimized Mesh', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_use_optimized_mesh:
            row_2B14B = col_5E461.row(heading='', align=False)
            row_2B14B.alert = False
            row_2B14B.enabled = True
            row_2B14B.active = True
            row_2B14B.use_property_split = False
            row_2B14B.use_property_decorate = False
            row_2B14B.scale_x = 1.0
            row_2B14B.scale_y = 1.0
            row_2B14B.alignment = 'Expand'.upper()
            row_2B14B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_2B14B.label(text='', icon_value=string_to_icon('BLANK1'))
            col_D57E2 = row_2B14B.column(heading='', align=False)
            col_D57E2.alert = False
            col_D57E2.enabled = True
            col_D57E2.active = True
            col_D57E2.use_property_split = False
            col_D57E2.use_property_decorate = False
            col_D57E2.scale_x = 1.0
            col_D57E2.scale_y = 1.0
            col_D57E2.alignment = 'Expand'.upper()
            col_D57E2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_D57E2.separator(factor=1.0)
            attr_20540 = '["' + str('Socket_123' + '"]') 
            col_D57E2.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_20540, text='Type', icon_value=0, emboss=True)
            if (bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_123'] == 2):
                col_D57E2.separator(factor=1.0)
                attr_BCCD2 = '["' + str('Socket_191' + '"]') 
                col_D57E2.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_BCCD2, text='Object', icon_value=0, emboss=True)
                col_D57E2.separator(factor=1.0)
                attr_B3E8A = '["' + str('Socket_193' + '"]') 
                col_D57E2.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_B3E8A, text='Proxy Scale', icon_value=0, emboss=True)
        col_82F39 = col_649E5.column(heading='', align=False)
        col_82F39.alert = False
        col_82F39.enabled = True
        col_82F39.active = True
        col_82F39.use_property_split = False
        col_82F39.use_property_decorate = False
        col_82F39.scale_x = 1.0
        col_82F39.scale_y = 1.0
        col_82F39.alignment = 'Expand'.upper()
        col_82F39.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_82F39.separator(factor=1.0)
        row_7A000 = col_82F39.row(heading='', align=True)
        row_7A000.alert = False
        row_7A000.enabled = True
        row_7A000.active = True
        row_7A000.use_property_split = False
        row_7A000.use_property_decorate = False
        row_7A000.scale_x = 1.0
        row_7A000.scale_y = 1.0
        row_7A000.alignment = 'Expand'.upper()
        row_7A000.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_7A000.prop(bpy.context.scene, 'sna_display_enable_camera_culling', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_enable_camera_culling else string_to_icon('RIGHTARROW')), emboss=False)
        attr_AF4DA = '["' + str('Socket_125' + '"]') 
        row_7A000.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_AF4DA, text='Camera Culling', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_enable_camera_culling:
            row_7D62F = col_82F39.row(heading='', align=False)
            row_7D62F.alert = False
            row_7D62F.enabled = True
            row_7D62F.active = True
            row_7D62F.use_property_split = False
            row_7D62F.use_property_decorate = False
            row_7D62F.scale_x = 1.0
            row_7D62F.scale_y = 1.0
            row_7D62F.alignment = 'Expand'.upper()
            row_7D62F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_7D62F.label(text='', icon_value=string_to_icon('BLANK1'))
            col_949FE = row_7D62F.column(heading='', align=False)
            col_949FE.alert = False
            col_949FE.enabled = True
            col_949FE.active = True
            col_949FE.use_property_split = False
            col_949FE.use_property_decorate = False
            col_949FE.scale_x = 1.0
            col_949FE.scale_y = 1.0
            col_949FE.alignment = 'Expand'.upper()
            col_949FE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_949FE.separator(factor=1.0)
            col_949FE.label(text='FOV:', icon_value=string_to_icon('CAMERA_DATA'))
            attr_6C26E = '["' + str('Socket_126' + '"]') 
            col_949FE.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_6C26E, text='Width', icon_value=0, emboss=True)
            attr_5E0B6 = '["' + str('Socket_127' + '"]') 
            col_949FE.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_5E0B6, text='Height', icon_value=0, emboss=True)
            col_949FE.separator(factor=1.0)
            col_949FE.label(text='Clipping', icon_value=string_to_icon('DRIVER_DISTANCE'))
            attr_49024 = '["' + str('Socket_128' + '"]') 
            col_949FE.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_49024, text='Clip Start', icon_value=0, emboss=True)
            attr_031A7 = '["' + str('Socket_129' + '"]') 
            col_949FE.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_031A7, text='Clip End', icon_value=0, emboss=True)


class SNA_AddonPreferences_14B35(bpy.types.AddonPreferences):
    bl_idname = __package__
    sna_auto_scene_switch_detection: bpy.props.BoolProperty(name='Auto Scene Switch Detection', description='Automatically detects when you switch scene and refreshes the visibility of scatter systems to match. This feature is experimental and can cause issues', default=False)
    sna_default_density: bpy.props.FloatProperty(name='Default Density', description='Controls what the density of scatter systems will be when created', default=10.0, subtype='NONE', unit='NONE', step=3, precision=3)
    sna_bounding_box: bpy.props.BoolProperty(name='Bounding Box', description='If enabled, new scatter systems will have the bounding box feature enabled by default which can help save computer resources', default=False)
    sna_align_to_surface: bpy.props.BoolProperty(name='Align to Surface', description='When enabled, new scatter systems will be aligned to the surface of the emitter object', default=False)
    sna_default_scale: bpy.props.FloatProperty(name='Default Scale', description='Controls what the default scale of scatter systems when created', default=1.0, subtype='NONE', unit='NONE', step=3, precision=3)
    sna_random_scale: bpy.props.BoolProperty(name='Random Scale', description='When enabled, new scatter systems will have the random scale feature enabled', default=False)
    sna_random_rotation: bpy.props.BoolProperty(name='Random Rotation', description='When enabled, new scatter systems will be randomly rotated', default=False)

    def draw(self, context):
        if not (False):
            layout = self.layout 
            box_B7037 = layout.box()
            box_B7037.alert = False
            box_B7037.enabled = True
            box_B7037.active = True
            box_B7037.use_property_split = False
            box_B7037.use_property_decorate = False
            box_B7037.alignment = 'Expand'.upper()
            box_B7037.scale_x = 1.0
            box_B7037.scale_y = 1.0
            if not True: box_B7037.operator_context = "EXEC_DEFAULT"
            box_B7037.prop(bpy.context.scene, 'sna_display_preferences_settings', text='Settings', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_preferences_settings else string_to_icon('RIGHTARROW')), emboss=False)
            if bpy.context.scene.sna_display_preferences_settings:
                col_A12E2 = box_B7037.column(heading='', align=False)
                col_A12E2.alert = False
                col_A12E2.enabled = True
                col_A12E2.active = True
                col_A12E2.use_property_split = False
                col_A12E2.use_property_decorate = False
                col_A12E2.scale_x = 1.0
                col_A12E2.scale_y = 1.0
                col_A12E2.alignment = 'Expand'.upper()
                col_A12E2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                box_E8703 = col_A12E2.box()
                box_E8703.alert = False
                box_E8703.enabled = True
                box_E8703.active = True
                box_E8703.use_property_split = False
                box_E8703.use_property_decorate = False
                box_E8703.alignment = 'Expand'.upper()
                box_E8703.scale_x = 1.0
                box_E8703.scale_y = 1.0
                if not True: box_E8703.operator_context = "EXEC_DEFAULT"
                box_E8703.prop(bpy.context.scene, 'sna_display_default_values', text='Defaults', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_default_values else string_to_icon('RIGHTARROW')), emboss=False)
                if bpy.context.scene.sna_display_default_values:
                    col_4BC51 = box_E8703.column(heading='', align=False)
                    col_4BC51.alert = False
                    col_4BC51.enabled = True
                    col_4BC51.active = True
                    col_4BC51.use_property_split = False
                    col_4BC51.use_property_decorate = False
                    col_4BC51.scale_x = 1.0
                    col_4BC51.scale_y = 1.0
                    col_4BC51.alignment = 'Expand'.upper()
                    col_4BC51.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    col_4BC51.label(text='Float Values', icon_value=61)
                    col_4BC51.prop(bpy.context.preferences.addons[__package__].preferences, 'sna_default_density', text='Density', icon_value=0, emboss=True)
                    col_4BC51.prop(bpy.context.preferences.addons[__package__].preferences, 'sna_default_scale', text='Scale', icon_value=0, emboss=True)
                    col_4BC51.separator(factor=1.0)
                    col_4BC51.label(text='Feature Toggles', icon_value=5)
                    col_4BC51.prop(bpy.context.preferences.addons[__package__].preferences, 'sna_random_scale', text='Random Scale', icon_value=(string_to_icon('CHECKBOX_HLT') if bpy.context.preferences.addons[__package__].preferences.sna_random_scale else string_to_icon('CHECKBOX_DEHLT')), emboss=True)
                    col_4BC51.prop(bpy.context.preferences.addons[__package__].preferences, 'sna_random_rotation', text='Random Rotation', icon_value=(string_to_icon('CHECKBOX_HLT') if bpy.context.preferences.addons[__package__].preferences.sna_random_rotation else string_to_icon('CHECKBOX_DEHLT')), emboss=True)
                    col_4BC51.prop(bpy.context.preferences.addons[__package__].preferences, 'sna_align_to_surface', text='Align to Surface', icon_value=(string_to_icon('CHECKBOX_HLT') if bpy.context.preferences.addons[__package__].preferences.sna_align_to_surface else string_to_icon('CHECKBOX_DEHLT')), emboss=True)
                    col_4BC51.prop(bpy.context.preferences.addons[__package__].preferences, 'sna_bounding_box', text='Bounding Box', icon_value=(string_to_icon('CHECKBOX_HLT') if bpy.context.preferences.addons[__package__].preferences.sna_bounding_box else string_to_icon('CHECKBOX_DEHLT')), emboss=True)
                col_A12E2.separator(factor=0.0)
                box_C65D7 = col_A12E2.box()
                box_C65D7.alert = False
                box_C65D7.enabled = True
                box_C65D7.active = True
                box_C65D7.use_property_split = False
                box_C65D7.use_property_decorate = False
                box_C65D7.alignment = 'Expand'.upper()
                box_C65D7.scale_x = 1.0
                box_C65D7.scale_y = 1.0
                if not True: box_C65D7.operator_context = "EXEC_DEFAULT"
                box_C65D7.prop(bpy.context.scene, 'sna_display_auto_scene_switch_detection', text='Scene Detection (Experimental)', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_auto_scene_switch_detection else string_to_icon('RIGHTARROW')), emboss=False)
                if bpy.context.scene.sna_display_auto_scene_switch_detection:
                    col_9E438 = box_C65D7.column(heading='', align=False)
                    col_9E438.alert = True
                    col_9E438.enabled = True
                    col_9E438.active = True
                    col_9E438.use_property_split = False
                    col_9E438.use_property_decorate = False
                    col_9E438.scale_x = 1.0
                    col_9E438.scale_y = 1.0
                    col_9E438.alignment = 'Expand'.upper()
                    col_9E438.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    row_862C6 = col_9E438.row(heading='', align=True)
                    row_862C6.alert = False
                    row_862C6.enabled = True
                    row_862C6.active = True
                    row_862C6.use_property_split = False
                    row_862C6.use_property_decorate = False
                    row_862C6.scale_x = 0.9599999785423279
                    row_862C6.scale_y = 1.0
                    row_862C6.alignment = 'Left'.upper()
                    row_862C6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    row_862C6.prop(bpy.context.preferences.addons[__package__].preferences, 'sna_auto_scene_switch_detection', text='Automatic Scene Switch Detection', icon_value=0, emboss=True)
                    op = row_862C6.operator('sna.documentation_7e9c9', text='', icon_value=44, emboss=False, depress=False)
                    op.sna_url = 'https://openscatter.notion.site/Automatic-Scene-Switch-Detection-1af0def6628280d7b523d6bdd61f5b5e'
                    col_9CB80 = col_9E438.column(heading='', align=True)
                    col_9CB80.alert = True
                    col_9CB80.enabled = True
                    col_9CB80.active = True
                    col_9CB80.use_property_split = False
                    col_9CB80.use_property_decorate = False
                    col_9CB80.scale_x = 1.0
                    col_9CB80.scale_y = 1.0
                    col_9CB80.alignment = 'Left'.upper()
                    col_9CB80.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                    col_9CB80.label(text='This feature is highly experimental and not recommended unless you switch between scenes very often.', icon_value=0)
                    col_9CB80.label(text="If you're not sure what it does, please read the documentation.", icon_value=0)


class SNA_OT_Documentation_7E9C9(bpy.types.Operator):
    bl_idname = "sna.documentation_7e9c9"
    bl_label = "Documentation"
    bl_description = "Open the documentation for information about this feature"
    bl_options = {"REGISTER", "UNDO"}
    sna_url: bpy.props.StringProperty(name='URL', description='', default='', subtype='NONE', maxlen=0)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_open_url_func_12FC5(self.sna_url)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_open_url_func_12FC5(URL):
    bpy.ops.wm.url_open('INVOKE_DEFAULT', url=URL)


def sna_func_proximity_773E1(layout_function, ):
    box_BD9AC = layout_function.box()
    box_BD9AC.alert = False
    box_BD9AC.enabled = True
    box_BD9AC.active = True
    box_BD9AC.use_property_split = False
    box_BD9AC.use_property_decorate = False
    box_BD9AC.alignment = 'Expand'.upper()
    box_BD9AC.scale_x = 1.0
    box_BD9AC.scale_y = 1.0
    if not True: box_BD9AC.operator_context = "EXEC_DEFAULT"
    col_46C7B = box_BD9AC.column(heading='', align=False)
    col_46C7B.alert = False
    col_46C7B.enabled = True
    col_46C7B.active = True
    col_46C7B.use_property_split = False
    col_46C7B.use_property_decorate = False
    col_46C7B.scale_x = 1.0
    col_46C7B.scale_y = 1.0
    col_46C7B.alignment = 'Expand'.upper()
    col_46C7B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_89EB6 = col_46C7B.row(heading='', align=False)
    row_89EB6.alert = False
    row_89EB6.enabled = True
    row_89EB6.active = True
    row_89EB6.use_property_split = False
    row_89EB6.use_property_decorate = False
    row_89EB6.scale_x = 1.0
    row_89EB6.scale_y = 1.0
    row_89EB6.alignment = 'Left'.upper()
    row_89EB6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_89EB6.prop(bpy.context.scene, 'sna_display_proximity', text='Proximity', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_proximity else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_display_proximity:
        col_2271A = col_46C7B.column(heading='', align=False)
        col_2271A.alert = False
        col_2271A.enabled = True
        col_2271A.active = True
        col_2271A.use_property_split = False
        col_2271A.use_property_decorate = False
        col_2271A.scale_x = 1.0
        col_2271A.scale_y = 1.0
        col_2271A.alignment = 'Expand'.upper()
        col_2271A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_D1B09 = col_2271A.column(heading='', align=False)
        col_D1B09.alert = False
        col_D1B09.enabled = True
        col_D1B09.active = True
        col_D1B09.use_property_split = False
        col_D1B09.use_property_decorate = False
        col_D1B09.scale_x = 1.0
        col_D1B09.scale_y = 1.0
        col_D1B09.alignment = 'Expand'.upper()
        col_D1B09.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_D1B09.separator(factor=1.0)
        row_5AD7E = col_D1B09.row(heading='', align=True)
        row_5AD7E.alert = False
        row_5AD7E.enabled = True
        row_5AD7E.active = True
        row_5AD7E.use_property_split = False
        row_5AD7E.use_property_decorate = False
        row_5AD7E.scale_x = 1.0
        row_5AD7E.scale_y = 1.0
        row_5AD7E.alignment = 'Expand'.upper()
        row_5AD7E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_5AD7E.prop(bpy.context.scene, 'sna_display_geometry_proximity', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_geometry_proximity else string_to_icon('RIGHTARROW')), emboss=False)
        attr_A2174 = '["' + str('Socket_44' + '"]') 
        row_5AD7E.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_A2174, text='Geometry Proximity', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_geometry_proximity:
            row_7EB1F = col_D1B09.row(heading='', align=False)
            row_7EB1F.alert = False
            row_7EB1F.enabled = True
            row_7EB1F.active = True
            row_7EB1F.use_property_split = False
            row_7EB1F.use_property_decorate = False
            row_7EB1F.scale_x = 1.0
            row_7EB1F.scale_y = 1.0
            row_7EB1F.alignment = 'Expand'.upper()
            row_7EB1F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_7EB1F.label(text='', icon_value=string_to_icon('BLANK1'))
            col_F8767 = row_7EB1F.column(heading='', align=False)
            col_F8767.alert = False
            col_F8767.enabled = True
            col_F8767.active = True
            col_F8767.use_property_split = False
            col_F8767.use_property_decorate = False
            col_F8767.scale_x = 1.0
            col_F8767.scale_y = 1.0
            col_F8767.alignment = 'Expand'.upper()
            col_F8767.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_F8767.separator(factor=1.0)
            col_F8767.prop(bpy.context.scene, 'sna_proximity_type', text='Type:', icon_value=0, emboss=True)
            col_F8767.separator(factor=0.5)
            if (bpy.context.scene.sna_proximity_type == 'Single Object'):
                attr_03A9F = '["' + str('Socket_45' + '"]') 
                col_F8767.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_03A9F, text='Object', icon_value=0, emboss=True)
            else:
                col_F8767.prop_search(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], '["Socket_47"]', bpy.data, 'collections', text='Collection', icon='OUTLINER_COLLECTION')
            col_F8767.separator(factor=1.0)
            col_F8767.label(text='Distance', icon_value=string_to_icon('DRIVER_DISTANCE'))
            attr_DB21B = '["' + str('Socket_177' + '"]') 
            col_F8767.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_DB21B, text='', icon_value=0, emboss=True)
            col_F8767.separator(factor=1.0)
            col_F8767.label(text='Falloff', icon_value=string_to_icon('SHARPCURVE'))
            attr_1A21E = '["' + str('Socket_175' + '"]') 
            col_F8767.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_1A21E, text='Smooth Transition', icon_value=0, emboss=True)
            if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_175']:
                row_EA66F = col_F8767.row(heading='', align=False)
                row_EA66F.alert = False
                row_EA66F.enabled = True
                row_EA66F.active = True
                row_EA66F.use_property_split = False
                row_EA66F.use_property_decorate = False
                row_EA66F.scale_x = 1.0
                row_EA66F.scale_y = 1.0
                row_EA66F.alignment = 'Expand'.upper()
                row_EA66F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_EA66F.label(text='', icon_value=string_to_icon('BLANK1'))
                col_BC157 = row_EA66F.column(heading='', align=False)
                col_BC157.alert = False
                col_BC157.enabled = True
                col_BC157.active = True
                col_BC157.use_property_split = False
                col_BC157.use_property_decorate = False
                col_BC157.scale_x = 1.0
                col_BC157.scale_y = 1.0
                col_BC157.alignment = 'Expand'.upper()
                col_BC157.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_BC157.separator(factor=0.25)
                attr_8431D = '["' + str('Socket_49' + '"]') 
                col_BC157.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_8431D, text='Transition', icon_value=0, emboss=True)
            col_F8767.separator(factor=1.0)
            attr_BAD2F = '["' + str('Socket_50' + '"]') 
            col_F8767.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_BAD2F, text='Behaviour', icon_value=0, emboss=True)
        col_76D50 = col_2271A.column(heading='', align=False)
        col_76D50.alert = False
        col_76D50.enabled = True
        col_76D50.active = True
        col_76D50.use_property_split = False
        col_76D50.use_property_decorate = False
        col_76D50.scale_x = 1.0
        col_76D50.scale_y = 1.0
        col_76D50.alignment = 'Expand'.upper()
        col_76D50.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_76D50.separator(factor=1.0)
        row_D6885 = col_76D50.row(heading='', align=True)
        row_D6885.alert = False
        row_D6885.enabled = True
        row_D6885.active = True
        row_D6885.use_property_split = False
        row_D6885.use_property_decorate = False
        row_D6885.scale_x = 1.0
        row_D6885.scale_y = 1.0
        row_D6885.alignment = 'Expand'.upper()
        row_D6885.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_D6885.prop(bpy.context.scene, 'sna_display_curve_proximity', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_curve_proximity else string_to_icon('RIGHTARROW')), emboss=False)
        attr_E007D = '["' + str('Socket_53' + '"]') 
        row_D6885.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_E007D, text='Curve Proximity', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_curve_proximity:
            row_917BD = col_76D50.row(heading='', align=False)
            row_917BD.alert = False
            row_917BD.enabled = True
            row_917BD.active = True
            row_917BD.use_property_split = False
            row_917BD.use_property_decorate = False
            row_917BD.scale_x = 1.0
            row_917BD.scale_y = 1.0
            row_917BD.alignment = 'Expand'.upper()
            row_917BD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_917BD.label(text='', icon_value=string_to_icon('BLANK1'))
            col_30362 = row_917BD.column(heading='', align=False)
            col_30362.alert = False
            col_30362.enabled = True
            col_30362.active = True
            col_30362.use_property_split = False
            col_30362.use_property_decorate = False
            col_30362.scale_x = 1.0
            col_30362.scale_y = 1.0
            col_30362.alignment = 'Expand'.upper()
            col_30362.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_30362.separator(factor=1.0)
            col_30362.prop(bpy.context.scene, 'sna_curve_proximity_type', text='Type', icon_value=0, emboss=True)
            col_30362.separator(factor=0.5)
            if (bpy.context.scene.sna_curve_proximity_type == 'Single Curve'):
                attr_A933A = '["' + str('Socket_59' + '"]') 
                col_30362.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_A933A, text='Curve', icon_value=0, emboss=True)
            else:
                col_30362.prop_search(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], '["Socket_60"]', bpy.data, 'collections', text='Collection', icon='OUTLINER_COLLECTION')
            col_30362.separator(factor=1.0)
            col_30362.label(text='Distance', icon_value=string_to_icon('DRIVER_DISTANCE'))
            attr_0081D = '["' + str('Socket_56' + '"]') 
            col_30362.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_0081D, text='', icon_value=0, emboss=True)
            col_30362.separator(factor=1.0)
            col_30362.label(text='Falloff', icon_value=string_to_icon('SHARPCURVE'))
            attr_0873E = '["' + str('Socket_176' + '"]') 
            col_30362.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_0873E, text='Smooth Transition', icon_value=0, emboss=True)
            if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_176']:
                row_6FB39 = col_30362.row(heading='', align=False)
                row_6FB39.alert = False
                row_6FB39.enabled = True
                row_6FB39.active = True
                row_6FB39.use_property_split = False
                row_6FB39.use_property_decorate = False
                row_6FB39.scale_x = 1.0
                row_6FB39.scale_y = 1.0
                row_6FB39.alignment = 'Expand'.upper()
                row_6FB39.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_6FB39.label(text='', icon_value=string_to_icon('BLANK1'))
                col_448D5 = row_6FB39.column(heading='', align=False)
                col_448D5.alert = False
                col_448D5.enabled = True
                col_448D5.active = True
                col_448D5.use_property_split = False
                col_448D5.use_property_decorate = False
                col_448D5.scale_x = 1.0
                col_448D5.scale_y = 1.0
                col_448D5.alignment = 'Expand'.upper()
                col_448D5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_448D5.separator(factor=0.25)
                attr_FF7F0 = '["' + str('Socket_58' + '"]') 
                col_448D5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_FF7F0, text='Transition', icon_value=0, emboss=True)
            col_30362.separator(factor=1.0)
            attr_1C762 = '["' + str('Socket_55' + '"]') 
            col_30362.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_1C762, text='Infinite Z', icon_value=0, emboss=True)
            attr_A0131 = '["' + str('Socket_138' + '"]') 
            col_30362.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_A0131, text='Behaviour', icon_value=0, emboss=True)


class SNA_PT_QUICK_SCATTER_0448D(bpy.types.Panel):
    bl_label = 'Quick Scatter'
    bl_idname = 'SNA_PT_QUICK_SCATTER_0448D'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'OpenScatter'
    bl_order = 1
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        if (bpy.context.scene.sna_emitter_object == None):
            layout.label(text='No Emitter Object Selected', icon_value=707)
        else:
            box_46D30 = layout.box()
            box_46D30.alert = False
            box_46D30.enabled = True
            box_46D30.active = True
            box_46D30.use_property_split = False
            box_46D30.use_property_decorate = False
            box_46D30.alignment = 'Expand'.upper()
            box_46D30.scale_x = 1.0
            box_46D30.scale_y = 1.2999999523162842
            if not True: box_46D30.operator_context = "EXEC_DEFAULT"
            row_B1406 = box_46D30.row(heading='', align=False)
            row_B1406.alert = False
            row_B1406.enabled = True
            row_B1406.active = True
            row_B1406.use_property_split = False
            row_B1406.use_property_decorate = False
            row_B1406.scale_x = 1.0
            row_B1406.scale_y = 1.0
            row_B1406.alignment = 'Left'.upper()
            row_B1406.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_B1406.prop(bpy.context.scene, 'sna_display_viewport_scatter', text='Viewport Scatter', icon_value=(string_to_icon('TRIA_DOWN') if bpy.context.scene.sna_display_viewport_scatter else string_to_icon('TRIA_RIGHT')), emboss=False)
            if bpy.context.scene.sna_display_viewport_scatter:
                box_6AF33 = box_46D30.box()
                box_6AF33.alert = False
                box_6AF33.enabled = True
                box_6AF33.active = True
                box_6AF33.use_property_split = False
                box_6AF33.use_property_decorate = False
                box_6AF33.alignment = 'Expand'.upper()
                box_6AF33.scale_x = 1.0
                box_6AF33.scale_y = 1.0
                if not True: box_6AF33.operator_context = "EXEC_DEFAULT"
                col_B3C02 = box_6AF33.column(heading='', align=True)
                col_B3C02.alert = False
                col_B3C02.enabled = True
                col_B3C02.active = True
                col_B3C02.use_property_split = False
                col_B3C02.use_property_decorate = False
                col_B3C02.scale_x = 1.0
                col_B3C02.scale_y = 1.0
                col_B3C02.alignment = 'Expand'.upper()
                col_B3C02.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_B3C02.prop(bpy.context.scene, 'sna_pattern', text='Pattern', icon_value=0, emboss=True)
                col_B3C02.separator(factor=1.0)
                col_B3C02.prop(bpy.context.scene, 'sna_presysdensity', text='Density', icon_value=0, emboss=True)
                col_B3C02.separator(factor=1.0)
                op = col_B3C02.operator('sna.scatter_viewport_objects_74948', text='Scatter Selected Objects', icon_value=string_to_icon('OBJECT_HIDDEN'), emboss=True, depress=False)


class SNA_OT_Scatter_Viewport_Objects_74948(bpy.types.Operator):
    bl_idname = "sna.scatter_viewport_objects_74948"
    bl_label = "Scatter Viewport Objects"
    bl_description = "Scatter the selected objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        collection_name_0_602b9, objects_selected_1_602b9 = sna_move_to_instance_collection_func_C7D29()
        if objects_selected_1_602b9:
            bpy.ops.sna.add_scatter_system_fbb77('INVOKE_DEFAULT', )
            bpy.data.collections[collection_name_0_602b9].hide_viewport = True
            bpy.context.view_layer.objects.active.sna_instance_type = 'Multiple Instances'
            bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_31'] = bpy.data.collections[collection_name_0_602b9]
            if (bpy.context.scene.sna_pattern == 'Clumps'):
                bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_62'] = True
                bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_63'] = 0.45399999618530273
                bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_64'] = 0.5080000162124634
            else:
                if (bpy.context.scene.sna_pattern == 'Lines'):
                    bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_75'] = True
            bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_8'] = bpy.context.scene.sna_presysdensity
            bpy.context.view_layer.objects.active.modifiers['GN_SCS_MOD']['Socket_13'] = True
        else:
            bpy.ops.wm.call_panel(name="SNA_PT_WARNING_E25FE", keep_open=False)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_move_to_instance_collection_func_C7D29():
    collection_name = None
    objects_selected = None
    # Function to create a unique collection name

    def get_unique_collection_name(base_name):
        counter = 1
        new_name = base_name
        while new_name in bpy.data.collections:
            new_name = f"{base_name}.{counter:03}"
            counter += 1
        return new_name
    # Get the selected objects
    selected_objects = bpy.context.selected_objects
    # Create a boolean output variable
    objects_selected = len(selected_objects) > 0
    # If objects are selected, proceed with duplicating and moving them to a new collection
    if objects_selected:
        # Base collection name
        base_collection_name = "OpenScatter Instances"
        # Get unique collection name and store it in a variable
        new_collection_name = get_unique_collection_name(base_collection_name)
        # Create a new collection with the unique name
        new_collection = bpy.data.collections.new(new_collection_name)
        bpy.context.scene.collection.children.link(new_collection)
        # Duplicate the selected objects and move them to the new collection
        for obj in selected_objects:
            # Duplicate the object
            obj_copy = obj.copy()
            obj_copy.data = obj.data.copy()  # Make sure the data is also duplicated
            # Link the duplicate to the new collection
            new_collection.objects.link(obj_copy)
        # The final collection name is stored in this variable
        collection_name = new_collection_name
    else:
        # No objects selected, objects_selected remains False
        collection_name = None
    return [collection_name, objects_selected]


def sna_pattern_enum_items(self, context):
    enum_items = [['Normal', 'Normal', '', 250], ['Clumps', 'Clumps', '', 255], ['Lines', 'Lines', '', 382]]
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


class SNA_PT_WARNING_E25FE(bpy.types.Panel):
    bl_label = 'Warning!'
    bl_idname = 'SNA_PT_WARNING_E25FE'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = ''
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col_1C219 = layout.column(heading='', align=False)
        col_1C219.alert = True
        col_1C219.enabled = True
        col_1C219.active = True
        col_1C219.use_property_split = False
        col_1C219.use_property_decorate = False
        col_1C219.scale_x = 1.0
        col_1C219.scale_y = 1.0
        col_1C219.alignment = 'Expand'.upper()
        col_1C219.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_1C219.label(text='No objects selected!', icon_value=707)


def sna_func_rotation_7C8F2(layout_function, ):
    box_AE892 = layout_function.box()
    box_AE892.alert = False
    box_AE892.enabled = True
    box_AE892.active = True
    box_AE892.use_property_split = False
    box_AE892.use_property_decorate = False
    box_AE892.alignment = 'Expand'.upper()
    box_AE892.scale_x = 1.0
    box_AE892.scale_y = 1.0
    if not True: box_AE892.operator_context = "EXEC_DEFAULT"
    col_CAA8F = box_AE892.column(heading='', align=False)
    col_CAA8F.alert = False
    col_CAA8F.enabled = True
    col_CAA8F.active = True
    col_CAA8F.use_property_split = False
    col_CAA8F.use_property_decorate = False
    col_CAA8F.scale_x = 1.0
    col_CAA8F.scale_y = 1.0
    col_CAA8F.alignment = 'Expand'.upper()
    col_CAA8F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_77445 = col_CAA8F.row(heading='', align=False)
    row_77445.alert = False
    row_77445.enabled = True
    row_77445.active = True
    row_77445.use_property_split = False
    row_77445.use_property_decorate = False
    row_77445.scale_x = 1.0
    row_77445.scale_y = 1.0
    row_77445.alignment = 'Left'.upper()
    row_77445.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_77445.prop(bpy.context.scene, 'sna_display_rotation', text='Rotation', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_rotation else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_display_rotation:
        col_D440C = col_CAA8F.column(heading='', align=False)
        col_D440C.alert = False
        col_D440C.enabled = True
        col_D440C.active = True
        col_D440C.use_property_split = False
        col_D440C.use_property_decorate = False
        col_D440C.scale_x = 1.0
        col_D440C.scale_y = 1.0
        col_D440C.alignment = 'Expand'.upper()
        col_D440C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_4648F = col_D440C.column(heading='', align=False)
        col_4648F.alert = False
        col_4648F.enabled = True
        col_4648F.active = True
        col_4648F.use_property_split = False
        col_4648F.use_property_decorate = False
        col_4648F.scale_x = 1.0
        col_4648F.scale_y = 1.0
        col_4648F.alignment = 'Expand'.upper()
        col_4648F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_4648F.separator(factor=1.0)
        row_13222 = col_4648F.row(heading='', align=True)
        row_13222.alert = False
        row_13222.enabled = True
        row_13222.active = True
        row_13222.use_property_split = False
        row_13222.use_property_decorate = False
        row_13222.scale_x = 1.0
        row_13222.scale_y = 1.0
        row_13222.alignment = 'Expand'.upper()
        row_13222.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_13222.prop(bpy.context.scene, 'sna_display_rotate', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_rotate else string_to_icon('RIGHTARROW')), emboss=False)
        attr_15DF5 = '["' + str('Socket_137' + '"]') 
        row_13222.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_15DF5, text='Rotate', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_rotate:
            row_16A81 = col_4648F.row(heading='', align=False)
            row_16A81.alert = False
            row_16A81.enabled = True
            row_16A81.active = True
            row_16A81.use_property_split = False
            row_16A81.use_property_decorate = False
            row_16A81.scale_x = 1.0
            row_16A81.scale_y = 1.0
            row_16A81.alignment = 'Expand'.upper()
            row_16A81.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_16A81.label(text='', icon_value=string_to_icon('BLANK1'))
            col_50FBE = row_16A81.column(heading='', align=False)
            col_50FBE.alert = False
            col_50FBE.enabled = True
            col_50FBE.active = True
            col_50FBE.use_property_split = False
            col_50FBE.use_property_decorate = False
            col_50FBE.scale_x = 1.0
            col_50FBE.scale_y = 1.0
            col_50FBE.alignment = 'Expand'.upper()
            col_50FBE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_50FBE.label(text='Amount:', icon_value=0)
            attr_CE970 = '["' + str('Socket_23' + '"]') 
            col_50FBE.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_CE970, text='', icon_value=0, emboss=True)
        col_E6A8C = col_4648F.column(heading='', align=False)
        col_E6A8C.alert = False
        col_E6A8C.enabled = True
        col_E6A8C.active = True
        col_E6A8C.use_property_split = False
        col_E6A8C.use_property_decorate = False
        col_E6A8C.scale_x = 1.0
        col_E6A8C.scale_y = 1.0
        col_E6A8C.alignment = 'Expand'.upper()
        col_E6A8C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_E6A8C.separator(factor=1.0)
        row_1CF9E = col_E6A8C.row(heading='', align=True)
        row_1CF9E.alert = False
        row_1CF9E.enabled = True
        row_1CF9E.active = True
        row_1CF9E.use_property_split = False
        row_1CF9E.use_property_decorate = False
        row_1CF9E.scale_x = 1.0
        row_1CF9E.scale_y = 1.0
        row_1CF9E.alignment = 'Expand'.upper()
        row_1CF9E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_1CF9E.prop(bpy.context.scene, 'sna_display_align_to_surface', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_align_to_surface else string_to_icon('RIGHTARROW')), emboss=False)
        attr_CEB04 = '["' + str('Socket_21' + '"]') 
        row_1CF9E.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_CEB04, text='Align to Surface', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_align_to_surface:
            row_C0F56 = col_E6A8C.row(heading='', align=False)
            row_C0F56.alert = False
            row_C0F56.enabled = True
            row_C0F56.active = True
            row_C0F56.use_property_split = False
            row_C0F56.use_property_decorate = False
            row_C0F56.scale_x = 1.0
            row_C0F56.scale_y = 1.0
            row_C0F56.alignment = 'Expand'.upper()
            row_C0F56.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_C0F56.label(text='', icon_value=string_to_icon('BLANK1'))
            col_A0C1F = row_C0F56.column(heading='', align=False)
            col_A0C1F.alert = False
            col_A0C1F.enabled = True
            col_A0C1F.active = True
            col_A0C1F.use_property_split = False
            col_A0C1F.use_property_decorate = False
            col_A0C1F.scale_x = 1.0
            col_A0C1F.scale_y = 1.0
            col_A0C1F.alignment = 'Expand'.upper()
            col_A0C1F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_A0C1F.separator(factor=1.0)
            col_A0C1F.label(text='Alignment Strength', icon_value=0)
            attr_0C186 = '["' + str('Socket_118' + '"]') 
            col_A0C1F.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_0C186, text='', icon_value=0, emboss=True, toggle=True)
        col_9C405 = col_E6A8C.column(heading='', align=False)
        col_9C405.alert = False
        col_9C405.enabled = True
        col_9C405.active = True
        col_9C405.use_property_split = False
        col_9C405.use_property_decorate = False
        col_9C405.scale_x = 1.0
        col_9C405.scale_y = 1.0
        col_9C405.alignment = 'Expand'.upper()
        col_9C405.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_9C405.separator(factor=1.0)
        row_B9B32 = col_9C405.row(heading='', align=True)
        row_B9B32.alert = False
        row_B9B32.enabled = True
        row_B9B32.active = True
        row_B9B32.use_property_split = False
        row_B9B32.use_property_decorate = False
        row_B9B32.scale_x = 1.0
        row_B9B32.scale_y = 1.0
        row_B9B32.alignment = 'Expand'.upper()
        row_B9B32.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_B9B32.prop(bpy.context.scene, 'sna_display_random_rotation', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_random_rotation else string_to_icon('RIGHTARROW')), emboss=False)
        attr_CC655 = '["' + str('Socket_25' + '"]') 
        row_B9B32.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_CC655, text='Random Rotation', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_random_rotation:
            row_3867D = col_9C405.row(heading='', align=False)
            row_3867D.alert = False
            row_3867D.enabled = True
            row_3867D.active = True
            row_3867D.use_property_split = False
            row_3867D.use_property_decorate = False
            row_3867D.scale_x = 1.0
            row_3867D.scale_y = 1.0
            row_3867D.alignment = 'Expand'.upper()
            row_3867D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_3867D.label(text='', icon_value=string_to_icon('BLANK1'))
            col_ACFDD = row_3867D.column(heading='', align=False)
            col_ACFDD.alert = False
            col_ACFDD.enabled = True
            col_ACFDD.active = True
            col_ACFDD.use_property_split = False
            col_ACFDD.use_property_decorate = False
            col_ACFDD.scale_x = 1.0
            col_ACFDD.scale_y = 1.0
            col_ACFDD.alignment = 'Expand'.upper()
            col_ACFDD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_9C0BA = '["' + str('Socket_26' + '"]') 
            col_ACFDD.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_9C0BA, text='Amount', icon_value=0, emboss=True)
            col_ACFDD.separator(factor=1.0)
            attr_C007C = '["' + str('Socket_27' + '"]') 
            col_ACFDD.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_C007C, text='Seed', icon_value=0, emboss=True)
            col_ACFDD.separator(factor=1.0)
            attr_6F1CA = '["' + str('Socket_155' + '"]') 
            col_ACFDD.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_6F1CA, text='Snap', icon_value=0, emboss=True)
            if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_155']:
                row_D2645 = col_ACFDD.row(heading='', align=False)
                row_D2645.alert = False
                row_D2645.enabled = True
                row_D2645.active = True
                row_D2645.use_property_split = False
                row_D2645.use_property_decorate = False
                row_D2645.scale_x = 1.0
                row_D2645.scale_y = 1.0
                row_D2645.alignment = 'Expand'.upper()
                row_D2645.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_D2645.label(text='', icon_value=string_to_icon('BLANK1'))
                col_D2895 = row_D2645.column(heading='', align=False)
                col_D2895.alert = False
                col_D2895.enabled = True
                col_D2895.active = True
                col_D2895.use_property_split = False
                col_D2895.use_property_decorate = False
                col_D2895.scale_x = 1.0
                col_D2895.scale_y = 1.0
                col_D2895.alignment = 'Expand'.upper()
                col_D2895.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_D2895.separator(factor=0.25)
                attr_40ED5 = '["' + str('Socket_156' + '"]') 
                col_D2895.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_40ED5, text='Max Angle', icon_value=0, emboss=True)


def sna_func_scale_A798D(layout_function, ):
    box_83DD3 = layout_function.box()
    box_83DD3.alert = False
    box_83DD3.enabled = True
    box_83DD3.active = True
    box_83DD3.use_property_split = False
    box_83DD3.use_property_decorate = False
    box_83DD3.alignment = 'Expand'.upper()
    box_83DD3.scale_x = 1.0
    box_83DD3.scale_y = 1.0
    if not True: box_83DD3.operator_context = "EXEC_DEFAULT"
    col_FC37A = box_83DD3.column(heading='', align=False)
    col_FC37A.alert = False
    col_FC37A.enabled = True
    col_FC37A.active = True
    col_FC37A.use_property_split = False
    col_FC37A.use_property_decorate = False
    col_FC37A.scale_x = 1.0
    col_FC37A.scale_y = 1.0
    col_FC37A.alignment = 'Expand'.upper()
    col_FC37A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_78ACF = col_FC37A.row(heading='', align=False)
    row_78ACF.alert = False
    row_78ACF.enabled = True
    row_78ACF.active = True
    row_78ACF.use_property_split = False
    row_78ACF.use_property_decorate = False
    row_78ACF.scale_x = 1.0
    row_78ACF.scale_y = 1.0
    row_78ACF.alignment = 'Left'.upper()
    row_78ACF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_78ACF.prop(bpy.context.scene, 'sna_display_scale', text='Scale', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_scale else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_display_scale:
        col_52FC4 = col_FC37A.column(heading='', align=False)
        col_52FC4.alert = False
        col_52FC4.enabled = True
        col_52FC4.active = True
        col_52FC4.use_property_split = False
        col_52FC4.use_property_decorate = False
        col_52FC4.scale_x = 1.0
        col_52FC4.scale_y = 1.0
        col_52FC4.alignment = 'Expand'.upper()
        col_52FC4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_52FC4.separator(factor=1.0)
        row_826D3 = col_52FC4.row(heading='', align=True)
        row_826D3.alert = False
        row_826D3.enabled = True
        row_826D3.active = True
        row_826D3.use_property_split = False
        row_826D3.use_property_decorate = False
        row_826D3.scale_x = 1.0
        row_826D3.scale_y = 1.0
        row_826D3.alignment = 'Expand'.upper()
        row_826D3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_826D3.prop(bpy.context.scene, 'sna_display_uniform_scale', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_uniform_scale else string_to_icon('RIGHTARROW')), emboss=False)
        attr_335DD = '["' + str('Socket_135' + '"]') 
        row_826D3.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_335DD, text='Uniform Scale', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_uniform_scale:
            row_9AFDD = col_52FC4.row(heading='', align=False)
            row_9AFDD.alert = False
            row_9AFDD.enabled = True
            row_9AFDD.active = True
            row_9AFDD.use_property_split = False
            row_9AFDD.use_property_decorate = False
            row_9AFDD.scale_x = 1.0
            row_9AFDD.scale_y = 1.0
            row_9AFDD.alignment = 'Expand'.upper()
            row_9AFDD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_9AFDD.label(text='', icon_value=string_to_icon('BLANK1'))
            col_D2DAD = row_9AFDD.column(heading='', align=False)
            col_D2DAD.alert = False
            col_D2DAD.enabled = True
            col_D2DAD.active = True
            col_D2DAD.use_property_split = False
            col_D2DAD.use_property_decorate = False
            col_D2DAD.scale_x = 1.0
            col_D2DAD.scale_y = 1.0
            col_D2DAD.alignment = 'Expand'.upper()
            col_D2DAD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_D2DAD.separator(factor=1.0)
            col_D2DAD.label(text='Uniform Scale:', icon_value=string_to_icon('DRIVER_TRANSFORM'))
            attr_1C93C = '["' + str('Socket_11' + '"]') 
            col_D2DAD.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_1C93C, text='', icon_value=0, emboss=True)
        col_717A3 = col_52FC4.column(heading='', align=False)
        col_717A3.alert = False
        col_717A3.enabled = True
        col_717A3.active = True
        col_717A3.use_property_split = False
        col_717A3.use_property_decorate = False
        col_717A3.scale_x = 1.0
        col_717A3.scale_y = 1.0
        col_717A3.alignment = 'Expand'.upper()
        col_717A3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_717A3.separator(factor=1.0)
        row_69D9E = col_717A3.row(heading='', align=True)
        row_69D9E.alert = False
        row_69D9E.enabled = True
        row_69D9E.active = True
        row_69D9E.use_property_split = False
        row_69D9E.use_property_decorate = False
        row_69D9E.scale_x = 1.0
        row_69D9E.scale_y = 1.0
        row_69D9E.alignment = 'Expand'.upper()
        row_69D9E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_69D9E.prop(bpy.context.scene, 'sna_display_nonuniform_scale', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_nonuniform_scale else string_to_icon('RIGHTARROW')), emboss=False)
        attr_0E4FC = '["' + str('Socket_136' + '"]') 
        row_69D9E.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_0E4FC, text='Non-Uniform Scale', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_nonuniform_scale:
            row_581A2 = col_717A3.row(heading='', align=False)
            row_581A2.alert = False
            row_581A2.enabled = True
            row_581A2.active = True
            row_581A2.use_property_split = False
            row_581A2.use_property_decorate = False
            row_581A2.scale_x = 1.0
            row_581A2.scale_y = 1.0
            row_581A2.alignment = 'Expand'.upper()
            row_581A2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_581A2.label(text='', icon_value=string_to_icon('BLANK1'))
            col_2BC93 = row_581A2.column(heading='', align=False)
            col_2BC93.alert = False
            col_2BC93.enabled = True
            col_2BC93.active = True
            col_2BC93.use_property_split = False
            col_2BC93.use_property_decorate = False
            col_2BC93.scale_x = 1.0
            col_2BC93.scale_y = 1.0
            col_2BC93.alignment = 'Expand'.upper()
            col_2BC93.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_2BC93.separator(factor=1.0)
            col_2BC93.label(text='Non-Uniform Scale:', icon_value=string_to_icon('CON_TRANSLIKE'))
            attr_9EAB5 = '["' + str('Socket_12' + '"]') 
            col_2BC93.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_9EAB5, text='', icon_value=0, emboss=True)
        col_B0749 = col_717A3.column(heading='', align=False)
        col_B0749.alert = False
        col_B0749.enabled = True
        col_B0749.active = True
        col_B0749.use_property_split = False
        col_B0749.use_property_decorate = False
        col_B0749.scale_x = 1.0
        col_B0749.scale_y = 1.0
        col_B0749.alignment = 'Expand'.upper()
        col_B0749.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_B0749.separator(factor=1.0)
        row_CE0F3 = col_B0749.row(heading='', align=True)
        row_CE0F3.alert = False
        row_CE0F3.enabled = True
        row_CE0F3.active = True
        row_CE0F3.use_property_split = False
        row_CE0F3.use_property_decorate = False
        row_CE0F3.scale_x = 1.0
        row_CE0F3.scale_y = 1.0
        row_CE0F3.alignment = 'Expand'.upper()
        row_CE0F3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_CE0F3.prop(bpy.context.scene, 'sna_display_random_scale', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_random_scale else string_to_icon('RIGHTARROW')), emboss=False)
        attr_2505F = '["' + str('Socket_13' + '"]') 
        row_CE0F3.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_2505F, text='Random Scale', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_random_scale:
            row_61C83 = col_B0749.row(heading='', align=False)
            row_61C83.alert = False
            row_61C83.enabled = True
            row_61C83.active = True
            row_61C83.use_property_split = False
            row_61C83.use_property_decorate = False
            row_61C83.scale_x = 1.0
            row_61C83.scale_y = 1.0
            row_61C83.alignment = 'Expand'.upper()
            row_61C83.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_61C83.label(text='', icon_value=string_to_icon('BLANK1'))
            col_96B9D = row_61C83.column(heading='', align=False)
            col_96B9D.alert = False
            col_96B9D.enabled = True
            col_96B9D.active = True
            col_96B9D.use_property_split = False
            col_96B9D.use_property_decorate = False
            col_96B9D.scale_x = 1.0
            col_96B9D.scale_y = 1.0
            col_96B9D.alignment = 'Expand'.upper()
            col_96B9D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_96B9D.separator(factor=1.0)
            col_D3578 = col_96B9D.column(heading='', align=True)
            col_D3578.alert = False
            col_D3578.enabled = True
            col_D3578.active = True
            col_D3578.use_property_split = False
            col_D3578.use_property_decorate = False
            col_D3578.scale_x = 1.0
            col_D3578.scale_y = 1.0
            col_D3578.alignment = 'Expand'.upper()
            col_D3578.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_62979 = '["' + str('Socket_15' + '"]') 
            col_D3578.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_62979, text='Min', icon_value=95, emboss=True, toggle=True)
            attr_E0424 = '["' + str('Socket_16' + '"]') 
            col_D3578.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_E0424, text='Max', icon_value=95, emboss=True, toggle=True)
            col_D3578.separator(factor=1.0)
            attr_5B15E = '["' + str('Socket_19' + '"]') 
            col_D3578.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_5B15E, text='Seed', icon_value=0, emboss=True, toggle=True)


def sna_func_scattering_80211(layout_function, ):
    box_E381B = layout_function.box()
    box_E381B.alert = False
    box_E381B.enabled = True
    box_E381B.active = True
    box_E381B.use_property_split = False
    box_E381B.use_property_decorate = False
    box_E381B.alignment = 'Expand'.upper()
    box_E381B.scale_x = 1.0
    box_E381B.scale_y = 1.0
    if not True: box_E381B.operator_context = "EXEC_DEFAULT"
    col_93FC8 = box_E381B.column(heading='', align=False)
    col_93FC8.alert = False
    col_93FC8.enabled = True
    col_93FC8.active = True
    col_93FC8.use_property_split = False
    col_93FC8.use_property_decorate = False
    col_93FC8.scale_x = 1.0
    col_93FC8.scale_y = 1.0
    col_93FC8.alignment = 'Expand'.upper()
    col_93FC8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_07607 = col_93FC8.row(heading='', align=False)
    row_07607.alert = False
    row_07607.enabled = True
    row_07607.active = True
    row_07607.use_property_split = False
    row_07607.use_property_decorate = False
    row_07607.scale_x = 1.0
    row_07607.scale_y = 1.0
    row_07607.alignment = 'Left'.upper()
    row_07607.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_07607.prop(bpy.context.scene, 'sna_displayscattering', text='Scattering', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_displayscattering else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_displayscattering:
        col_65DCB = col_93FC8.column(heading='', align=False)
        col_65DCB.alert = False
        col_65DCB.enabled = True
        col_65DCB.active = True
        col_65DCB.use_property_split = False
        col_65DCB.use_property_decorate = False
        col_65DCB.scale_x = 1.0
        col_65DCB.scale_y = 1.0
        col_65DCB.alignment = 'Expand'.upper()
        col_65DCB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_65DCB.separator(factor=1.0)
        col_EEDB6 = col_65DCB.column(heading='', align=True)
        col_EEDB6.alert = False
        col_EEDB6.enabled = True
        col_EEDB6.active = True
        col_EEDB6.use_property_split = False
        col_EEDB6.use_property_decorate = False
        col_EEDB6.scale_x = 1.0
        col_EEDB6.scale_y = 1.0
        col_EEDB6.alignment = 'Expand'.upper()
        col_EEDB6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_E2454 = col_EEDB6.row(heading='', align=True)
        row_E2454.alert = False
        row_E2454.enabled = True
        row_E2454.active = True
        row_E2454.use_property_split = False
        row_E2454.use_property_decorate = False
        row_E2454.scale_x = 1.0
        row_E2454.scale_y = 1.0
        row_E2454.alignment = 'Expand'.upper()
        row_E2454.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_F5469 = '["' + str('Socket_8' + '"]') 
        row_E2454.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_F5469, text='Density / m²', icon_value=0, emboss=True)
        row_EDFBD = col_EEDB6.row(heading='', align=True)
        row_EDFBD.alert = False
        row_EDFBD.enabled = True
        row_EDFBD.active = True
        row_EDFBD.use_property_split = False
        row_EDFBD.use_property_decorate = False
        row_EDFBD.scale_x = 1.0
        row_EDFBD.scale_y = 1.0
        row_EDFBD.alignment = 'Expand'.upper()
        row_EDFBD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        attr_87D33 = '["' + str('Socket_9' + '"]') 
        row_EDFBD.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_87D33, text='Seed', icon_value=0, emboss=True)
        op = row_EDFBD.operator('sna.randomize_seed_73e32', text='', icon_value=_icons['1439410433.png'].icon_id, emboss=True, depress=False)
        col_65DCB.separator(factor=1.0)
        col_BD544 = col_65DCB.column(heading='', align=True)
        col_BD544.alert = False
        col_BD544.enabled = True
        col_BD544.active = True
        col_BD544.use_property_split = False
        col_BD544.use_property_decorate = False
        col_BD544.scale_x = 1.0
        col_BD544.scale_y = 1.0
        col_BD544.alignment = 'Expand'.upper()
        col_BD544.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_BD544.prop(bpy.context.scene, 'sna_mathfactor', text='Factor', icon_value=0, emboss=True)
        row_63049 = col_BD544.row(heading='', align=True)
        row_63049.alert = False
        row_63049.enabled = True
        row_63049.active = True
        row_63049.use_property_split = False
        row_63049.use_property_decorate = False
        row_63049.scale_x = 1.0
        row_63049.scale_y = 1.0
        row_63049.alignment = 'Expand'.upper()
        row_63049.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = row_63049.operator('sna.density_cfa8a', text='*', icon_value=0, emboss=True, depress=False)
        op = row_63049.operator('sna.density_59664', text='/', icon_value=0, emboss=True, depress=False)
        op = row_63049.operator('sna.density_fa923', text='+', icon_value=0, emboss=True, depress=False)
        op = row_63049.operator('sna.density_7c2d8', text='-', icon_value=0, emboss=True, depress=False)
        col_65DCB.separator(factor=1.0899999141693115)
        attr_829F3 = '["' + str('Socket_140' + '"]') 
        col_65DCB.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_829F3, text='Limit Self-Collision', icon_value=0, emboss=True)
        if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_140']:
            row_AE6D1 = col_65DCB.row(heading='', align=False)
            row_AE6D1.alert = False
            row_AE6D1.enabled = True
            row_AE6D1.active = True
            row_AE6D1.use_property_split = False
            row_AE6D1.use_property_decorate = False
            row_AE6D1.scale_x = 1.0
            row_AE6D1.scale_y = 1.0
            row_AE6D1.alignment = 'Expand'.upper()
            row_AE6D1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_AE6D1.label(text='', icon_value=string_to_icon('BLANK1'))
            col_2533E = row_AE6D1.column(heading='', align=False)
            col_2533E.alert = False
            col_2533E.enabled = True
            col_2533E.active = True
            col_2533E.use_property_split = False
            col_2533E.use_property_decorate = False
            col_2533E.scale_x = 1.0
            col_2533E.scale_y = 1.0
            col_2533E.alignment = 'Expand'.upper()
            col_2533E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_0410F = '["' + str('Socket_43' + '"]') 
            col_2533E.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_0410F, text='Minimum Distance', icon_value=0, emboss=True)


class SNA_OT_Density_Cfa8A(bpy.types.Operator):
    bl_idname = "sna.density_cfa8a"
    bl_label = "Density*"
    bl_description = "Multiply by the factor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_8'] = float(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_8'] * bpy.context.scene.sna_mathfactor)
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Density_59664(bpy.types.Operator):
    bl_idname = "sna.density_59664"
    bl_label = "Density/"
    bl_description = "Divide by the factor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_8'] = float(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_8'] / bpy.context.scene.sna_mathfactor)
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Density_Fa923(bpy.types.Operator):
    bl_idname = "sna.density_fa923"
    bl_label = "Density+"
    bl_description = "Add the factor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_8'] = float(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_8'] + bpy.context.scene.sna_mathfactor)
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Density_7C2D8(bpy.types.Operator):
    bl_idname = "sna.density_7c2d8"
    bl_label = "Density-"
    bl_description = "Subtract the factor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_8'] = float(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_8'] - bpy.context.scene.sna_mathfactor)
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Randomize_Seed_73E32(bpy.types.Operator):
    bl_idname = "sna.randomize_seed_73e32"
    bl_label = "Randomize Seed"
    bl_description = "Randomizes the seed of the active scatter system"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_9'] = random_integer(-100000000.0, 100000000.0, None)
        bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Refresh_View_E4454(bpy.types.Operator):
    bl_idname = "sna.refresh_view_e4454"
    bl_label = "Refresh View"
    bl_description = "Updates the visibility of scatter systems to match the correct scene"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_refresh_view_func_8ABC3()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_refresh_view_func_8ABC3():
    for i_17EDF in range(len(bpy.data.collections['Scatter Systems'].all_objects)):
        if (property_exists("bpy.context.scene.sna_scattersystemcollection", globals(), locals()) and bpy.data.collections['Scatter Systems'].all_objects[i_17EDF].name in bpy.context.scene.sna_scattersystemcollection):
            bpy.data.objects[bpy.data.collections['Scatter Systems'].all_objects[i_17EDF].name].hide_viewport = False
            bpy.data.objects[bpy.data.collections['Scatter Systems'].all_objects[i_17EDF].name].hide_render = False
        else:
            bpy.data.objects[bpy.data.collections['Scatter Systems'].all_objects[i_17EDF].name].hide_viewport = True
            bpy.data.objects[bpy.data.collections['Scatter Systems'].all_objects[i_17EDF].name].hide_render = True
        for i_E7F1D in range(len(bpy.data.collections['OSGN_ProxyObjectsCollection'].all_objects)):
            bpy.data.collections['OSGN_ProxyObjectsCollection'].all_objects[i_E7F1D].hide_viewport = False
            bpy.data.collections['OSGN_ProxyObjectsCollection'].all_objects[i_E7F1D].hide_render = False


@persistent
def frame_change_pre_handler_D854F(dummy):
    if bpy.context.preferences.addons[__package__].preferences.sna_auto_scene_switch_detection:
        if bpy.context.screen.is_animation_playing:
            pass
        else:
            sna_refresh_view_func_8ABC3()


def sna_func_surfacesample_80F42(layout_function, ):
    box_503C7 = layout_function.box()
    box_503C7.alert = False
    box_503C7.enabled = True
    box_503C7.active = True
    box_503C7.use_property_split = False
    box_503C7.use_property_decorate = False
    box_503C7.alignment = 'Expand'.upper()
    box_503C7.scale_x = 1.0
    box_503C7.scale_y = 1.0
    if not True: box_503C7.operator_context = "EXEC_DEFAULT"
    col_CAFBC = box_503C7.column(heading='', align=False)
    col_CAFBC.alert = False
    col_CAFBC.enabled = True
    col_CAFBC.active = True
    col_CAFBC.use_property_split = False
    col_CAFBC.use_property_decorate = False
    col_CAFBC.scale_x = 1.0
    col_CAFBC.scale_y = 1.0
    col_CAFBC.alignment = 'Expand'.upper()
    col_CAFBC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_AFDCB = col_CAFBC.row(heading='', align=False)
    row_AFDCB.alert = False
    row_AFDCB.enabled = True
    row_AFDCB.active = True
    row_AFDCB.use_property_split = False
    row_AFDCB.use_property_decorate = False
    row_AFDCB.scale_x = 1.0
    row_AFDCB.scale_y = 1.0
    row_AFDCB.alignment = 'Left'.upper()
    row_AFDCB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_AFDCB.prop(bpy.context.scene, 'sna_displaysurfacesample', text='Surface', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_displaysurfacesample else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_displaysurfacesample:
        col_A4518 = col_CAFBC.column(heading='', align=False)
        col_A4518.alert = False
        col_A4518.enabled = True
        col_A4518.active = True
        col_A4518.use_property_split = False
        col_A4518.use_property_decorate = False
        col_A4518.scale_x = 1.0
        col_A4518.scale_y = 1.0
        col_A4518.alignment = 'Expand'.upper()
        col_A4518.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_A4518.separator(factor=1.0)
        col_A4518.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name], 'sna_surface_type', text='Type', icon_value=0, emboss=True)
        if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_179']:
            pass
        else:
            col_A4518.separator(factor=1.0)
            col_6B411 = col_A4518.column(heading='', align=False)
            col_6B411.alert = False
            col_6B411.enabled = False
            col_6B411.active = False
            col_6B411.use_property_split = False
            col_6B411.use_property_decorate = False
            col_6B411.scale_x = 1.0
            col_6B411.scale_y = 1.0
            col_6B411.alignment = 'Expand'.upper()
            col_6B411.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            attr_9356E = '["' + str('Socket_178' + '"]') 
            col_6B411.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_9356E, text='', icon_value=0, emboss=True)
        if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_179']:
            col_A4518.separator(factor=1.0)
            if bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD']['Socket_109']:
                col_A4518.prop_search(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], '["Socket_110"]', bpy.context.scene.collection, 'children', text='', icon='OUTLINER_COLLECTION')
            else:
                attr_6ECCD = '["' + str('Socket_108' + '"]') 
                col_A4518.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_6ECCD, text='', icon_value=0, emboss=True)


def sna_func_texturemasks_641D8(layout_function, ):
    box_BBEA1 = layout_function.box()
    box_BBEA1.alert = False
    box_BBEA1.enabled = True
    box_BBEA1.active = True
    box_BBEA1.use_property_split = False
    box_BBEA1.use_property_decorate = False
    box_BBEA1.alignment = 'Expand'.upper()
    box_BBEA1.scale_x = 1.0
    box_BBEA1.scale_y = 1.0
    if not True: box_BBEA1.operator_context = "EXEC_DEFAULT"
    col_69AE7 = box_BBEA1.column(heading='', align=False)
    col_69AE7.alert = False
    col_69AE7.enabled = True
    col_69AE7.active = True
    col_69AE7.use_property_split = False
    col_69AE7.use_property_decorate = False
    col_69AE7.scale_x = 1.0
    col_69AE7.scale_y = 1.0
    col_69AE7.alignment = 'Expand'.upper()
    col_69AE7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_F7039 = col_69AE7.row(heading='', align=False)
    row_F7039.alert = False
    row_F7039.enabled = True
    row_F7039.active = True
    row_F7039.use_property_split = False
    row_F7039.use_property_decorate = False
    row_F7039.scale_x = 1.0
    row_F7039.scale_y = 1.0
    row_F7039.alignment = 'Left'.upper()
    row_F7039.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_F7039.prop(bpy.context.scene, 'sna_display_texturemasks', text='Texture Masks', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_texturemasks else string_to_icon('RIGHTARROW')), emboss=False)
    if bpy.context.scene.sna_display_texturemasks:
        col_644B3 = col_69AE7.column(heading='', align=False)
        col_644B3.alert = False
        col_644B3.enabled = True
        col_644B3.active = True
        col_644B3.use_property_split = False
        col_644B3.use_property_decorate = False
        col_644B3.scale_x = 1.0
        col_644B3.scale_y = 1.0
        col_644B3.alignment = 'Expand'.upper()
        col_644B3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_E845C = col_644B3.column(heading='', align=False)
        col_E845C.alert = False
        col_E845C.enabled = True
        col_E845C.active = True
        col_E845C.use_property_split = False
        col_E845C.use_property_decorate = False
        col_E845C.scale_x = 1.0
        col_E845C.scale_y = 1.0
        col_E845C.alignment = 'Expand'.upper()
        col_E845C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_E845C.separator(factor=1.0)
        row_5867D = col_E845C.row(heading='', align=True)
        row_5867D.alert = False
        row_5867D.enabled = True
        row_5867D.active = True
        row_5867D.use_property_split = False
        row_5867D.use_property_decorate = False
        row_5867D.scale_x = 1.0
        row_5867D.scale_y = 1.0
        row_5867D.alignment = 'Expand'.upper()
        row_5867D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_5867D.prop(bpy.context.scene, 'sna_display_noise', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_noise else string_to_icon('RIGHTARROW')), emboss=False)
        attr_08AC7 = '["' + str('Socket_62' + '"]') 
        row_5867D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_08AC7, text='Noise', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_noise:
            row_8F445 = col_E845C.row(heading='', align=False)
            row_8F445.alert = False
            row_8F445.enabled = True
            row_8F445.active = True
            row_8F445.use_property_split = False
            row_8F445.use_property_decorate = False
            row_8F445.scale_x = 1.0
            row_8F445.scale_y = 1.0
            row_8F445.alignment = 'Expand'.upper()
            row_8F445.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_8F445.label(text='', icon_value=string_to_icon('BLANK1'))
            col_756A5 = row_8F445.column(heading='', align=False)
            col_756A5.alert = False
            col_756A5.enabled = True
            col_756A5.active = True
            col_756A5.use_property_split = False
            col_756A5.use_property_decorate = False
            col_756A5.scale_x = 1.0
            col_756A5.scale_y = 1.0
            col_756A5.alignment = 'Expand'.upper()
            col_756A5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_756A5.separator(factor=1.0)
            col_756A5.label(text='Falloff:', icon_value=string_to_icon('SHARPCURVE'))
            attr_8395E = '["' + str('Socket_63' + '"]') 
            col_756A5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_8395E, text='Min', icon_value=0, emboss=True)
            attr_D6D8C = '["' + str('Socket_64' + '"]') 
            col_756A5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_D6D8C, text='Max', icon_value=0, emboss=True)
            col_756A5.separator(factor=1.0)
            col_756A5.label(text='Texture Settings:', icon_value=string_to_icon('TEXTURE'))
            attr_687D0 = '["' + str('Socket_65' + '"]') 
            col_756A5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_687D0, text='Seed', icon_value=0, emboss=True)
            attr_2F115 = '["' + str('Socket_66' + '"]') 
            col_756A5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_2F115, text='Scale', icon_value=0, emboss=True)
            attr_E220A = '["' + str('Socket_67' + '"]') 
            col_756A5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_E220A, text='Detail', icon_value=0, emboss=True)
            attr_6A861 = '["' + str('Socket_68' + '"]') 
            col_756A5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_6A861, text='Roughness', icon_value=0, emboss=True)
            attr_187D5 = '["' + str('Socket_69' + '"]') 
            col_756A5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_187D5, text='Lacunarity', icon_value=0, emboss=True)
            attr_E668B = '["' + str('Socket_70' + '"]') 
            col_756A5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_E668B, text='Distortion', icon_value=0, emboss=True)
            col_756A5.separator(factor=1.0)
            col_756A5.label(text='Transform:', icon_value=string_to_icon('EMPTY_ARROWS'))
            attr_680A0 = '["' + str('Socket_71' + '"]') 
            col_756A5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_680A0, text='Location', icon_value=0, emboss=True)
            attr_445B7 = '["' + str('Socket_72' + '"]') 
            col_756A5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_445B7, text='Rotation', icon_value=0, emboss=True)
            attr_66CF6 = '["' + str('Socket_73' + '"]') 
            col_756A5.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_66CF6, text='Scale', icon_value=0, emboss=True)
        col_B00EE = col_644B3.column(heading='', align=False)
        col_B00EE.alert = False
        col_B00EE.enabled = True
        col_B00EE.active = True
        col_B00EE.use_property_split = False
        col_B00EE.use_property_decorate = False
        col_B00EE.scale_x = 1.0
        col_B00EE.scale_y = 1.0
        col_B00EE.alignment = 'Expand'.upper()
        col_B00EE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_B00EE.separator(factor=1.0)
        row_FD534 = col_B00EE.row(heading='', align=True)
        row_FD534.alert = False
        row_FD534.enabled = True
        row_FD534.active = True
        row_FD534.use_property_split = False
        row_FD534.use_property_decorate = False
        row_FD534.scale_x = 1.0
        row_FD534.scale_y = 1.0
        row_FD534.alignment = 'Expand'.upper()
        row_FD534.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_FD534.prop(bpy.context.scene, 'sna_display_lines', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_lines else string_to_icon('RIGHTARROW')), emboss=False)
        attr_C7145 = '["' + str('Socket_75' + '"]') 
        row_FD534.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_C7145, text='Lines', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_lines:
            row_6F958 = col_B00EE.row(heading='', align=False)
            row_6F958.alert = False
            row_6F958.enabled = True
            row_6F958.active = True
            row_6F958.use_property_split = False
            row_6F958.use_property_decorate = False
            row_6F958.scale_x = 1.0
            row_6F958.scale_y = 1.0
            row_6F958.alignment = 'Expand'.upper()
            row_6F958.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_6F958.label(text='', icon_value=string_to_icon('BLANK1'))
            col_B2BB6 = row_6F958.column(heading='', align=False)
            col_B2BB6.alert = False
            col_B2BB6.enabled = True
            col_B2BB6.active = True
            col_B2BB6.use_property_split = False
            col_B2BB6.use_property_decorate = False
            col_B2BB6.scale_x = 1.0
            col_B2BB6.scale_y = 1.0
            col_B2BB6.alignment = 'Expand'.upper()
            col_B2BB6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_B2BB6.separator(factor=1.0)
            col_B2BB6.label(text='Falloff:', icon_value=string_to_icon('SHARPCURVE'))
            attr_CB1D8 = '["' + str('Socket_76' + '"]') 
            col_B2BB6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_CB1D8, text='Min', icon_value=0, emboss=True)
            attr_E5171 = '["' + str('Socket_77' + '"]') 
            col_B2BB6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_E5171, text='Max', icon_value=0, emboss=True)
            col_B2BB6.separator(factor=1.0)
            col_B2BB6.label(text='Texture Settings', icon_value=string_to_icon('TEXTURE'))
            attr_1E061 = '["' + str('Socket_78' + '"]') 
            col_B2BB6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_1E061, text='Scale', icon_value=0, emboss=True)
            attr_8D636 = '["' + str('Socket_79' + '"]') 
            col_B2BB6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_8D636, text='Distortion', icon_value=0, emboss=True)
            attr_889F5 = '["' + str('Socket_80' + '"]') 
            col_B2BB6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_889F5, text='Detail', icon_value=0, emboss=True)
            attr_A1AB4 = '["' + str('Socket_81' + '"]') 
            col_B2BB6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_A1AB4, text='Detail Scale', icon_value=0, emboss=True)
            attr_C548E = '["' + str('Socket_82' + '"]') 
            col_B2BB6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_C548E, text='Detail Roughness', icon_value=0, emboss=True)
            attr_7CE2C = '["' + str('Socket_83' + '"]') 
            col_B2BB6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_7CE2C, text='Phase Offset', icon_value=0, emboss=True)
            col_B2BB6.separator(factor=1.0)
            col_B2BB6.label(text='Transform:', icon_value=string_to_icon('EMPTY_ARROWS'))
            attr_7E1F0 = '["' + str('Socket_84' + '"]') 
            col_B2BB6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_7E1F0, text='Location', icon_value=0, emboss=True)
            attr_CAAE0 = '["' + str('Socket_85' + '"]') 
            col_B2BB6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_CAAE0, text='Rotation', icon_value=0, emboss=True)
            attr_F23BF = '["' + str('Socket_86' + '"]') 
            col_B2BB6.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_F23BF, text='Scale', icon_value=0, emboss=True)
        col_96826 = col_644B3.column(heading='', align=False)
        col_96826.alert = False
        col_96826.enabled = True
        col_96826.active = True
        col_96826.use_property_split = False
        col_96826.use_property_decorate = False
        col_96826.scale_x = 1.0
        col_96826.scale_y = 1.0
        col_96826.alignment = 'Expand'.upper()
        col_96826.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_96826.separator(factor=1.0)
        row_8B83D = col_96826.row(heading='', align=True)
        row_8B83D.alert = False
        row_8B83D.enabled = True
        row_8B83D.active = True
        row_8B83D.use_property_split = False
        row_8B83D.use_property_decorate = False
        row_8B83D.scale_x = 1.0
        row_8B83D.scale_y = 1.0
        row_8B83D.alignment = 'Expand'.upper()
        row_8B83D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_8B83D.prop(bpy.context.scene, 'sna_display_tiles', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_tiles else string_to_icon('RIGHTARROW')), emboss=False)
        attr_99823 = '["' + str('Socket_88' + '"]') 
        row_8B83D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_99823, text='Tiles', icon_value=0, emboss=True)
        if bpy.context.scene.sna_display_tiles:
            row_A970A = col_96826.row(heading='', align=False)
            row_A970A.alert = False
            row_A970A.enabled = True
            row_A970A.active = True
            row_A970A.use_property_split = False
            row_A970A.use_property_decorate = False
            row_A970A.scale_x = 1.0
            row_A970A.scale_y = 1.0
            row_A970A.alignment = 'Expand'.upper()
            row_A970A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_A970A.label(text='', icon_value=string_to_icon('BLANK1'))
            col_3499D = row_A970A.column(heading='', align=False)
            col_3499D.alert = False
            col_3499D.enabled = True
            col_3499D.active = True
            col_3499D.use_property_split = False
            col_3499D.use_property_decorate = False
            col_3499D.scale_x = 1.0
            col_3499D.scale_y = 1.0
            col_3499D.alignment = 'Expand'.upper()
            col_3499D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_3499D.separator(factor=1.0)
            col_3499D.label(text='Texture Settings', icon_value=string_to_icon('TEXTURE'))
            attr_D370E = '["' + str('Socket_91' + '"]') 
            col_3499D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_D370E, text='Scale', icon_value=0, emboss=True)
            attr_B4ABF = '["' + str('Socket_92' + '"]') 
            col_3499D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_B4ABF, text='Gap Size', icon_value=0, emboss=True)
            attr_B4AF2 = '["' + str('Socket_94' + '"]') 
            col_3499D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_B4AF2, text='Width', icon_value=0, emboss=True)
            attr_A2EEA = '["' + str('Socket_95' + '"]') 
            col_3499D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_A2EEA, text='Height', icon_value=0, emboss=True)
            col_3499D.separator(factor=1.0)
            col_3499D.label(text='Transform:', icon_value=string_to_icon('EMPTY_ARROWS'))
            attr_4A7B5 = '["' + str('Socket_96' + '"]') 
            col_3499D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_4A7B5, text='Location', icon_value=0, emboss=True)
            attr_C9D3D = '["' + str('Socket_97' + '"]') 
            col_3499D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_C9D3D, text='Rotation', icon_value=0, emboss=True)
            attr_ADE8F = '["' + str('Socket_98' + '"]') 
            col_3499D.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_ADE8F, text='Scale', icon_value=0, emboss=True)
        layout_function = col_644B3
        sna_func_texturemasks2_E0304(layout_function, )


def sna_func_texturemasks2_E0304(layout_function, ):
    col_7F523 = layout_function.column(heading='', align=False)
    col_7F523.alert = False
    col_7F523.enabled = True
    col_7F523.active = True
    col_7F523.use_property_split = False
    col_7F523.use_property_decorate = False
    col_7F523.scale_x = 1.0
    col_7F523.scale_y = 1.0
    col_7F523.alignment = 'Expand'.upper()
    col_7F523.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_7F523.separator(factor=1.0)
    row_93C28 = col_7F523.row(heading='', align=True)
    row_93C28.alert = False
    row_93C28.enabled = True
    row_93C28.active = True
    row_93C28.use_property_split = False
    row_93C28.use_property_decorate = False
    row_93C28.scale_x = 1.0
    row_93C28.scale_y = 1.0
    row_93C28.alignment = 'Expand'.upper()
    row_93C28.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_93C28.prop(bpy.context.scene, 'sna_display_image', text='', icon_value=(string_to_icon('DOWNARROW_HLT') if bpy.context.scene.sna_display_image else string_to_icon('RIGHTARROW')), emboss=False)
    attr_D8C78 = '["' + str('Socket_190' + '"]') 
    row_93C28.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_D8C78, text='Image', icon_value=0, emboss=True)
    if bpy.context.scene.sna_display_image:
        row_88AA1 = col_7F523.row(heading='', align=False)
        row_88AA1.alert = False
        row_88AA1.enabled = True
        row_88AA1.active = True
        row_88AA1.use_property_split = False
        row_88AA1.use_property_decorate = False
        row_88AA1.scale_x = 1.0
        row_88AA1.scale_y = 1.0
        row_88AA1.alignment = 'Expand'.upper()
        row_88AA1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_88AA1.label(text='', icon_value=string_to_icon('BLANK1'))
        col_EB814 = row_88AA1.column(heading='', align=False)
        col_EB814.alert = False
        col_EB814.enabled = True
        col_EB814.active = True
        col_EB814.use_property_split = False
        col_EB814.use_property_decorate = False
        col_EB814.scale_x = 1.0
        col_EB814.scale_y = 1.0
        col_EB814.alignment = 'Expand'.upper()
        col_EB814.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_EB814.separator(factor=1.0)
        col_EB814.prop(bpy.context.scene, 'sna_image_mask', text='Image', icon_value=0, emboss=True)
        col_EB814.separator(factor=1.0)
        attr_EEC69 = '["' + str('Socket_182' + '"]') 
        col_EB814.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_EEC69, text='Bounds', icon_value=0, emboss=True)
        col_EB814.separator(factor=1.0)
        attr_875B3 = '["' + str('Socket_183' + '"]') 
        col_EB814.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_875B3, text='Min', icon_value=0, emboss=True)
        attr_7B9A3 = '["' + str('Socket_184' + '"]') 
        col_EB814.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_7B9A3, text='Max', icon_value=0, emboss=True)
        attr_F8EEE = '["' + str('Socket_185' + '"]') 
        col_EB814.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_F8EEE, text='Invert', icon_value=0, emboss=True)
        attr_42A64 = '["' + str('Socket_186' + '"]') 
        col_EB814.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_42A64, text='Sharpen', icon_value=0, emboss=True)
        attr_9B163 = '["' + str('Socket_187' + '"]') 
        col_EB814.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_9B163, text='Location', icon_value=0, emboss=True)
        attr_3F2B7 = '["' + str('Socket_188' + '"]') 
        col_EB814.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_3F2B7, text='Rotation', icon_value=0, emboss=True)
        attr_ABD84 = '["' + str('Socket_189' + '"]') 
        col_EB814.prop(bpy.data.objects[bpy.context.scene.sna_scattersystemcollection[bpy.context.scene.sna_active_index].name].modifiers['GN_SCS_MOD'], attr_ABD84, text='Scale', icon_value=0, emboss=True)


def sna_get_latest_release_func_BC0A1(current_version):
    current_version = current_version
    version_comparison = None
    import json
    # URL of the latest release of OpenScatter addon from GitHub
    release_url = "https://api.github.com/repos/GitMay3D/OpenScatter/releases/latest"

    def get_latest_release_version(url):
        """Fetches the latest release version from GitHub API."""
        response = requests.get(url)
        if response.status_code == 200:
            release_info = json.loads(response.text)
            latest_version = release_info.get("tag_name", None)
            return latest_version
        else:
            return None

    def parse_version_string(version_str):
        """Extracts and converts the version part from a string like 'v1.0.3_4.2+' to a tuple (1, 0, 3)."""
        # Use regex to find the major.minor.patch part (e.g., '1.0.3')
        match = re.search(r'(\d+)\.(\d+)\.(\d+)', version_str)
        if match:
            # Convert the matched version numbers to a tuple of integers
            return tuple(map(int, match.groups()))
        return None

    def compare_versions(current_version_tuple):
        """Compares the current version (as a tuple) with the latest GitHub release."""
        latest_version_str = get_latest_release_version(release_url)
        if not latest_version_str:
            return None  # Return None if unable to get the latest version
        latest_version_tuple = parse_version_string(latest_version_str)
        if not latest_version_tuple:
            return None  # Return None if unable to parse the latest version
        # Compare versions
        if current_version_tuple < latest_version_tuple:
            return "lower"  # Current version is lower than the latest release
        elif current_version_tuple == latest_version_tuple:
            return "same"  # Current version is the same as the latest release
        else:
            return "higher"  # Current version is newer than the latest release
    # Example input: the current version of the addon as a tuple (e.g., (1, 0, 3))
    current_version = current_version  # You can change this value as needed
    # Call the function and get the comparison result
    version_comparison = compare_versions(current_version)
    # Output the result based on the comparison
    if version_comparison is None:
        print("Could not determine the version.")
    elif version_comparison == "lower":
        print("Your version is older than the latest release.")
    elif version_comparison == "same":
        print("You are using the latest version.")
    elif version_comparison == "higher":
        print("You are using a newer version than the latest release!")
    return version_comparison


class SNA_OT_Update_8D639(bpy.types.Operator):
    bl_idname = "sna.update_8d639"
    bl_label = "Update"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        version_comparison_0_05fa3 = sna_get_latest_release_func_BC0A1((1, 0, 5))
        if (version_comparison_0_05fa3 == 'higher'):
            bpy.ops.wm.call_panel(name="SNA_PT_USING_NEWER_VERSION_3AB30", keep_open=False)
        else:
            if (version_comparison_0_05fa3 == 'lower'):
                bpy.ops.wm.call_panel(name="SNA_PT_NEW_VERSION_AVAILABLE_88765", keep_open=False)
            else:
                bpy.ops.wm.call_panel(name="SNA_PT_NO_NEW_VERSION_AVAILABLE_C64EB", keep_open=False)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_NEW_VERSION_AVAILABLE_88765(bpy.types.Panel):
    bl_label = 'New Version Available'
    bl_idname = 'SNA_PT_NEW_VERSION_AVAILABLE_88765'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = ''
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.label(text='New version available!', icon_value=43)
        op = layout.operator('wm.url_open', text='Download', icon_value=100, emboss=True, depress=False)
        op.url = 'https://github.com/GitMay3D/OpenScatter/releases/latest'


class SNA_PT_NO_NEW_VERSION_AVAILABLE_C64EB(bpy.types.Panel):
    bl_label = 'No New Version Available'
    bl_idname = 'SNA_PT_NO_NEW_VERSION_AVAILABLE_C64EB'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = ''
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.label(text='Already using latest version', icon_value=51)


class SNA_PT_USING_NEWER_VERSION_3AB30(bpy.types.Panel):
    bl_label = 'Using Newer Version'
    bl_idname = 'SNA_PT_USING_NEWER_VERSION_3AB30'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = ''
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.label(text='Using pre-release version', icon_value=0)


class SNA_GROUP_sna_scattersystemgroupprops(bpy.types.PropertyGroup):
    label: bpy.props.StringProperty(name='Label', description='', default='', subtype='NONE', maxlen=0, update=sna_update_label_9ED9A)
    name: bpy.props.StringProperty(name='Name', description='', default='', subtype='NONE', maxlen=0)
    colorlabel: bpy.props.FloatVectorProperty(name='ColorLabel', description='', size=3, default=(0.0, 0.0, 0.0), subtype='COLOR', unit='NONE', min=0.0, max=1.0, step=3, precision=6)
    groupname: bpy.props.StringProperty(name='GroupName', description='', default='', subtype='NONE', maxlen=0)
    scene: bpy.props.PointerProperty(name='Scene', description='', type=bpy.types.Scene)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_GROUP_sna_scattersystemgroupprops)
    bpy.types.Scene.sna_scattersystemcollection = bpy.props.CollectionProperty(name='ScatterSystemCollection', description='', type=SNA_GROUP_sna_scattersystemgroupprops)
    bpy.types.Object.sna_systemgroups = bpy.props.BoolProperty(name='SystemGroups', description='', default=False)
    bpy.types.Scene.sna_active_index = bpy.props.IntProperty(name='Active Index', description='', default=0, subtype='NONE')
    bpy.types.Scene.sna_active_scatter_system = bpy.props.StringProperty(name='Active Scatter System', description='', default='', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_displaysurfacesample = bpy.props.BoolProperty(name='DisplaySurfaceSample', description='', default=False)
    bpy.types.Object.sna_surface_type = bpy.props.EnumProperty(name='Surface Type', description='', items=[('Emitter Object', 'Emitter Object', '', 0, 0), ('Single Surface', 'Single Surface', '', 0, 1), ('Multiple Surfaces', 'Multiple Surfaces', '', 0, 2)], update=sna_update_sna_surface_type_C9A72)
    bpy.types.Scene.sna_displayscattering = bpy.props.BoolProperty(name='DisplayScattering', description='', default=False)
    bpy.types.Scene.sna_density_type = bpy.props.EnumProperty(name='Density Type', description='', items=[('/m²', '/m²', '', 0, 1), ('Count', 'Count', '', 0, 2)], options={'ENUM_FLAG'})
    bpy.types.Scene.sna_displayinstances = bpy.props.BoolProperty(name='DisplayInstances', description='', default=False)
    bpy.types.Object.sna_instance_type = bpy.props.EnumProperty(name='Instance Type', description='', items=[('Single Instance', 'Single Instance', '', 0, 0), ('Multiple Instances', 'Multiple Instances', '', 0, 1)], update=sna_update_sna_instance_type_01FB7)
    bpy.types.Scene.sna_display_scale = bpy.props.BoolProperty(name='Display Scale', description='', default=False)
    bpy.types.Scene.sna_display_rotation = bpy.props.BoolProperty(name='Display Rotation', description='', default=False)
    bpy.types.Scene.sna_display_abiotic = bpy.props.BoolProperty(name='Display Abiotic', description='', default=False)
    bpy.types.Scene.sna_display_proximity = bpy.props.BoolProperty(name='Display Proximity', description='', default=False)
    bpy.types.Scene.sna_display_culling = bpy.props.BoolProperty(name='Display Culling', description='', default=False)
    bpy.types.Scene.sna_display_texturemasks = bpy.props.BoolProperty(name='Display TextureMasks', description='', default=False)
    bpy.types.Scene.sna_display_optimization = bpy.props.BoolProperty(name='Display Optimization', description='', default=False)
    bpy.types.Scene.sna_display_uniform_scale = bpy.props.BoolProperty(name='Display Uniform Scale', description='', default=False)
    bpy.types.Scene.sna_display_nonuniform_scale = bpy.props.BoolProperty(name='Display Non-Uniform Scale', description='', default=False)
    bpy.types.Scene.sna_display_random_scale = bpy.props.BoolProperty(name='Display Random Scale', description='', default=False)
    bpy.types.Scene.sna_display_rotate = bpy.props.BoolProperty(name='Display Rotate', description='', default=False)
    bpy.types.Scene.sna_display_align_to_surface = bpy.props.BoolProperty(name='Display Align to Surface', description='', default=False)
    bpy.types.Scene.sna_display_random_rotation = bpy.props.BoolProperty(name='Display Random Rotation', description='', default=False)
    bpy.types.Scene.sna_display_vertex_group = bpy.props.BoolProperty(name='Display Vertex Group', description='', default=False)
    bpy.types.Scene.sna_display_slope_mask = bpy.props.BoolProperty(name='Display Slope Mask', description='', default=False)
    bpy.types.Scene.sna_display_elevation_mask = bpy.props.BoolProperty(name='Display Elevation Mask', description='', default=False)
    bpy.types.Scene.sna_display_angle_mask = bpy.props.BoolProperty(name='Display Angle Mask', description='', default=False)
    bpy.types.Scene.sna_display_geometry_proximity = bpy.props.BoolProperty(name='Display Geometry Proximity', description='', default=False)
    bpy.types.Scene.sna_proximity_type = bpy.props.EnumProperty(name='Proximity Type', description='', items=[('Single Object', 'Single Object', '', 0, 0), ('Multiple Objects', 'Multiple Objects', '', 0, 1)], update=sna_update_sna_proximity_type_69A01)
    bpy.types.Scene.sna_display_curve_proximity = bpy.props.BoolProperty(name='Display Curve Proximity', description='', default=False)
    bpy.types.Scene.sna_curve_proximity_type = bpy.props.EnumProperty(name='Curve Proximity Type', description='', items=[('Single Curve', 'Single Curve', '', 0, 0), ('Multiple Curves', 'Multiple Curves', '', 0, 1)], update=sna_update_sna_curve_proximity_type_54F1E)
    bpy.types.Scene.sna_display_noise = bpy.props.BoolProperty(name='Display Noise', description='', default=False)
    bpy.types.Scene.sna_display_lines = bpy.props.BoolProperty(name='Display Lines', description='', default=False)
    bpy.types.Scene.sna_display_tiles = bpy.props.BoolProperty(name='Display Tiles', description='', default=False)
    bpy.types.Scene.sna_display_image = bpy.props.BoolProperty(name='Display Image', description='', default=False)
    bpy.types.Scene.sna_image_mask = bpy.props.StringProperty(name='Image Mask', description='', default='', subtype='FILE_PATH', maxlen=0, update=sna_update_sna_image_mask_252C4)
    bpy.types.Scene.sna_display_decrease_viewport_density = bpy.props.BoolProperty(name='Display Decrease Viewport Density', description='', default=False)
    bpy.types.Scene.sna_display_use_optimized_mesh = bpy.props.BoolProperty(name='Display Use Optimized Mesh', description='', default=False)
    bpy.types.Scene.sna_display_enable_camera_culling = bpy.props.BoolProperty(name='Display Enable Camera Culling', description='', default=False)
    bpy.types.Scene.sna_display_dynamics = bpy.props.BoolProperty(name='Display Dynamics', description='', default=False)
    bpy.types.Scene.sna_display_wind = bpy.props.BoolProperty(name='Display Wind', description='', default=False)
    bpy.types.Scene.sna_display_collision = bpy.props.BoolProperty(name='Display Collision', description='', default=False)
    bpy.types.Scene.sna_display_ecosystem = bpy.props.BoolProperty(name='Display Ecosystem', description='', default=False)
    bpy.types.Scene.sna_display_attraction = bpy.props.BoolProperty(name='Display Attraction', description='', default=False)
    bpy.types.Scene.sna_display_repulsion = bpy.props.BoolProperty(name='Display Repulsion', description='', default=False)
    bpy.types.Scene.sna_display_system_list = bpy.props.BoolProperty(name='Display System List', description='', default=True)
    bpy.types.Scene.sna_emitter_object = bpy.props.PointerProperty(name='Emitter Object', description='', type=bpy.types.Object, update=sna_update_sna_emitter_object_7F6B0)
    bpy.types.Scene.sna_emitter_text = bpy.props.StringProperty(name='Emitter Text', description='', default='Choose an emitter using the tool above!', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_display_misc = bpy.props.BoolProperty(name='Display Misc', description='', default=False)
    bpy.types.Scene.sna_display_scene_context = bpy.props.BoolProperty(name='Display Scene Context', description='', default=False)
    bpy.types.Scene.sna_active_scene = bpy.props.PointerProperty(name='Active Scene', description='', type=bpy.types.Scene)
    bpy.types.Scene.sna_display_viewport_scatter = bpy.props.BoolProperty(name='Display Viewport Scatter', description='', default=False)
    bpy.types.Scene.sna_pattern = bpy.props.EnumProperty(name='Pattern', description='Select the pattern you want to use for the scattered objects', items=sna_pattern_enum_items)
    bpy.types.Scene.sna_presysdensity = bpy.props.FloatProperty(name='PreSysDensity', description='', default=10.0, subtype='NONE', unit='NONE', min=0.0, step=3, precision=3)
    bpy.types.Scene.sna_mathfactor = bpy.props.FloatProperty(name='MathFactor', description='', default=2.0, subtype='NONE', unit='NONE', step=3, precision=2)
    bpy.types.Scene.sna_display_preferences_settings = bpy.props.BoolProperty(name='Display Preferences Settings', description='', default=False)
    bpy.types.Scene.sna_display_auto_scene_switch_detection = bpy.props.BoolProperty(name='Display Auto Scene Switch Detection', description='', default=False)
    bpy.types.Scene.sna_display_default_values = bpy.props.BoolProperty(name='Display Default Values', description='', default=False)
    bpy.utils.register_class(SNA_PT_OPENSCATTER_82501)
    bpy.utils.register_class(SNA_UL_display_collection_list_29FCA)
    bpy.utils.register_class(SNA_OT_Add_Scatter_System_Fbb77)
    bpy.utils.register_class(SNA_OT_Delete_Scatter_Layer_537D5)
    bpy.utils.register_class(SNA_OT_Move_Up_Aeedb)
    bpy.utils.register_class(SNA_OT_Move_Down_Fc101)
    bpy.utils.register_class(SNA_PT_cant_create_scatter_systems_in_this_mode_C1531)
    bpy.utils.register_class(SNA_MT_09C83)
    bpy.utils.register_class(SNA_OT_Enter_Weight_Paint_Mode_Db6F9)
    bpy.utils.register_class(SNA_AddonPreferences_14B35)
    bpy.utils.register_class(SNA_OT_Documentation_7E9C9)
    bpy.utils.register_class(SNA_PT_QUICK_SCATTER_0448D)
    bpy.utils.register_class(SNA_OT_Scatter_Viewport_Objects_74948)
    bpy.utils.register_class(SNA_PT_WARNING_E25FE)
    if not '1439410433.png' in _icons: _icons.load('1439410433.png', os.path.join(os.path.dirname(__file__), 'icons', '1439410433.png'), "IMAGE")
    bpy.utils.register_class(SNA_OT_Density_Cfa8A)
    bpy.utils.register_class(SNA_OT_Density_59664)
    bpy.utils.register_class(SNA_OT_Density_Fa923)
    bpy.utils.register_class(SNA_OT_Density_7C2D8)
    bpy.utils.register_class(SNA_OT_Randomize_Seed_73E32)
    bpy.utils.register_class(SNA_OT_Refresh_View_E4454)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_D854F)
    bpy.utils.register_class(SNA_OT_Update_8D639)
    bpy.utils.register_class(SNA_PT_NEW_VERSION_AVAILABLE_88765)
    bpy.utils.register_class(SNA_PT_NO_NEW_VERSION_AVAILABLE_C64EB)
    bpy.utils.register_class(SNA_PT_USING_NEWER_VERSION_3AB30)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_display_default_values
    del bpy.types.Scene.sna_display_auto_scene_switch_detection
    del bpy.types.Scene.sna_display_preferences_settings
    del bpy.types.Scene.sna_mathfactor
    del bpy.types.Scene.sna_presysdensity
    del bpy.types.Scene.sna_pattern
    del bpy.types.Scene.sna_display_viewport_scatter
    del bpy.types.Scene.sna_active_scene
    del bpy.types.Scene.sna_display_scene_context
    del bpy.types.Scene.sna_display_misc
    del bpy.types.Scene.sna_emitter_text
    del bpy.types.Scene.sna_emitter_object
    del bpy.types.Scene.sna_display_system_list
    del bpy.types.Scene.sna_display_repulsion
    del bpy.types.Scene.sna_display_attraction
    del bpy.types.Scene.sna_display_ecosystem
    del bpy.types.Scene.sna_display_collision
    del bpy.types.Scene.sna_display_wind
    del bpy.types.Scene.sna_display_dynamics
    del bpy.types.Scene.sna_display_enable_camera_culling
    del bpy.types.Scene.sna_display_use_optimized_mesh
    del bpy.types.Scene.sna_display_decrease_viewport_density
    del bpy.types.Scene.sna_image_mask
    del bpy.types.Scene.sna_display_image
    del bpy.types.Scene.sna_display_tiles
    del bpy.types.Scene.sna_display_lines
    del bpy.types.Scene.sna_display_noise
    del bpy.types.Scene.sna_curve_proximity_type
    del bpy.types.Scene.sna_display_curve_proximity
    del bpy.types.Scene.sna_proximity_type
    del bpy.types.Scene.sna_display_geometry_proximity
    del bpy.types.Scene.sna_display_angle_mask
    del bpy.types.Scene.sna_display_elevation_mask
    del bpy.types.Scene.sna_display_slope_mask
    del bpy.types.Scene.sna_display_vertex_group
    del bpy.types.Scene.sna_display_random_rotation
    del bpy.types.Scene.sna_display_align_to_surface
    del bpy.types.Scene.sna_display_rotate
    del bpy.types.Scene.sna_display_random_scale
    del bpy.types.Scene.sna_display_nonuniform_scale
    del bpy.types.Scene.sna_display_uniform_scale
    del bpy.types.Scene.sna_display_optimization
    del bpy.types.Scene.sna_display_texturemasks
    del bpy.types.Scene.sna_display_culling
    del bpy.types.Scene.sna_display_proximity
    del bpy.types.Scene.sna_display_abiotic
    del bpy.types.Scene.sna_display_rotation
    del bpy.types.Scene.sna_display_scale
    del bpy.types.Object.sna_instance_type
    del bpy.types.Scene.sna_displayinstances
    del bpy.types.Scene.sna_density_type
    del bpy.types.Scene.sna_displayscattering
    del bpy.types.Object.sna_surface_type
    del bpy.types.Scene.sna_displaysurfacesample
    del bpy.types.Scene.sna_active_scatter_system
    del bpy.types.Scene.sna_active_index
    del bpy.types.Object.sna_systemgroups
    del bpy.types.Scene.sna_scattersystemcollection
    bpy.utils.unregister_class(SNA_GROUP_sna_scattersystemgroupprops)
    bpy.utils.unregister_class(SNA_PT_OPENSCATTER_82501)
    bpy.utils.unregister_class(SNA_UL_display_collection_list_29FCA)
    bpy.utils.unregister_class(SNA_OT_Add_Scatter_System_Fbb77)
    bpy.utils.unregister_class(SNA_OT_Delete_Scatter_Layer_537D5)
    bpy.utils.unregister_class(SNA_OT_Move_Up_Aeedb)
    bpy.utils.unregister_class(SNA_OT_Move_Down_Fc101)
    bpy.utils.unregister_class(SNA_PT_cant_create_scatter_systems_in_this_mode_C1531)
    bpy.utils.unregister_class(SNA_MT_09C83)
    bpy.utils.unregister_class(SNA_OT_Enter_Weight_Paint_Mode_Db6F9)
    bpy.utils.unregister_class(SNA_AddonPreferences_14B35)
    bpy.utils.unregister_class(SNA_OT_Documentation_7E9C9)
    bpy.utils.unregister_class(SNA_PT_QUICK_SCATTER_0448D)
    bpy.utils.unregister_class(SNA_OT_Scatter_Viewport_Objects_74948)
    bpy.utils.unregister_class(SNA_PT_WARNING_E25FE)
    bpy.utils.unregister_class(SNA_OT_Density_Cfa8A)
    bpy.utils.unregister_class(SNA_OT_Density_59664)
    bpy.utils.unregister_class(SNA_OT_Density_Fa923)
    bpy.utils.unregister_class(SNA_OT_Density_7C2D8)
    bpy.utils.unregister_class(SNA_OT_Randomize_Seed_73E32)
    bpy.utils.unregister_class(SNA_OT_Refresh_View_E4454)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_D854F)
    bpy.utils.unregister_class(SNA_OT_Update_8D639)
    bpy.utils.unregister_class(SNA_PT_NEW_VERSION_AVAILABLE_88765)
    bpy.utils.unregister_class(SNA_PT_NO_NEW_VERSION_AVAILABLE_C64EB)
    bpy.utils.unregister_class(SNA_PT_USING_NEWER_VERSION_3AB30)
