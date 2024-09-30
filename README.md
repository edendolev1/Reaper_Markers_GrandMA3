# Reaper Markers to GrandMA3 Timecode & Macro Generator

Hi! After following this [YouTube tutorial](https://www.youtube.com/watch?v=Gu_CuGmEe3A&t=556s&ab_channel=fiets.de), I encountered an issue using GrandMA3 version 2.0.0.2. To solve this, I created a Python script that generates two files:
1. A macro file
2. A timecode file

## How to Make It Work

> *Note: I am a Mac user, but the differences for other operating systems are minimal.*

### Steps:

1. **Create Markers in Reaper and Export as CSV**  
   After creating markers on the Reaper software and exporting them, you will obtain a `.csv` file.

2. **Run the Python Code**  
   When running the Python script, you will be prompted to enter the path of the `.csv` file.

3. **Choose Export Location**  
   You will be asked where to export the files:
   - Choose the same folder by typing `Y`
   - Choose a different folder by typing `N`, then enter the desired path

4. **Place the Files in the Correct Location**  
   - Put the macro file in:  
     `/Users/USERNAME/MALightingTechnology/gma3_library/datapools/macros/`
   - Put the timecode file in:  
     `/Users/USERNAME/MALightingTechnology/gma3_library/datapools/timecodes/`

5. **Import the Files into GrandMA3**  
   - Go to **Menu -> Show Creator -> Import -> Macros**, and choose the correct macro.
   - Go to **Menu -> Show Creator -> Import -> Timecodes**, and choose the correct timecode.

6. **Generate the New Sequence**  
   Press the macro to generate the new sequence.

### Further Steps

For additional steps on how to sync Reaper and GrandMA3, I recommend watching this [YouTube tutorial](https://www.youtube.com/watch?v=vcQuV80J9UU&t=184s&ab_channel=JSDennison).
