import bpy
import ctypes

bl_info = {
    "name": "System Console Toggle",
    "author": "Meta Person; tintwotin",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "Text Editor > Text Menu > Show System Console",
    "description": "Toggle the visibility and topmost state of the system console window.",
    "category": "System",
}


def show_system_console(show):
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
    SW_HIDE = 0
    SW_SHOW = 5

    ctypes.windll.user32.ShowWindow(
        ctypes.windll.kernel32.GetConsoleWindow(), SW_SHOW if show else SW_HIDE
    )


def set_system_console_topmost(top):
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowpos
    HWND_NOTOPMOST = -2
    HWND_TOPMOST = -1
    HWND_TOP = 0
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    SWP_NOZORDER = 0x0004

    ctypes.windll.user32.SetWindowPos(
        ctypes.windll.kernel32.GetConsoleWindow(),
        HWND_TOP if top else HWND_NOTOPMOST,
        0,
        0,
        0,
        0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER,
    )


class SystemConsoleToggleOperator(bpy.types.Operator):
    """Show the system console"""
    bl_idname = "text.toggle"
    bl_label = "Toggle System Console"

    show_system_console: bpy.props.BoolProperty(
        name="Show Console",
        default=False,
        description="Toggle the visibility of the system console window.",
    )

    def execute(self, context):
        show_system_console(True)
        set_system_console_topmost(True)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "show_system_console")


def draw_system_console_toggle_button(self, context):
    layout = self.layout
    layout.separator()
    op = layout.operator(SystemConsoleToggleOperator.bl_idname)


def register():
    bpy.utils.register_class(SystemConsoleToggleOperator)
    bpy.types.TEXT_MT_text.append(draw_system_console_toggle_button)


def unregister():
    bpy.utils.unregister_class(SystemConsoleToggleOperator)
    bpy.types.TEXT_MT_text.remove(draw_system_console_toggle_button)


if __name__ == "__main__":
    register()
