# MADNESS (Matt's Application Dashboard, Necessary to Ensure Successful Sequencing)
Django-isation of refseq program, uses conda package refseq


This is a web-platform port of the reference sequence generator application, available in another repository. This uses a Django framework to allow a user to upload files, runs the reference conversion in the background, and then provides links to each reference to download the final PDF

The app currently features no login-control, and has not been designed with security in mind, as it is to be locally available to users within the trust network only. 

The repo contains a req.txt requirements file, built using conda. Build a new environment for this project using $ conda create -n new environment --file req.txt
