The goal of this project is to provide an annotation tool to build image databases for computer vision research.
In this example, we are landmarking critical points on images extracted from a recording of a chemical synthesis
that produces a melting zone.

Nonetheless, this tool can be generalized. The initial step is placing general points on all the images, approximatively
where they should be located (i.e, all corners and extremities of the waist). this step that can be disregarded based
on the type of annotations). Then, a GUI opens, and the user can drag the points where they should be. By pressing 'n',
the user can move to the next image, while pressing 's' will save the landmarked image and pressing 'a' will print the
coordinates. Each image is stored in a landmarkedimage object, which is appended to a list.

The purpose is to observe how the coordinates of the critical points vary as a result of a change of parameter,
which will then help understand how to make more successful syntheses using Machine Learning.

This implementation has a flaw, because when a image is annotated then saved, stopping the program and reopening it again
will show the previous landmarks on the image, without trace of them stored anywhere. That is because a real time database
is required, and the issue could be solved by adding an boolean attribute to the landmarked image object, in order to
know whether or not to refer to the dictionary that is stored (in which case you can read the dictionary and extract
the coordinates).
