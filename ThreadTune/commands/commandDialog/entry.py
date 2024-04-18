import adsk.core, adsk.fusion, traceback
import math
import os
from ...lib import fusion360utils as futil
from ... import config
app = adsk.core.Application.get()
ui = app.userInterface


# TODO *** Specify the command identity information. ***
CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_cmdDialog'
CMD_NAME = 'ThreadTune'
CMD_Description = 'Fine-Tune your Screw Thread Designs'

# Specify that the command will be promoted to the panel.
IS_PROMOTED = True

# TODO *** Define the location where the command button will be created. ***
# This is done by specifying the workspace, the tab, and the panel, and the 
# command it will be inserted beside. Not providing the command to position it
# will insert it at the end.
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []

def DrawThreads(dia_exp, pitch_exp, height_exp, angleTop, angleBot, splinePts, G_Rail, RL_thread):
    try:

# Get the root component of the active design
        design = app.activeProduct
        product = app.activeProduct
        rootComp = design.rootComponent

        OD = dia_exp
        Pitch = pitch_exp
        AngT = angleTop
        AngB = angleBot
        Ht = height_exp
        Ht1 = Ht * 0.1
        LH = 1
        PI1 = math.pi
#We want to use the absolute value of largest angle to use with formulas to get R_Min
        abs_angT = abs(AngT)
        abs_angB = abs(AngB)
        ang = abs_angB
    
        if abs_angT < abs_angB:
            ang = abs_angT
        if ang == 0.0:
            ang = 30.0
        if AngT < 0 and AngB < 0:
            if abs_angT > abs_angB:
                ang = AngT
            else:
                ang = AngB
        T_Ang = math.tan(float(AngT) * PI1/float(180.0))
        B_Ang = math.tan(float(AngB) * PI1/float(180.0))
        C_Ang = math.tan(float(ang) * PI1/float(180.0))
        Rad = OD / 2.0
        H_Thread = (1 / C_Ang) * (Pitch / 2)
# Test for angle of 0.0 because we can't divide by 0
        if T_Ang == 0.0:
            H_Thread_T = 0.0
        else:
            H_Thread_T = (1 / T_Ang) * (Pitch / 2)
        if B_Ang == 0.0:
            H_Thread_B = 0.0
        else:
            H_Thread_B = (1 / B_Ang) * (Pitch / 2)

        H8 = H_Thread / 8
        H_5H8 = (5 * H_Thread) / 8
        H3 = ((H_5H8 + H8) * C_Ang) * 0.1

        P8 = Pitch / 8
        D_Min = (OD - (2 * abs(H_5H8))) * 0.1
        R_Min = D_Min / 2
        R_Min1 = D_Min / 2 - .01                    # need just a little more inward
                                                    # Because Helix sweep is not exact
        YB_B = (H_5H8 + H8 + .1) * B_Ang * .1       # Biggest Length closest to center
        YS_B = H8 * B_Ang * .1
        YB_T = (H_5H8 + H8 + .1) * T_Ang * .1       # Smallest Length on Outside Diameter
        YS_T = H8 * T_Ang * .1
# Center of everthing is at Origin 0,0,0
        P0 = adsk.core.Point3D.create(0,0,0)
        
# Points for Bottom Angle
# Points P1 & P4 are the points Minimum Radius
# Points P2 & P3 are the points on the Outside Radius
# Points P5 & P6 are 5mm inward to fill in gap when cylinder of radius R_Min is added
# This gap is due to the helix using spline points that are just a hair off of being cylindrical
 
# For some reason, points for this profile below the X-Axis are Positive.  I would think they would be negative
        if AngB > 0:
            P1 = adsk.core.Point3D.create(R_Min1, YB_B, 0)
            P2 = adsk.core.Point3D.create(Rad * 0.1, YS_B, 0)
        elif AngB == 0:
            P1 = adsk.core.Point3D.create(R_Min1, H3, 0)
            P2 = adsk.core.Point3D.create(Rad * 0.1, H3, 0)
        elif AngB < 0:
            P1 = adsk.core.Point3D.create(R_Min1, YS_B, 0)
            P2 = adsk.core.Point3D.create(Rad * 0.1, YB_B, 0)
# Points for Top Angle
        if AngT > 0:
            P3 = adsk.core.Point3D.create(Rad * 0.1, -YS_T, 0)
            P4 = adsk.core.Point3D.create(R_Min1, -YB_T, 0)
        elif AngT == 0:
            P3 = adsk.core.Point3D.create(Rad * 0.1, -H3, 0)
            P4 = adsk.core.Point3D.create(R_Min1,-H3, 0)
        elif AngT < 0:
            P3 = adsk.core.Point3D.create(Rad * 0.1, -YB_T, 0)
            P4 = adsk.core.Point3D.create(R_Min1, -YS_T, 0)
# Top Point for Center Vertical Line
        P10 = adsk.core.Point3D.create(0,0,Ht1 + .1)
# Create a new 3D sketch.
        sketches = rootComp.sketches
        sketch_Helix = sketches.add(rootComp.xYConstructionPlane)
        sketch_Helix.name = "Sketch_Helix"

# Draw circle with minimum radius.
        sketchCircles = sketch_Helix.sketchCurves.sketchCircles
        circle = sketchCircles.addByCenterRadius(P0, R_Min)
        profCir = sketch_Helix.profiles.item(0)                 #Can't get cylinder automatically Extruded yet

# Create sketch for the profile to sweep
        sketch_Profile = sketches.add(rootComp.xZConstructionPlane)
        sketch_Profile.name = "sketch_Profile"

        sketchLines = sketch_Profile.sketchCurves.sketchLines
        sketchLines.addByTwoPoints(P1,P2)
        sketchLines.addByTwoPoints(P2,P3)
        sketchLines.addByTwoPoints(P3,P4)
        sketchLines.addByTwoPoints(P4,P1)

        rev = Ht * Pitch
        turns = rev * 2.0 * math.pi
        segs = splinePts * rev                     #18 is a good number to use for turns
        inc = turns / segs

# Create an object collection for the points.
        sketchSplines = sketch_Helix.sketchCurves.sketchFittedSplines
        sketchCenter = sketch_Helix.sketchCurves.sketchLines

        Vert_Line = sketchCenter.addByTwoPoints(P0,P10)       #Draw Center Vertical for Guide Rail with Sweeep

        points = adsk.core.ObjectCollection.create()
        points1  = adsk.core.ObjectCollection.create()
        ang = 0.0
        ang1 = 0.0
        Rad1 = Rad * .1
        inc1 = inc
        if RL_thread == 'L':
            inc1 = inc * -1                      #this will change direction of helix to CW for Left hand threads
# Plot the points for the Helix
        while (ang <= turns):
            x = R_Min1 * math.cos(ang1)          # Helix point along inside Radius minus .1mm to fill any gap
            y = R_Min1 * math.sin(ang1)
            z = (Ht1 * (ang / turns))

            x1 = Rad1 * math.cos(ang1)           # Helix points along outside radius of thread
            y1 = Rad1 * math.sin(ang1)
            z1 = (Ht1 * (ang / turns))
            points.add(adsk.core.Point3D.create(x, y, z))
            points1.add(adsk.core.Point3D.create(x1, y1, z1))     #Need 2nd spline for guide rail
            ang = ang + inc
            ang1 = ang1 + inc1
# Create a 3D spline through the points.
        spline = sketchSplines.add(points)
        spline1 = sketchSplines.add(points1)

# Get the profile defined by thread.
        prof = sketch_Profile.profiles.item(0)
        path = rootComp.features.createPath(spline)
        guide = rootComp.features.createPath(spline1)
        guideLine = rootComp.features.createPath(Vert_Line)

# Create a sweep input
        sweeps = rootComp.features.sweepFeatures
        sweepInput = sweeps.createInput(prof, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        sweepInput.guideRail = guide            #Default guide rail is the outer Helix
        if G_Rail == 'C':
            sweepInput.guideRail = guideLine
        sweepInput.profileScaling = adsk.fusion.SweepProfileScalingOptions.SweepProfileScaleOption
# Create the sweep.
        sweep = sweeps.add(sweepInput)
        body1 = sweep.bodies.item(0)
        body1.name = "M6x5mm_Threads"
#  Create the extrusion of cylinder (Does Not work yet)
        #extrudes = rootComp.features.extrudeFeatures
        #ext = extrudes.addSimple(profCir, Ht1, adsk.fusion.FeatureOperations.JoinFeatureOperation) 
    except Exception as e:
        ui.messageBox("Error: {}".format(traceback.format_exc()))
# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get the panel the button will be created in.
    panel = workspace.toolbarPanels.itemById(PANEL_ID)

    # Create the button command control in the UI after the specified existing command.
    control = panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False)

    # Specify if the command is promoted to the main toolbar. 
    control.isPromoted = IS_PROMOTED

# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()

# Function that is called when a user clicks the corresponding button in the UI.
# This defines the contents of the command dialog and connects to the command related events.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Created Event')

    # https://help.autodesk.com/view/fusion360/ENU/?contextId=CommandInputs
    #ui.messageBox('Before dlgImage')
    inputs = args.command.commandInputs
    #dlgImageFilename = 'Thread_Types_240x240.png'  # File name of the image for thread profile
    #dlgImagePath = 'resources/'  # Path to the image file

    # Add image preview (Does not work yet)
    #imgInput = inputs.addImageCommandInput('imgInput', '', dlgImagePath + dlgImageFilename)
    #imgInput.isVisible = True
# Create a value input field and set the default using 1 unit of the default length unit.
    inputs.addTextBoxCommandInput('diameter', 'Diameter (mm): ', '6', 1, False)
    inputs.addTextBoxCommandInput('pitch', 'Pitch (mm): ', '1', 1, False)
    inputs.addTextBoxCommandInput('height', 'Height (mm): ', '5', 1, False)
    inputs.addTextBoxCommandInput('angleTop', 'Top Angle (deg): ', '30', 1, False)
    inputs.addTextBoxCommandInput('angleBot', 'Bottom Angle (deg): ', '30', 1, False)
    inputs.addTextBoxCommandInput('splinePts', 'Helix Spline Points: ', '36', 1, False)
    inputs.addTextBoxCommandInput('GuideRail', 'Helix Guide Rail or Centerline Guide: ', 'C', 1, False)
    inputs.addTextBoxCommandInput('RL_thread', 'Right or Left Thread: ', 'R', 1, False)
# Create dropdown input with radio style.

    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.inputChanged, command_input_changed, local_handlers=local_handlers)
    futil.add_handler(args.command.executePreview, command_preview, local_handlers=local_handlers)
    futil.add_handler(args.command.validateInputs, command_validate_input, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)

# This event handler is called when the user clicks the OK button in the command dialog or 
# is immediately called after the created event not command inputs were created for the dialog.
def command_execute(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Execute Event')

    # Get a reference to your command's inputs.
    inputs = args.command.commandInputs
    diameter: adsk.core.TextBoxCommandInput = inputs.itemById('diameter')
    pitch: adsk.core.TextBoxCommandInput = inputs.itemById('pitch')
    height: adsk.core.TextBoxCommandInput = inputs.itemById('height')
    angleTop: adsk.core.TextBoxCommandInput = inputs.itemById('angleTop')
    angleBot: adsk.core.TextBoxCommandInput = inputs.itemById('angleBot')
    splinePts: adsk.core.TextBoxCommandInput = inputs.itemById('splinePts')
    GuideRail: adsk.core.TextBoxCommandInput = inputs.itemById('GuideRail')
    RL_thread: adsk.core.TextBoxCommandInput = inputs.itemById('RL_thread')
    # Do something interesting
    diameter = diameter.text
    pitch = pitch.text
    height = height.text
    angleTop = angleTop.text
    angleBot = angleBot.text
    splinePts = splinePts.text
    RL_thread = RL_thread.text
    GuideRail = GuideRail.text

    GR_Char = GuideRail[0].upper()
    RL_Char = RL_thread[0].upper()
    if RL_Char != 'R' and RL_Char != 'L':
        msg = f'Must be a Right or Left Thread, you entered : "{RL_Char}" for 1st character'
        ui.messageBox(msg)
    else:
        DrawThreads(float(diameter), float(pitch), float(height), float(angleTop), float(angleBot), int(splinePts), GR_Char, RL_Char)

# This event handler is called when the command needs to compute a new preview in the graphics window.
def command_preview(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Preview Event')
    inputs = args.command.commandInputs


# This event handler is called when the user changes anything in the command dialog
# allowing you to modify values of other inputs based on that change.
def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    inputs = args.inputs

    # General logging for debug.
    futil.log(f'{CMD_NAME} Input Changed Event fired from a change to {changed_input.id}')


# This event handler is called when the user interacts with any of the inputs in the dialog
# which allows you to verify that all of the inputs are valid and enables the OK button.
def command_validate_input(args: adsk.core.ValidateInputsEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Validate Input Event')

    inputs = args.inputs
    
    # Verify the validity of the input values. This controls if the OK button is enabled or not.
    valueInput = inputs.itemById('value_input')
    if valueInput.value >= 0:
        args.areInputsValid = True
    else:
        args.areInputsValid = False
        

# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Destroy Event')

    global local_handlers
    local_handlers = []
