To Do (Guillaume Florent)
=========================

******** Create a dummy parts library to test instantiation of Part from library

Point .9 of Charles Scharman issues

Move the calculation of geometric signature to the Part object

Merge Part and Assembly

Anchor object

Notion de contact?

Reverse engineering -> rapprochement pièces catalogue?

Automatic relationships detection in reverse engineering

Graph links creation from STEP

Graph links creation from XML/JSON

Nested assemblies


To Do (list written by Charles Scharman)
========================================

1. Allow shells (and 2D curves?) in the boolean operations.

2. Allow shell returns from cylinder, sphere, box, wedge, cone, torus.

3. More robust error handling--usually shows a buried SWIG issue,
   which isn't helpful.

4. Enhance the options to various routines to more encompass OCC's
   capabilities.

5. Add parabola, hyperbola edges

6. Add edge intersection

7. I never got OCC's concept of orientation in 3d.  That caused a
   liberal use of .fix statements.  It would be nice to get this right.

8. Distinction between face, wire, solid, etc. can get muddled after
   certain operations.  Boolean can naturally do so.  Even a basic
   translate converts TopoDS_Vertex to TopoDS_Shape, for example.
   It's currently fixed by converting at the point where the specific
   type is needed.  May be better to correct immediately after the
   loose operation.  Ought to be more careful about this, or maybe
   should make a single class (shape) that is smart and handles all
   types.  That seems harder but is more python-like.

9. Separate compound, compsolid from solid.
