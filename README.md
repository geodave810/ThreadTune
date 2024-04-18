# ThreadTune
Fine-Tune your Screw Thread Designs in Autodesk Fusion 360

This started out to be just a way to be able to give more adjustable threads by varying the Diameter, Pitch Height and Angle like I can easily do using openSCAD.  This gave me a lot of flexibility with tolerance fit between male & female threads.  The formula for the thread profile is pretty simple to generate a single profile.  I used this page for reference.
https://en.wikipedia.org/wiki/ISO_metric_screw_thread

Here is a forum discussion I started on this idea & shows most of my thoughts along the way.  I won't repeat a lot of the info from there.
https://forum.v1e.com/t/drawing-more-flexible-screw-threads-in-fusion-360/43352

You can create threads with most any angle as well as using different angles for the top thread & bottom thread.  If your combined top & bottom angle are too large, the code will fail.  using a 30 & 60 will work, but using a 60 & 60 will fail.  If you set either or both angles to 0, it will give you a flat thread on the top, bottom or both.  You can also enter a negative number for the thread angle which will invert the thread.  I did see a YouTube video where the inverted style was actually used.  You can also do a Right or Left hand thread.

How this works is that it draws a profile of the thread.  Then it draws a helix for the path of that thread profile following the inside edge of that profile & either another helix along the outside radius of that profile for the guide rail or a vertical Centerline.  The more spline points you use the more accurate the thread will be for the full length of the thread.  Interestingly enough, I can use 18 spline points with the outside helix as the guide rail & get about the same accuracy using 45 spline points with the vertical centerline guide rail.  I have the default currently set to Centerline Guide rail & 36 spline points.  Another gotcha, is if you use a different angle for the top & bottom other than 0, it will fail when using the outside helix for the guide rail.

This program is setup as an Add-In in Autodesk Fusion 360.  To install this, copy the file structure to:
C:\Users\<UserName>\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns
After you copied the files, your folder structure should look like this.<br>
![ThreadTune Folder](ThreadTuneFolder.JPG)<br>
To run the program, click on Utilites, then ADD-INS, then Add-Ins tab.  You should see the program ThreadTune in the list under **My Add-Ins**
Click on the program & you should see a thread icon in the ADD-INS panel.  To run the program, just click on that thread icon.

The most commone use of this program for me anyway is to have a different diameter for the Male threads & the Female threads in order to get a good tolerance in 3D prints.  For example, using 6mm diameter threads with a pitch of 1 & angle of 30, then a 5.5mm diameter threads with same parameters you will get a tolerance of 0.25mm all the way around the vertical part of the threads, but a little less around the angled part of the threads.<br>
![ThreadTune Dialogbox](ThreadTuneDialog.JPG)<br>
Using the Helex guide rail instead of the vertical centerline will require less points for the spline points to be accurate.  18 - 36 spline points is usually sufficent with the Helix guiderail, but you will need at least 36-45 spline points when using the vertical centerline for it to be accurate.  Using a different angle for the top & bottom of the thread you will need to use the vertical centerline for it to work.  The exception here is using 0 for the top and/or bottom angle either type of guide rail will work.<br>
![ThreadTune Types](Thread_Types_800x600.jpg)<br>

This program draws the thread at 0,0,0 and only draws the threads.  I draw the inner circle for the threads, but it is not extruded.  I was not able to get that to work just yet.
