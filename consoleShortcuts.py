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
    bpy.types.INFO_HT_header.remove(draw_item)
    bpy.types.INFO_HT_header.append(draw_item)


class addon_preferences(bpy.types.AddonPreferences):
    """Define Prefernces for this Addon."""

    # Set class idname to same as module
    bl_idname = __name__

    # Create a property to set the visibility of the console toggle button
    consoleLaunch = bpy.props.BoolProperty(
        name="Console Button Enabled",
        description="Include a Button To open the System Console?",
        default=False,
        update=update_buttons
    )

    # Create a property to set teh visibility of the console clearing button
    consoleClear = bpy.props.BoolProperty(
        name="Clear Button Enabled",
        description="Include A Button to clear the system console?",
        default=True,
        update=update_buttons
    )

    def draw(self, context):
        """Draw the preferences menu for the addon."""
        layout = self.layout
        # Create a columnt
        col = layout.column()

        # New row
        row = col.row()
        row.label('Enable Button to clear system console?')
        row.prop(self, 'consoleClear', text='')

        # New Row with second checkbox and label
        row = col.row()

        # Add checkbox and label
        row.label('Enable Button to toggle system Console?')
        row.prop(self, 'consoleLaunch', text='')


# Console Clearing operator
class consoleClear(bpy.types.Operator):
    """Clear the console window across Operating Systems."""

    # set operator parameters
    bl_label = "Clear System Console"
    bl_idname = "wm.clear_console"

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


# Header drawing function
def draw_item(self, context):
    """Draw Operator."""
    prefs = bpy.context.user_preferences.addons[__name__].preferences
    layout = self.layout

    # Check the value of the preferences to decide what to display
    if prefs.consoleClear:
        layout.operator(consoleClear.bl_idname)
    if prefs.consoleLaunch:
        layout.operator("wm.console_toggle")


# Register classes
def register():
    """Regiser classes for script."""
    # Register all classes in the module
    bpy.utils.register_module(__name__)
    # Add the buttons to the menu
    bpy.types.INFO_HT_header.append(draw_item)


# Unregister classes
def unregister():
    """Unregister classes upon script unload."""
    # Unregister all classes in the module
    bpy.utils.unregister_module(__name__)
    # REmove the buttons from the menu
    bpy.types.INFO_HT_header.remove(draw_item)
