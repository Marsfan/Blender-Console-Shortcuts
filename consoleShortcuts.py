"""Clear the Blender system console."""

# Pylint disable commands

# pylint: disable=R0903,E0401, C0103, W0613, R0201

import os
import platform
import bpy

# Define the info about the addon

bl_info = {
    "name": "System Console Shortcuts",
    "description": "Adds buttons to toggle and clear the system console from"
                   " the info header",
    "author": "Gabriel R (marsfan)",
    "version": (1, 0),
    "blender": (2, 79),
    "location": "Info Header > Clear Console",
    "category": "System"
}


# Update the visible button by removing and readding
def update_buttons(self, context):
    """Update which buttons are visible."""
    bpy.types.INFO_HT_header.remove(draw_item_info)
    bpy.types.INFO_HT_header.append(draw_item_info)
    bpy.types.TEXT_HT_header.remove(draw_item_text_editor)
    bpy.types.TEXT_HT_header.append(draw_item_text_editor)


class addon_preferences(bpy.types.AddonPreferences):
    """Define Prefernces for this Addon."""

    # Set class idname to same as module
    bl_idname = __name__

    # Create a property to set the visibility of the console toggle button
    infoConsoleLaunch = bpy.props.BoolProperty(
        name="Console Button Enabled",
        description="Include button in the Info Bar to open the System Console?",  # noqa
        default=False,
        update=update_buttons
    )

    # Create a property to set teh visibility of the console clearing button
    infoConsoleClear = bpy.props.BoolProperty(
        name="Clear Button Enabled",
        description="Include button in the Info Bar to clear the system console?",  # noqa
        default=True,
        update=update_buttons
    )

    infoDebugToggle = bpy.props.BoolProperty()

    textEditorConsoleLaunch = bpy.props.BoolProperty(
        name="Console Button Enabled",
        description="Include a Button in the Text Editor Menu Bar to toggle System Console ?",  # noqa
        default=False,
        update=update_buttons
    )

    # Create a property to set teh visibility of the console clearing button
    textEditorConsoleClear = bpy.props.BoolProperty(
        name="Clear Button Enabled",
        description="Include button to clear the system console in the Text Editor Menu Bar?",  # noqa
        default=True,
        update=update_buttons
    )

    textEditorDebugToggle = bpy.props.BoolProperty()

    infoBox = bpy.props.BoolProperty(default=False)
    textEditorBox = bpy.props.BoolProperty(default=False)

    def draw(self, context):
        """Draw the preferences menu for the addon."""
        layout = self.layout
        # Create a columnt
        box = layout.box()
        row = box.row()
        row.alignment = 'LEFT'
        row.prop(
            self, "infoBox",
            icon="TRIA_DOWN" if self.infoBox else "TRIA_RIGHT",
            text="Info Bar Settings", emboss=False
            )
        if self.infoBox:
            row = box.row()
            row.label('Enable Button to clear system console?')
            row.prop(self, 'infoConsoleClear', text='')

            # New Row with second checkbox and label
            row = box.row()

            # Add checkbox and label
            row.label('Enable Button to toggle system Console?')
            row.prop(self, 'infoConsoleLaunch', text='')

            row = box.row()
            row.label('Enable Debug Mode toggle button?')
            row.prop(self, 'infoDebugToggle', text='')

        box = layout.box()
        row = box.row()
        row.alignment = 'LEFT'
        row.prop(
            self, "textEditorBox",
            icon="TRIA_DOWN" if self.textEditorBox else "TRIA_RIGHT",
            text="Text Editor Settings", emboss=False
            )
        if self.textEditorBox:
            row = box.row()
            row.label('Enable Button to clear system console?')
            row.prop(self, 'textEditorConsoleClear', text='')

            # New Row with second checkbox and label
            row = box.row()

            # Add checkbox and label
            row.label('Enable Button to toggle system Console?')
            row.prop(self, 'textEditorConsoleLaunch', text='')

            row = box.row()
            row.label('Enable debug mode toggle button?')
            row.prop(self, 'textEditorDebugToggle', text='')


# Console Clearing operator
class consoleClear(bpy.types.Operator):
    """Clear the console window across Operating Systems."""

    # set operator parameters
    bl_label = "Clear System Console"
    bl_idname = "console_shortcuts.clear_console"

    # Function to run when pressed
    def execute(self, context):
        """Clear Console Window across Operating Systems."""
        # Check what OS the user is running, and respond accordingly
        if platform.system() == 'Windows':
            os.system('cls')
            return {'FINISHED'}
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            os.system('clear')
            return {'FINISHED'}

        # Message the user if their OS is unsupported and return an error.
        self.report({'ERROR'}, "Operating System not supported. Please "
                    "contact the developer and tell him that your "
                    "platform string is '" + platform.system() + "'")
        return {'CANCELLED'}


class debugModeToggle(bpy.types.Operator):
    """Enable/Disable the debug mode in Blender."""

    bl_label = "Enable Blender Debug Mode"
    bl_idname = 'console_shortcuts.enable_debug'

    def execute(self, context):
        """Run on operator call."""
        bpy.app.debug = not bpy.app.debug
        return {'FINISHED'}


# Header drawing function
def draw_item_info(self, context):
    """Draw Operator."""
    prefs = bpy.context.user_preferences.addons[__name__].preferences
    layout = self.layout

    # Check the value of the preferences to decide what to display
    text = "Enable Debug Mode" if not bpy.app.debug else "Disable Debug Mode"
    if prefs.infoConsoleClear:
        layout.operator(consoleClear.bl_idname)
    if prefs.infoConsoleLaunch:
        layout.operator("wm.console_toggle")
    if prefs.infoDebugToggle:
        layout.operator(debugModeToggle.bl_idname, text=text)


def draw_item_text_editor(self, context):
    """Draw Operator."""
    prefs = bpy.context.user_preferences.addons[__name__].preferences
    layout = self.layout

    # Check the value of the preferences to decide what to display
    text = "Enable Debug Mode" if not bpy.app.debug else "Disable Debug Mode"
    if prefs.textEditorConsoleClear:
        layout.operator(consoleClear.bl_idname)
    if prefs.textEditorConsoleLaunch:
        layout.operator("wm.console_toggle")
    if prefs.textEditorDebugToggle:
        layout.operator(debugModeToggle.bl_idname, text=text)


# Register classes
def register():
    """Regiser classes for script."""
    # Register all classes in the module
    bpy.utils.register_module(__name__)
    # Add the buttons to the menu
    bpy.types.INFO_HT_header.append(draw_item_info)
    bpy.types.TEXT_HT_header.append(draw_item_text_editor)


# Unregister classes
def unregister():
    """Unregister classes upon script unload."""
    # Unregister all classes in the module
    bpy.utils.unregister_module(__name__)
    # REmove the buttons from the menu
    bpy.types.INFO_HT_header.remove(draw_item_info)
    bpy.types.INFO_HT_header.remove(draw_item_text_editor)
