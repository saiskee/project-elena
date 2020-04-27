# !/bin/sh
wget https://www.dropbox.com/s/fgxt8y9eegkyqs7/cached_graphs.zip

unzip cached_graphs.zip

mv massachusetts_bike.pkl massachusetts_drive.pkl massachusetts_walk.pkl backend/src/data