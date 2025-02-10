# Setting up the client
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
from AudioDome_Communication_Setup import *

# Command functions in practice
#Check if a input value is float or not
def check_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

#-------- Scene Commands
#Play a scene
def play_scene(sceneID):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    command = "/scene/{}/play".format(sceneID)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process()


#Stop a scene
def stop_scene(sceneID):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    command = "/scene/{}/stop".format(sceneID)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process()   

#-------- Object Commands
#Play an object
def play_object(sceneID, objectID):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    command = "/scene/{}/object/{}/play".format(sceneID, objectID)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process()   

#Stop an object
def stop_object(sceneID, objectID):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    command = "/scene/{}/object/{}/stop".format(sceneID, objectID)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process()

#Set the gain of an object
def set_object_gain(sceneID, objectID, objectGain):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    #   objectGain: string variable refering to the object's gain in dB (between -40 to 40)
    if check_float(objectGain) is False:
        objectGain = "0"

    command = "/scene/{0}/object/{1}/gain/{2}".format(sceneID, objectID, objectGain)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process() 

#Set the azimuth angle of an object
def set_object_azimuth(sceneID, objectID, objectAzimuth):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    #   objectAzimuth:  string variable refering to the object's azimuth angle in degrees (between -180 and 180)
    command = "/scene/{0}/object/{1}/azi/{2}".format(sceneID, objectID, objectAzimuth)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process()

#Set the elevation angle of an object
def set_object_elevation(sceneID, objectID, objectElevation):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    #   objectElevation:  string variable refering to the object's elevation angle in degrees (between -90 and 90)
    command = "/scene/{0}/object/{1}/ele/{2}".format(sceneID, objectID, objectElevation)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process()  

#Set the speaker channel of an object
def set_object_channel(sceneID, objectID, objectChannel):
    # Note 1:   For audio to come from just the set speaker channel you must switch the panning method to "nearest" with the 'set_object_panning' command.
    # Note 2:   This command will change the object's position (the set azimuth and elevation angles are cleared after running this command).
    # Note 3:   The change in position with this command is not overwritten on azimuth and elevation levels in the spatial audio creator GUI. For compatibality reasons it's also avoided here.

    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    #   objectChannel:  string variable refering to the channel number of interest (between 1 to 91)
    command = "/scene/{0}/object/{1}/channeldir/{2}".format(sceneID, objectID, objectChannel)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process()  

#Set the panning method of an object. 
def set_object_panning(sceneID, objectID, objectPanningMethod):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    #   objectPanningMethod:    string variable refering to object panning method: "ambi"||"vbap"||"nearest"
    command = "/scene/{0}/object/{1}/method/{2}".format(sceneID, objectID, objectPanningMethod)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process()   

#Set/unset looping (repeting infinitly) cues of an object
def set_object_loop(sceneID, objectID, loopStatus):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    #   loopStatus: string variable turning on or off the object's looping: "on"||"off"
    command = "/scene/{0}/object/{1}/loop/{2}".format(sceneID, objectID, loopStatus)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process() 

#Set/unset the room effect of an object
def set_object_room_effect(sceneID, objectID, roomEffectStatus):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    #   roomEffectStatus:   string variable turning on or off the room effect on an object: "on"||"off"
    command = "/scene/{0}/object/{1}/room/{2}".format(sceneID, objectID, roomEffectStatus)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process() 

#-------- Cue Commands
#Play a cue
def play_cue(sceneID, objectID, cueID):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    #   cueID:      string variable refering to the cue number belonging to the object specified with objectID
    command = "/scene/{0}/object/{1}/cue/{2}/play".format(sceneID, objectID, cueID)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process() 

#Stop a cue
def stop_cue(sceneID, objectID, cueID):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    #   cueID:      string variable refering to the cue number belonging to the object specified with objectID
    command = "/scene/{0}/object/{1}/cue/{2}/stop".format(sceneID, objectID, cueID)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process()

#Select a cue beloning to an object
def set_cue_select(sceneID, objectID, cueID):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    #   cueID:      string variable refering to the cue number belonging to the object specified with objectID - to be set as for the object
    command = "/scene/{0}/object/{1}/cue/{2}/select".format(sceneID, objectID, cueID)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process() 

#Set the gain of a cue (belonging to an object)
def set_cue_gain(sceneID, objectID, cueID, cueGain):
    # Inputs:
    #   sceneID:    string variable refering to the scene number on the spatial sound creator
    #   objectID:   string variable refering to the object number in the scene specified with sceneID
    #   cueID:      string variable refering to the cue number belonging to the object specified with objectID
    #   cueGain:    string variable refering to that specific cue's gain in dB (between -40 to 40)
    if check_float(cueGain) is False:
        cueGain = "0"

    command = "/scene/{0}/object/{1}/cue/{2}/gain/{3}".format(sceneID, objectID, cueID, cueGain)
    #print("Sending "+command)
    msg = oscbuildparse.OSCMessage(command,None,[])
    osc_send(msg, clientName)
    osc_process()

class cue:
    def __init__(self, ID, name, object_ID, scene_ID):
        # Cue info
        self.ID = ID
        self.name = name
        self.gain = 0
        self.selected = (ID==0)

        # Belongingness info
        self.object_ID = object_ID
        self.scene_ID = scene_ID

        # Sending relevant commands to the dome
        self.set_gain(self.gain)
    
    # Methods to change atributes and communicate changes to the dome
    # Play
    def play(self):
        play_cue(self.scene_ID, self.object_ID, self.ID)

    #Stop
    def stop(self):
        stop_cue(self.scene_ID, self.object_ID, self.ID)

    # Set gain
    def set_gain(self, gain):
        self.gain = gain
        set_cue_gain(self.scene_ID, self.object_ID, self.ID, self.gain)

class auditory_object:
    def __init__(self, ID, name, scene_ID, panning_method, room_effect):
        # Auditory object info
        self.ID = ID
        self.name = name
        self.gain = 0
        self.channel = 1
        self.azi = 0
        self.ele = 0
        self.panning_method = panning_method
        self.loop = "off"
        self.room_effect = room_effect
        self.dist = 0.3 # communication and initiation?

        # Belongingness info
        self.scene_ID = scene_ID

        # Associated Cues
        self.cues = [cue(0, "Reserved Cue", self.ID, self.scene_ID)]
        self.selected_cue_ID = 0 # initiated with the reserved cue

        # Sending relevant commands to the dome
        self.set_gain(self.gain)
        self.set_channel(self.channel)
        self.set_azimuth(self.azi)
        self.set_elevation(self.ele)
        self.set_panning(self.panning_method)
        self.turn_loop(self.loop)
        self.turn_roomEffect(self.room_effect)

    # Methods to change atributes and communicate changes to the dome
    # Play
    def play(self):
        play_object(self.scene_ID, self.ID)

    #Stop
    def stop(self):
        stop_object(self.scene_ID, self.ID)

    # Set gain
    def set_gain(self, gain):
        self.gain = gain
        set_object_gain(self.scene_ID, self.ID, self.gain)

    # Set azimuth
    def set_azimuth(self, azi):
        self.azi = azi
        set_object_azimuth(self.scene_ID, self.ID, self.azi)

    # Set channel
    def set_channel(self, channel):
        self.channel = channel
        set_object_channel(self.scene_ID, self.ID, self.channel)

    # Set elevation
    def set_elevation(self, ele):
        self.ele = ele
        set_object_elevation(self.scene_ID, self.ID, self.ele)

    # Set panning method
    def set_panning(self, panning_method):
        self.panning_method = panning_method
        set_object_panning(self.scene_ID, self.ID, self.panning_method)

    # Set looping
    def turn_loop(self, loop):
        self.loop = loop
        set_object_loop(self.scene_ID, self.ID, self.loop)
    
    # Set room effect
    def turn_roomEffect(self, room_effect):
        self.room_effect = room_effect
        set_object_room_effect(self.scene_ID, self.ID, self.room_effect)

    # The method to add cues to an object
    def add_cue(self, cue_ID, cue_name):
        self.cues.append(cue(cue_ID, cue_name, self.ID, self.scene_ID))

    # The method to select a cue
    def select_cue(self, cue_ID):
        set_cue_select(self.scene_ID, self.ID, cue_ID)
        self.cues[self.selected_cue_ID].selected = False
        self.cues[cue_ID].selected = True
        self.selected_cue_ID = cue_ID

class scene:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        self.gain = 0
        self.panning_method = "ambi"
        self.room_effect = "off"
        self.room_size = 0.50 # communication and initiation?
        self.objects = [auditory_object(0, "Reserved Object", self.ID, self.panning_method, self.room_effect)]

    # Methods to change atributes and communicate changes to the dome
    # Play
    def play(self):
        play_scene(self.ID)

    # Stop
    def stop(self):
        stop_scene(self.ID)

    # The method to add objects to the scene
    def add_object(self, object_ID, obejct_name):
        self.objects.append(auditory_object(object_ID, obejct_name, self.ID, self.panning_method, self.room_effect))