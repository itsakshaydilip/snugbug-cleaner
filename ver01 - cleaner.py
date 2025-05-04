import maya.cmds as cmds
import maya.mel as mel
import time

def cleanup_scene(*args):
    cmds.button(startButton, edit=True, enable=False)
    
    # Initialize a log variable
    log = ""

    # Action 1: Checking and Deleting Unwanted Nodes
    unwanted_nodes = cmds.ls(type=["unknown", "unknownDag", "unknownTransform"])
    if unwanted_nodes:
        cmds.delete(unwanted_nodes)
        log += f"Action 1: Deleted {len(unwanted_nodes)} unwanted nodes. Completed.\n"
        unwanted_nodes_deleted = True
    else:
        log += "Action 1: No unwanted nodes found. Completed.\n"
        unwanted_nodes_deleted = False
    time.sleep(4)  # Delay for 4 seconds

    # Action 2: Checking and Deleting Empty Groups
    empty_groups = [grp for grp in cmds.ls(type="transform") if not cmds.listRelatives(grp, children=True)]
    if empty_groups:
        cmds.delete(empty_groups)
        log += f"Action 2: Deleted {len(empty_groups)} empty groups. Completed.\n"
    else:
        log += "Action 2: No empty groups found. Completed.\n"
    time.sleep(4)  # Delay for 4 seconds

    # Action 3: Centering Pivot for All Objects
    all_objects = cmds.ls(dag=True, long=True)
    progress_label = cmds.text(progressTextLabel, edit=True, label="Action 3: Centering Pivot...")
    
    for i, obj in enumerate(all_objects):
        cmds.select(obj)
        mel.eval('CenterPivot;')
        cmds.refresh()  # Force UI update
    log += "Action 3: Centering Pivot: Completed.\n"
    time.sleep(4)  # Delay for 4 seconds

    # Action 4: Resetting the Maya Viewport
    mel.eval('FrameAll;')
    log += "Action 4: Resetting the Maya Viewport: Completed.\n"
    time.sleep(4)  # Delay for 4 seconds

    # Action 5: Deleting Unused Nodes Using HyperShade
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    log += "Action 5: Deleting Unused Nodes: Completed.\n"
    
    # Update the text label with the accumulated log
    cmds.text(progressTextLabel, edit=True, label=log)

    # Display message about unwanted nodes deleted
    if unwanted_nodes_deleted:
        cmds.warning("Unwanted nodes deleted.")
    
    # Group all visible objects and name the group "GEO" if it doesn't exist
    group_geo()
    
    cmds.button(startButton, edit=True, enable=True)
    cmds.text(finishLabel, edit=True, label="Snubug Cleaner complete.")

def group_geo():
    if not cmds.objExists("GEO"):
        visible_objects = cmds.ls(visible=True, long=True)
        if visible_objects:
            geo_group = cmds.group(visible_objects, name="GEO")
            cmds.warning(f"Grouped {len(visible_objects)} visible objects into 'GEO' group. Completed.")
    else:
        cmds.warning("Group 'GEO' already exists. Skipping group creation.")

if cmds.window("cleanupWindow", exists=True):
    cmds.deleteUI("cleanupWindow", window=True)

window = cmds.window("cleanupWindow", title="Snubug Cleaner", widthHeight=(400, 400))
cmds.columnLayout(adjustableColumn=True)

cmds.text(label="Click 'Start Cleanup' to begin:")
startButton = cmds.button(label="Start Cleanup", command=cleanup_scene)
progressTextLabel = cmds.text(label="", align="left", wordWrap=True)
finishLabel = cmds.text(label="", align="center")

cmds.showWindow(window)
