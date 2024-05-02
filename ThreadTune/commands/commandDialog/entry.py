import adsk.core, adsk.fusion, traceback
import math
import os
import csv
import time

from ...lib import fusion360utils as futil
from ... import config
#import DrawThreads
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent
ui = app.userInterface



# TODO *** Specify the command identity information. ***
CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_cmdDialog'
CMD_NAME = 'ThreadTune'
CMD_Description = 'Fine-Tune your Screw Thread Designs'

# Specify that the command will be promoted to the panel.
IS_PROMOTED = True


WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []
import adsk.core, adsk.fusion, traceback
import math
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent
ui = app.userInterface
##########################################################################
def draw_regular_polygon(sketch, num_sides, rad):
    # Calculate the coordinates of the polygon's vertices
    angle_offset = math.pi / num_sides
    vertices = []
    for i in range(num_sides):
        angle = angle_offset + i * (2 * math.pi / num_sides)
        x = rad * math.cos(angle)
        y = rad * math.sin(angle)
        vertices.append(adsk.core.Point3D.create(x, y, 0))

    # Draw lines connecting the vertices
    lines = []
    for i in range(num_sides):
        start_point = vertices[i]
        end_point = vertices[(i + 1) % num_sides]
        lines.append(sketch.sketchCurves.sketchLines.addByTwoPoints(start_point, end_point))
    
    return lines
##########################################################################
def create_offset_plane_from_xy(construction_plane, offset_distance):
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent
# Get the construction planes collection.
    planes = design.rootComponent.constructionPlanes

# Get the XY construction plane.
    xy_plane = rootComp.xYConstructionPlane

# Create an offset plane from the XY construction plane.
    offset_plane_input = planes.createInput()
    offset_plane_input.setByOffset(xy_plane, adsk.core.ValueInput.createByReal(offset_distance))
    offset_plane = planes.add(offset_plane_input)

    return offset_plane
##########################################################################
def create_circle_sketch_on_plane(plane, radius):
    app = adsk.core.Application.get()
    design = app.activeProduct

# Get the sketches collection of the root component.
    sketches = design.rootComponent.sketches

# Create a sketch on the given plane.
    sketch = sketches.add(plane)

# Draw a circle at the origin with the given radius.
    center_point = adsk.core.Point3D.create(0, 0, 0)
    circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(center_point, radius)

    return sketch
##########################################################################
def DrawCylinder(R_Min, Ht1, iflag):
    # Draw a circle.
    circles = sketch_Helix.sketchCurves.sketchCircles
    circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), R_Min)
    circle2 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), Rad1+.01)

    # Get the profile defined by the circle.
    profCir = sketch_Helix.profiles.item(0)
    profCir1 = sketch_Helix.profiles.item(1)

    # Define that the extent is a distance extent of 5mm
    # Hardcoded for now until we can get this to work with number we input
    Ht2 = adsk.core.ValueInput.createByReal(Ht1)
    extrudes = rootComp.features.extrudeFeatures
    if iflag == 0:
        ext = extrudes.addSimple(profCir, Ht2, adsk.fusion.FeatureOperations.JoinFeatureOperation)
#Cut the threads that are below origin
        Ht3 = adsk.core.ValueInput.createByReal(-YB_B - 0.001)
        ext1 = extrudes.addSimple(profCir1, Ht3, adsk.fusion.FeatureOperations.CutFeatureOperation)
        ext2 = extrudes.addSimple(profCir, Ht3, adsk.fusion.FeatureOperations.CutFeatureOperation)
# Get the XY construction plane.
        xy_plane = create_offset_plane_from_xy
# Create the offset plane.
        Ht4 = float(Ht1)
        Ht5 = adsk.core.ValueInput.createByReal(YB_T + 0.001)
        offset_plane = create_offset_plane_from_xy(xy_plane,Ht4)
# Create sketch on the offset plane and draw a circle.
        sketchTop = create_circle_sketch_on_plane(offset_plane, Rad1+.01)
        profCir2 = sketchTop.profiles.item(0)
        ext3 = extrudes.addSimple(profCir2, Ht5, adsk.fusion.FeatureOperations.CutFeatureOperation)
    else:
        ext = extrudes.addSimple(profCir, Ht2, adsk.fusion.FeatureOperations.CutFeatureOperation)

def DrawHelix(Rad, Pitch, Ht, Ht1, sPts, G_Rail, RL_thread, iflag):
# Top Point for Center Vertical Line
        P10 = adsk.core.Point3D.create(0,0,Ht1 + .1)
        rev = Ht / Pitch
        turns = rev * 2.0 * math.pi
        segs = sPts * rev                     #18 is a good number to use for turns
        inc = turns / segs

# Create an object collection for the points.
        sketchSplines = sketch_Helix.sketchCurves.sketchFittedSplines
        sketchCenter = sketch_Helix.sketchCurves.sketchLines

        Vert_Line = sketchCenter.addByTwoPoints(P0,P10)       #Draw Center Vertical for Guide Rail with Sweeep

        points = adsk.core.ObjectCollection.create()
        points1  = adsk.core.ObjectCollection.create()
        ang = 0.0
        ang1 = 0.0
        global Rad1
        Rad1 = Rad * .1
        inc1 = inc
        Icount = 0
        Icount1 = 0
        if RL_thread == 'L':
            inc1 = inc * -1                      #this will change direction of helix to CW for Left hand threads
# Plot the points for the Helix
        while (ang <= turns):
            Icount = Icount + 1
            x = R_Min1 * math.cos(ang1)          # Helix point along inside Radius minus .1mm to fill any gap
            y = R_Min1 * math.sin(ang1)
            z = (Ht1 * (ang / turns))
# this should speed it up a little if we are not doing an outer guide rail helix
            if G_Rail != 'C':
                Icount1 = Icount1 + 1
                x1 = Rad1 * math.cos(ang1)           # Helix points along outside radius of thread
                y1 = Rad1 * math.sin(ang1)
                z1 = (Ht1 * (ang / turns))
                points1.add(adsk.core.Point3D.create(x1, y1, z1))     #Need 2nd spline for guide rail
            points.add(adsk.core.Point3D.create(x, y, z))

            ang = ang + inc
            ang1 = ang1 + inc1
# Create a 3D spline through the points.
        #msg = f'Ht: {Ht}<br>rev: {rev}<br>turns: {turns}<br>segs: {segs}<br>inc: {inc}<br>splinePts: {splinePts}<br>Icount: {Icount}<br>Icount1: {Icount1}'
        #ui.messageBox(msg)
        spline = sketchSplines.add(points)
        if G_Rail != 'C':
            spline1 = sketchSplines.add(points1)
            guide = rootComp.features.createPath(spline1)
# Get the profile defined by thread.
        prof = sketch_Profile.profiles.item(0)
        path = rootComp.features.createPath(spline)
        
        guideLine = rootComp.features.createPath(Vert_Line)

# Create a sweep input
        sweeps = rootComp.features.sweepFeatures
        if iflag == 0:
            sweepInput = sweeps.createInput(prof, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        else:
            sweepInput = sweeps.createInput(prof, path, adsk.fusion.FeatureOperations.CutFeatureOperation)
        if G_Rail == 'C':
            sweepInput.guideRail = guideLine
        else:
            sweepInput.guideRail = guide            #Default guide rail is the outer Helix
        sweepInput.profileScaling = adsk.fusion.SweepProfileScalingOptions.SweepProfileScaleOption
# Create the sweep.
        sweep = sweeps.add(sweepInput)
        if iflag ==0:
            global body1
            body1 = sweep.bodies.item(0)
            body1.name = Body_Name                      # rename body to most of input parameters from main routine

def DrawBoltHead(BoltFlat_Dia, num_sides, BoltHd_Ht):

# Define the number of sides and side length of the polygon
    #num_sides = 12                      # Change this value to set the number of sides
    Flat_OD = BoltFlat_Dia * .1         # Diameter between Flats
    Flat_Rad = Flat_OD / 2              # Rad of Flat Diamter
    Ang1 = 360.0 / (num_sides * 2)      # Amgle between a Vertex & center of a Flat
    PI1 = math.pi                       # Value of pi
    R_Ang1 = Ang1 * PI1 / 180.0         # Angle in radians
    Rad = Flat_Rad / math.cos(R_Ang1)   # Radius to a Vertex

    sketches = rootComp.sketches
    xyPlane = rootComp.xYConstructionPlane
    sketch_Head = sketches.add(xyPlane)
    sketch_Head.name = "sketch_Head"
# Draw the regular polygon
    polygon_lines = draw_regular_polygon(sketch_Head, num_sides, Rad)
# Get the profile defined by the Polygon.
    profPoly = sketch_Head.profiles.item(0)
    Ht2 = adsk.core.ValueInput.createByReal(-BoltHd_Ht * .1)
    extrudes = rootComp.features.extrudeFeatures
    ext = extrudes.addSimple(profPoly, Ht2, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    ##########################################################################
def DrawNut(NutFlat_Dia, num_sides, NutHd_Ht, Pitch):
# Define the number of sides and side length of the polygon
    #num_sides = 12                      # Change this value to set the number of sides
    Flat_OD = NutFlat_Dia * .1         # Diameter between Flats
    Flat_Rad = Flat_OD / 2              # Rad of Flat Diamter
    Ang1 = 360.0 / (num_sides * 2)      # Amgle between a Vertex & center of a Flat
    PI1 = math.pi                       # Value of pi
    R_Ang1 = Ang1 * PI1 / 180.0         # Angle in radians
    Rad = Flat_Rad / math.cos(R_Ang1)   # Radius to a Vertex
    sketches = rootComp.sketches
#    xyPlane = rootComp.xYConstructionPlane
# Get the XY construction plane.
    xy_plane = create_offset_plane_from_xy
    offset_plane = create_offset_plane_from_xy(xy_plane, float(Pitch * .1))
    sketch_Nut = sketches.add(offset_plane)
    sketch_Nut.name = "sketch_Nut"
# Draw the regular polygon
    polygon_lines = draw_regular_polygon(sketch_Nut, num_sides, Rad)
# Get the profile defined by the Polygon.
    profPoly = sketch_Nut.profiles.item(0)
    Ht2 = adsk.core.ValueInput.createByReal(NutHd_Ht * .1)
    extrudes = rootComp.features.extrudeFeatures
    ext = extrudes.addSimple(profPoly, Ht2, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body2 = rootComp.bRepBodies.itemByName('body2')
    #body2 = extrudes.bodies.item(0)
    #body2.name = BodyNut_Name 
##########################################################################
def DrawThreads(OD, Pitch, Ht, AngT, AngB, sPts, G_Rail, RL_thread, iflag):
    try:
        Ht1 = Ht * 0.1
        PI1 = math.pi
# We want to use the absolute value of largest angle to use with formulas to get R_Min
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

        H8 = H_Thread / 8
        H_5H8 = (5 * H_Thread) / 8
        H3 = ((H_5H8 + H8) * C_Ang) * 0.1

        P8 = Pitch / 8
        D_Min = (OD - (2 * abs(H_5H8))) * 0.1
        R_Min = D_Min / 2
        global R_Min1
        R_Min1 = D_Min / 2 - .01                    # need just a little more inward
                                                    # Because Helix sweep is not exact
        global YB_B                                 # These 2 are used for cutting bottom & top of threads flush
        global YB_T
        YB_B = (H_5H8 + H8 + .1) * B_Ang * .1       # Biggest Length closest to center
        YS_B = H8 * B_Ang * .1
        YB_T = (H_5H8 + H8 + .1) * T_Ang * .1       # Smallest Length on Outside Diameter
        YS_T = H8 * T_Ang * .1
# Center of everthing is at Origin 0,0,0
        global P0
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

# Create a new 3D sketch.
        global sketch_Helix
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch_Helix = sketches.add(xyPlane)
        sketch_Helix.name = "Sketch_Helix"

# Create sketch for the profile to sweep
        global sketch_Profile
        sketch_Profile = sketches.add(rootComp.xZConstructionPlane)
        sketch_Profile.name = "Thread_Profile"

        sketchLines = sketch_Profile.sketchCurves.sketchLines
        sketchLines.addByTwoPoints(P1,P2)
        sketchLines.addByTwoPoints(P2,P3)
        sketchLines.addByTwoPoints(P3,P4)
        sketchLines.addByTwoPoints(P4,P1)

        DrawHelix(Rad, Pitch, Ht, Ht1, sPts, G_Rail, RL_thread, iflag)
        DrawCylinder(R_Min, Ht1, iflag)
    except Exception as e:
        ui.messageBox("Error: {}".format(traceback.format_exc()))
##########################################################################
def get_current_folder():
    return os.path.dirname(os.path.abspath(__file__))

def file_exists(file_path):
    return os.path.exists(file_path)
def read_variables_from_text_file(Fname):
    variables = {}
    DialogName = open(Fname, 'r')
# Read variables from the text file
    with DialogName as file:
        variables['diameter'] = file.readline().strip()
        variables['pitch'] = file.readline().strip()
        variables['height'] = file.readline().strip()
        variables['angleTop'] = file.readline().strip()
        variables['angleBot'] = file.readline().strip()
        variables['splinePts'] = file.readline().strip()
        variables['GR_Char'] = file.readline().strip()
        variables['RL_Char'] = file.readline().strip()
    DialogName.close
    return variables


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
    current_folder = get_current_folder()           #Get the folder this program is located in

    cmd = args.command    
    inputs = cmd.commandInputs
    cmd.setDialogInitialSize(330, 330)
# Create tab input 1
    tabCmdInput1 = inputs.addTabCommandInput('_Threads', 'Threads')
    tab1ChildInputs = tabCmdInput1.children
# Create tab input 2
    tabCmdInput2 = inputs.addTabCommandInput('_BoltNut', 'Bolts and Nuts')
    tab2ChildInputs = tabCmdInput2.children
    global Fname
    global csvData
    global diameter
    global height
    global pitch
    global angleTop
    global angleBot
    global splinePts
    global GR_Char
    global RL_Char

    global Bolt_Sides
    global BoltFlat_Dia 
    global BoltHd_Ht
    global Nut_Sides
    global NutFlat_Dia
    global NutHd_Ht
    global MF_Gap
    #BN_Check
    Fname = current_folder + '\\' + 'DialogInput_V2.txt'   #This is the Default Input file from previous entries
    if file_exists(Fname):
        DialogName = open(Fname, 'r')
# Read variables from the text file if it exists
        with DialogName as f:
            reader = list(csv.reader(f))

        DialogName.close
    
        for csvData in reader:
            diameter = csvData[0]
            pitch = csvData[1]
            height = csvData[2]
            angleTop = csvData[3]
            angleBot = csvData[4]
            splinePts = csvData[5]
            GR_Char = csvData[6]
            RL_Char = csvData[7]

            Bolt_Sides = csvData[8]
            BoltFlat_Dia = csvData[9]
            BoltHd_Ht = csvData[10]
            Nut_Sides = csvData[11]
            NutFlat_Dia = csvData[12]
            NutHd_Ht = csvData[13]
            MF_Gap = csvData[14]
            BN_Check = csvData[15]
# File does not exist, so set the defaults to these
    else:
        diameter = '6'
        pitch = '1'
        height = '5'
        angleTop = '30'
        angleBot = '30'
        splinePts = '18'
        GR_Char = 'C'
        RL_Char = 'R'
 
        Bolt_Sides = '6'
        BoltFlat_Dia = '10'
        BoltHd_Ht = '4'
        Nut_Sides = '6'
        NutFlat_Dia = '10'
        NutHd_Ht = '5'
        MF_Gap = '0.3'
        BN_Check = 'Y'
# Create a dropdown command input
    global dropDownCommandInput
    dropDownCommandInput = tab1ChildInputs.addDropDownCommandInput('MetType', 'Metric Thread Type:', adsk.core.DropDownStyles.TextListDropDownStyle);
    # Subscribe to the dropdown change event
    #dropdownInput0.listItemActivated.add(onDropdownChange)
    MFname = current_folder + '\\' + 'metric_V2.txt'        #Standard Metric sizes from M3 - M30
    global Metdata
    if file_exists(MFname):
# Read the Metric Sizes file
        file = open(MFname, "r")
        Metdata = list(csv.reader(file, delimiter=","))
        file.close()
        outstr = ""
        j = len(Metdata)
        dropdown0Items = dropDownCommandInput.listItems
        for i in range(1,j):
            outstr= Metdata[i][0] + Metdata[i][1]+ "x" + Metdata[i][2]
            dropdown0Items.add(outstr, False, '')                       #Add this Metric size to the Dropdownlist
# Create a value input field and set the default using 1 unit of the default length unit.
    #tab1ChildInputs.addTextBoxCommandInput('writable_textBox', 'Text Box 2', 'This is an example of an editable text box.', 2, False)
    global _diameter
    global _pitch
    global _BoltFlat_Dia
    global _BoltHd_Ht
    global _NutFlat_Dia
    global _NutHd_Ht
    
    _diameter = tab1ChildInputs.addTextBoxCommandInput('diameter','Diameter (mm): ',diameter, 1, False )
    
    _pitch = tab1ChildInputs.addTextBoxCommandInput('pitch', 'Pitch (mm): ', pitch, 1, False)
    tab1ChildInputs.addTextBoxCommandInput('height', 'Height (mm): ', height, 1, False)
    tab1ChildInputs.addTextBoxCommandInput('angleTop', 'Top Angle (deg): ', angleTop, 1, False)
    tab1ChildInputs.addTextBoxCommandInput('angleBot', 'Bottom Angle (deg): ', angleBot, 1, False)
    tab1ChildInputs.addTextBoxCommandInput('splinePts', 'Helix Spline Points: ', splinePts, 1, False)

    tab2ChildInputs.addTextBoxCommandInput('Bolt_Sides', '# of Bolt Head Sides: ', Bolt_Sides, 1, False)
    _BoltFlat_Dia = tab2ChildInputs.addTextBoxCommandInput('BoltFlat_Dia', 'Bolt Head Flat Dia: ', BoltFlat_Dia, 1, False)
    _BoltHd_Ht = tab2ChildInputs.addTextBoxCommandInput('BoltHd_Ht', 'Bolt Head Height: ', BoltHd_Ht, 1, False)
    tab2ChildInputs.addTextBoxCommandInput('Nut_Sides', '# of Sides of Nut: ', Nut_Sides, 1, False)
    _NutFlat_Dia = tab2ChildInputs.addTextBoxCommandInput('NutFlat_Dia', 'Nut Flat Dia: ', NutFlat_Dia, 1, False)
    _NutHd_Ht = tab2ChildInputs.addTextBoxCommandInput('NutHd_Ht', 'Nut Height: ', NutHd_Ht, 1, False)
    tab2ChildInputs.addTextBoxCommandInput('MF_Gap', 'M/F thread Gap: ', MF_Gap, 1, False)
    #inputs.addTextBoxCommandInput('GuideRail', 'Helix Guide Rail or Centerline Guide: ', GR_Char, 1, False)
# Create dropdown input with test list style.
    dropdownInput1 = tab1ChildInputs.addDropDownCommandInput('GuideRail', 'Helix Guide Rail or Centerline Guide:', adsk.core.DropDownStyles.TextListDropDownStyle);
    dropdown4Items = dropdownInput1.listItems
# Test what was used for the guideline on previous run
    if GR_Char == 'H':
        dropdown4Items.add('Helix', True, '')
        dropdown4Items.add('CenterLine', False, '')
    else:
        dropdown4Items.add('Helix', False, '')
        dropdown4Items.add('CenterLine', True, '')
    dropdownInput2 = tab1ChildInputs.addDropDownCommandInput('RightLeft', 'Right or Left Threads', adsk.core.DropDownStyles.TextListDropDownStyle);
    dropdown4Items = dropdownInput2.listItems
# Test what was used for the Thread direction on previous run
    if RL_Char == 'R':
        dropdown4Items.add('Right', True, '')
        dropdown4Items.add('Left', False, '')
    else:
        dropdown4Items.add('Right', False, '')
        dropdown4Items.add('Left', True, '')

# Create bool value input with checkbox style.
    if BN_Check == 'Y':
        tab2ChildInputs.addBoolValueInput('_DrawBoltNut', 'Draw Bolt & Nut', True, '', True)
    else:
        tab2ChildInputs.addBoolValueInput('_DrawBoltNut', 'Draw Bolt & Nut', True, '', False)

# Connect to event handlers
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

    Bolt_Sides: adsk.core.TextBoxCommandInput = inputs.itemById('Bolt_Sides')
    BoltFlat_Dia: adsk.core.TextBoxCommandInput = inputs.itemById('BoltFlat_Dia')
    BoltHd_Ht: adsk.core.TextBoxCommandInput = inputs.itemById('BoltHd_Ht')
    Nut_Sides: adsk.core.TextBoxCommandInput = inputs.itemById('Nut_Sides')
    NutFlat_Dia: adsk.core.TextBoxCommandInput = inputs.itemById('NutFlat_Dia')
    NutHd_Ht: adsk.core.TextBoxCommandInput = inputs.itemById('NutHd_Ht')
    MF_Gap: adsk.core.TextBoxCommandInput = inputs.itemById('MF_Gap')

    dropDownInput1 = inputs.itemById('GuideRail')
    GuideRail = dropDownInput1.selectedItem.name

    dropDownInput2 = inputs.itemById('RightLeft')
    RtLt = dropDownInput2.selectedItem.name

    BoltNutYesNo = 0
    BN_Check = 'N'
    _DrawBoltNut: adsk.core.BoolValueCommandInput = inputs.itemById('_DrawBoltNut')
    if _DrawBoltNut.value:
        BN_Check = 'Y'
        BoltNutYesNo = 1

    diameter = diameter.text
    pitch = pitch.text
    height = height.text
    angleTop = angleTop.text
    angleBot = angleBot.text
    splinePts = splinePts.text

    Bolt_Sides = Bolt_Sides.text
    BoltFlat_Dia = BoltFlat_Dia.text
    BoltHd_Ht = BoltHd_Ht.text
    Nut_Sides = Nut_Sides.text
    NutFlat_Dia = NutFlat_Dia.text
    NutHd_Ht = NutHd_Ht.text
    MF_Gap = MF_Gap.text
    
    GR_Char = 'C'
    RL_Char = 'R'
    if GuideRail == 'Helix':
        GR_Char = 'H'
    if RtLt == 'Left':
        RL_Char = 'L'

# Write back user inputs as defaults for next time
    BoltNut = Bolt_Sides + "," + BoltFlat_Dia + "," + BoltHd_Ht + "," + Nut_Sides + "," + NutFlat_Dia + "," + NutHd_Ht + "," + MF_Gap + "," + BN_Check
    OutString = diameter +',' + pitch +',' + height +',' + angleTop +',' + angleBot +',' + splinePts +',' + GR_Char +',' + RL_Char + ',' + BoltNut
    with open(Fname, 'w') as csvfile:
        csvfile.write(OutString)
    csvfile.close
    global Body_Name
    Body_Name = "M" + diameter + "_" + pitch + "Px" + height + "mm" + "_" + RL_Char + "_" + angleTop + "D_" + angleBot + "D_" + splinePts + "spts_" + GR_Char + "_Guide"
    msg = f'diameter: {diameter}<br>pitch: {pitch}<br>height: {height}<br>angleTop: {angleTop}<br>angleBot: {angleBot}<br>splinePts: {splinePts}GR_Char: {GR_Char}<br>RL_Char: {RL_Char}<br>'
    #ui.messageBox(msg)
    sPts = int(splinePts)
    start = time.time()
    OD = float(diameter)
    Pit = float(pitch)
    DrawThreads(OD, Pit, float(height), float(angleTop), float(angleBot), sPts, GR_Char, RL_Char, 0)
    if BoltNutYesNo == 1:
        NH_Ht = float(NutHd_Ht)
        Nt_Thread_Ht = NH_Ht + Pit + Pit
        DrawBoltHead(float(BoltFlat_Dia),int(Bolt_Sides),float(BoltHd_Ht))
        hide_body(body1)
        OD1 = (float(MF_Gap) * 2.0)  + OD
        msg = f'OD: {OD}<br>OD1: {OD1}'
        #ui.messageBox(msg)
        global BodyNut_Name
        BodyNut_Name = "M" + diameter + "_Nut"
        DrawNut(float(NutFlat_Dia), int(Nut_Sides), float(NutHd_Ht),float(pitch))
        DrawThreads(OD1, Pit, Nt_Thread_Ht, float(angleTop), float(angleBot), sPts, GR_Char, RL_Char, 1)
        unhide_body(body1)
    end = time.time()
    Elapsed = round(end - start,2)
        #msg = f'Elapsed Time: {Elapsed} seconds'
        #ui.messageBox(msg)
def hide_body(body):
    if body.isVisible:
        body.isVisible = False
def unhide_body(body):
    if not body.isVisible:
        body.isVisible = True

# This event handler is called when the command needs to compute a new preview in the graphics window.
def command_preview(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Preview Event')
    inputs = args.command.commandInputs


# This event handler is called when the user changes anything in the command dialog
# allowing you to modify values of other inputs based on that change.
            #Connect handler to inputChanged event
def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    if args.input.id == 'MetType':
        #Met_Item = dropDownCommandInput.selectedItem.name
        Met_ID = dropDownCommandInput.selectedItem.index
        Met_ID = Met_ID + 1
        #msg = f'Met_ID = {Met_ID}'
        #ui.messageBox(msg)
        diameter = Metdata[Met_ID][1]
        pitch = Metdata[Met_ID][2]
        BoltFlat_Dia = Metdata[Met_ID][3]
        BoltHd_Ht = Metdata[Met_ID][4]
        NutFlat_Dia = Metdata[Met_ID][3]
        NutHd_Ht = Metdata[Met_ID][5]
# Set all the appropriate text boxes
        _diameter.text = diameter
        _pitch.text = pitch
        _BoltFlat_Dia.text = BoltFlat_Dia
        _BoltHd_Ht.text = BoltHd_Ht
        _NutFlat_Dia.text = NutFlat_Dia
        _NutHd_Ht.text = NutHd_Ht
#Metric, Diameter, Pitch, Hex Bolt Flat Diameter, Hex Head Thickness, Hex Nut Thickness
#M,      3,        0.5,   5.5,                    2.1,                2.4
#0       1         2      3                       4                   5
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
