import json
import csv
import pandas as pd
import os
import dropbox
import subprocess

def download_dropbox(token: str, local_folder: str, cloud_path: str, file_type: str = ""):
    def get_folders_id(dbx, folder):
        result = dbx.files_list_folder(folder, recursive=True)
        
        folders={}
        
        def process_dirs(entries):
            for entry in entries:
                if isinstance(entry, dropbox.files.FolderMetadata):
                    folders.update({entry.path_lower: entry.id})
        
        process_dirs(result.entries)
                
        while result.has_more:
            result = dbx.files_list_folder_continue(result.cursor)
            process_dirs(result.entries)
            
        return(folders)

    def get_files(dbx, folder_id, local_folder):
        result = dbx.files_list_folder(folder_id, recursive=True)
        files_paths = []
        folders_paths = []

        for val in result.entries:
            txt = val.path_display
            if "." in txt:
                files_paths.append(txt)
            else:
                folders_paths.append(txt)

        for folder in folders_paths:
            if not(os.path.isdir(local_folder + folder)):
                os.mkdir(local_folder + folder)

        for file in files_paths:
            if file_type in file:
                dbx.files_download_to_file(local_folder + file, file, None)
        
        return [x for x in files_paths]

    dbx = dropbox.Dropbox(token)
    folder_id = get_folders_id(dbx, cloud_path)[cloud_path]

    paths = get_files(dbx, folder_id, local_folder)
    
    cloud_files_path = [local_folder + k for k in paths if file_type in k]

    return cloud_files_path

def export_data(filetype: str):
    token = 'KjuflX1NCx4AAAAAAAAAAZC_0k_v9uPmWOQgRbWiuT1vaQBL8f7Zmmr38MQgCvk0'
    path = "files/"
    if not(os.path.isdir(path)):
        os.makedirs(path)

        if os.name != "nt":
            subprocess.call(['find', path, '-type', 'd', '-exec', 'chmod', '755', '{}', '+'])

    return download_dropbox(token, path, "/cochesnet", filetype)
