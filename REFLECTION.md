# Reflection: Make vs run_all.sh


#What does the Makefile make explicit that run_all.sh left implicit?
#	Think about: dependency relationships between files, which steps need to rerun when some- thing changes, and what a new collaborator learns by reading each file.

The Makefile makes explicit the dependency relationships between files that were implicit in run_all.sh. In the bash script, the execution order determined what ran, but there was no formal representation of which outputs depended on which inputs. The Makefile encodes these relationships declaratively, allowing Make to rebuild only what has changed. This improves efficiency, documentation, and collaboration because a new reader can immediately understand the project’s dependency structure by reading the Makefile.
