# ue-googletranslate-localization
A lazy way to hack bad localization into your unreal project.

Disclaimer: Obviously using Google Translate output for packaging is a bad idea, I mainly did this to quickly generate test data to check how well UI designs and Fonts are holding up. 

This script uses json parsing to read Unreal's game archives and then churns them through google translate thanks to the googletrans python package: https://pypi.org/project/googletrans/

To get it working you need to first configure locales in Unreal and run a text gather. Then you can run the script and do a text compile and count in Unreal afterwards. 

