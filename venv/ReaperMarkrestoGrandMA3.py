import csv
import xml.etree.ElementTree as ET
import uuid
from xml.dom import minidom
import os


def generate_guid():
    """Generate a random GUID in the format required by MA3 (spaces between bytes)."""
    return ' '.join(format(x, '02X') for x in uuid.uuid4().bytes)  # Format as hex and join with spaces


# Function to read CSV file and parse marker data
def read_marker_file(filename):
    markers = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            markers.append({'name': row['Name'], 'time': row['Start']})
    return markers


def create_ma3_timecode_xml(markers, sequence_number, output_filename):
    root = ET.Element("GMA3", DataVersion="1.4.0.2")

    # Generate GUIDs for Timecode and TrackGroup
    timecode_guid = generate_guid()
    track_group_guid = timecode_guid

    # Create Timecode element
    timecode = ET.SubElement(
        root, "Timecode",
        Name=os.path.splitext(os.path.basename(output_filename))[0],  # Use the CSV filename as the Timecode name
        Guid=timecode_guid,
        Duration=str(float(markers[-1]['time']) + 1),  # Set duration to the last marker time + some offset
        LoopCount="0",
        TCSlot="0",
        AutoStop="No",
        SwitchOff="Keep Playbacks",
        TimeDisplayFormat="Default",
        FrameReadout="Default"
    )

    # Add TrackGroup element with the same GUID
    track_group = ET.SubElement(timecode, "TrackGroup", Play="", Rec="")

    # Add MarkerTrack element with a new GUID
    marker_track_guid = timecode_guid
    marker_track = ET.SubElement(
        track_group, "MarkerTrack",
        Name="Marker",
        Guid=marker_track_guid
    )

    # Add Track element with attributes pointing to a target sequence
    track_guid = marker_track_guid
    track = ET.SubElement(
        track_group, "Track",
        Guid=track_guid,
        Target=f"ShowData.DataPools.Default.Sequences.{sequence_number-1}",
        Play="",
        Rec=""
    )

    # Add TimeRange element inside the Track with a new GUID
    time_range_guid = marker_track_guid
    time_range = ET.SubElement(
        track, "TimeRange",
        Guid=time_range_guid,
        Duration="To End",
        Play="",
        Rec=""
    )

    # Add CmdSubTrack element
    cmd_sub_track = ET.SubElement(time_range, "CmdSubTrack")

    # Add CmdEvent elements for each marker
    for i, marker in enumerate(markers):
        cue_number = 1000 + (i * 1000)  # Generates 1000, 2000, 3000, ...

        # Adjusted object sequence number
        adjusted_sequence = sequence_number - 1

        cmd_event = ET.SubElement(
            cmd_sub_track, "CmdEvent",
            Name="Goto",
            Time=marker['time'],
            CueDestination=marker['name'],
        )

        # Add RealtimeCmd with adjusted sequence number for the Object
        realtime_cmd = ET.SubElement(
            cmd_event, "RealtimeCmd",
            Type="Key",
            Source="Original",
            UserProfile="0",
            User="1",
            Status="On",
            IsRealtime="0",
            IsXFade="0",
            IgnoreFollow="0",
            IgnoreCommand="0",
            Assert="0",
            IgnoreNetwork="0",
            FromTriggerNode="0",
            IgnoreExecTime="0",
            IssuedByTimecode="0",
            FromLocalHardwareFader="1",
            IgnoreExecXFade="0",
            IsExecXFade="0",
            Object=f"12.12.0.5.{adjusted_sequence}",
            ExecToken="Goto",
            ValCueDestination=f"12.12.0.5.{adjusted_sequence}.{cue_number}"
        )

    # Write the XML to a file
    tree = ET.ElementTree(root)

    # Pretty print the XML with encoding
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    xml_str = xml_str.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>')  # Add encoding

    with open(output_filename, "w") as f:
        f.write(xml_str)


# Create XML structure using marker data for macro
def create_ma3_macro_xml(markers, sequence_number, output_filename):
    root = ET.Element("GMA3", DataVersion="1.4.0.2")

    macro = ET.SubElement(
        root, "Macro",
        Name=f"Macro {os.path.splitext(os.path.basename(output_filename))[0]}",
        Guid=generate_guid()
    )

    # Command to store sequence and cues
    macro_line_store = ET.SubElement(
        macro, "MacroLine",
        Command=f"Store Sequence {sequence_number} Cue 1 thru {len(markers)}",
        Wait="0.10"
    )

    # Create MacroLine elements for each marker
    for i, marker in enumerate(markers):
        macro_line_label = ET.SubElement(
            macro, "MacroLine",
            Command=f'Label Sequence {sequence_number} Cue {i + 1} "{marker["name"]}"',  # Use normal quotes
            Wait="0.10"
        )

    # Write the XML to a file
    tree = ET.ElementTree(root)

    # Pretty print the XML
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    with open(output_filename, "w") as f:
        f.write(xml_str)


if __name__ == "__main__":
    # Prompt for input CSV file path
    input_filename = input("Please enter the path to the CSV file: ")
    markers = read_marker_file(input_filename)

    # Get the sequence number from the user
    sequence_number = int(input("Enter the sequence number: "))  # Convert input to int

    # Ask if output should be in the same folder
    output_same_folder = input("Output to the same folder? (Y/N): ").strip().upper()
    if output_same_folder == 'Y':
        output_folder = os.path.dirname(input_filename)
    else:
        output_folder = input("Please enter a valid directory for output files: ")
        while not os.path.isdir(output_folder):
            print("Invalid directory. Please try again.")
            output_folder = input("Please enter a valid directory for output files: ")

    # Create filenames based on the CSV filename
    base_filename = os.path.splitext(os.path.basename(input_filename))[0]
    output_timecode_filename = os.path.join(output_folder, f"{base_filename}_timecode.xml")
    output_macro_filename = os.path.join(output_folder, f"{base_filename}_macro.xml")

    # Create timecode and macro XML files
    create_ma3_timecode_xml(markers, sequence_number, output_timecode_filename)
    create_ma3_macro_xml(markers, sequence_number, output_macro_filename)

    print(f"XML files '{output_timecode_filename}' and '{output_macro_filename}' created successfully.")
