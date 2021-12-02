#!/usr/bin/env python3
import time
import googletrans
import json

#Setup
#This is a Python 3 script. You need to install the googletrans 
#package https://pypi.org/project/googletrans/ 
#At time of writing the current version has some issues, but 
#this one should work: pip install googletrans==4.0.0rc1

#Usage 
#Set cultures to unreal pacakge and google translate 
game_source_culture = "en"

#Destination culture as used in Unreal
game_dest_culture = "de"

#Destination culture as used by Google
#To find out which those are try print(googletrans.LANGUAGES)
translation_culture = "de"

#Path to folder where the .uproject file is in
unreal_project_path = "../../UnrealProject"

#Timeouts: Google translate will occasionally fail a translation but 
#also rate limit. If an exception occurs the script will retry to do 
#the translation, but wait a set time before sending another request
timeout_retries = 1
timeout_seconds = 30


#Script starts here, you shouldn't need to change below

#Filepath to the localization archive
archive_file_path = unreal_project_path+"/Content/Localization/Game/"+game_dest_culture+"/Game.archive"

translator = googletrans.Translator()
total_count = 1

def translate(source_string, culture, retries=1):
    try: 
        translation = translator.translate(source_string, src=game_source_culture, dest=culture)
        return translation.text
    except:
        print("Error Translating: \t"+source_string)
        if retries > 0:
            print("Retrying in 30s")
            time.sleep(timeout_seconds)
            return translate(source_string, culture, retries-1)
    
    return ""

def update_progress(count, step):
    new_count = count + step
    if new_count % 25 == 0:
        progress = int((new_count / total_count)*100)
        print("Progress: "+str(new_count)+"/"+str(total_count)+"\t"+str(progress)+"%")

    return new_count
    
#Read the archive file and parse it to json
with open(archive_file_path, 'r', encoding='utf16') as fh:
    data = json.load(fh)
    
#Count how many entries are in the archive
total_count = len(data['Children'])
for namespace in data['Subnamespaces']:
    total_count += len(namespace['Children'])

print("Items To Translate: "+str(total_count))

#Start translating one by one
index = 0
for item in data['Children']:
    item['Translation']['Text'] = translate(item['Source']['Text'], translation_culture, timeout_retries)
    index = update_progress(index, 1)        

#Translate sub namespaces
for namespace in data['Subnamespaces']:
    for item in namespace['Children']:
        item['Translation']['Text'] = translate(item['Source']['Text'], translation_culture, timeout_retries)
        index = update_progress(index, 1)        

#Save the translated archive
with open(archive_file_path, 'w', encoding='utf16') as fh:
    json.dump(data, fh, ensure_ascii=False, indent='\t')
    
