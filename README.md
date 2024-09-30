Hi, so following https://www.youtube.com/watch?v=Gu_CuGmEe3A&t=556s&ab_channel=fiets.de tutorial led to an issue using GrandMA3 2.0.0.2
So I created a python code that generates two files:
1. a macro file
2. a timecode file

How to make it work?
(I am a Mac user but the diffrences are not big)
1. After creating the markers on the Reaper software and exporting them, you will find an csv file
2. When running the python code you will be asked to enter the path of that file
3. You will be asked where do you want the export to happen - you can chose the same folder by Y
or chosing another folder by entering N and then the desired path name
4. Puth the files in the correct location - /Users/USERNAME/MALightingTechnology/gma3_library/datapools/macros/ for the macro file
   and /Users/USERNAME/MALightingTechnology/gma3_library/datapools/timecodes/ for the timecode file 
4. after you have the two files in those location - you will need to import them on the GrandMA3 software:
   a. go to Menu->Show Creator->Import->Macros and then chose the correct macro
   b. go to Menu->Show Creator->Import->Timecodes and then chose the correct timecode
5. then press the macro - that will generate the new sequence 

for further steps on how to sync Reaper and Grandma3 I recommend watching:
https://www.youtube.com/watch?v=vcQuV80J9UU&t=184s&ab_channel=JSDennison
