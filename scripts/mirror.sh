#!/bin/sh
cd ~/openApiSamples/$1
git svn rebase
git push origin master
