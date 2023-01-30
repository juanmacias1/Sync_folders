import os
import sys
import shutil
import filecmp
from classes.file import File
from folder_logger import logger

class Sync:
    def __init__(self, source_folder, replica_folder, log_file):
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.log_file = log_file
    
    def run(self):
        if self.verification():    
            # If the source folder is empty, all the files in the replica folder will be deleted
            if (not os.listdir(self.source_folder)):
                os.system("rm -rf {0}/*".format(self.replica_folder)) 
            # If the replica folder is empty all the files from source will be copied
            elif (not os.listdir(self.replica_folder)):
                logger(self.log_file, "[Message] No files on replica folder. Copying...")
                os.system("cp -r {0}/* {1}".format(self.source_folder, self.replica_folder))
                succesfull_copy = filecmp.dircmp(self.source_folder, self.replica_folder)
                if succesfull_copy.same_files:
                    logger(self.log_file, "[Synchronized] The files in both directories are identical.")

                else:
                    logger(self.log_file, "[Error] The files in both directories are NOT identical.")
            #If the replica folder and the source folder are not empty
            else:
                list_source_hashes = []
                list_replica_hashes = []
                for source_dirpath, source_dirnames, source_filenames in os.walk(self.source_folder):
                    for source_filename in source_filenames: 
                        source_file_path = os.path.join(source_dirpath, source_filename)
                        my_source_file = File(source_file_path)               
                        hash_source_file = my_source_file.calculate_hash()
                        list_source_hashes.append(hash_source_file)
                        for replica_dirpath, replica_dirnames, replica_filenames in os.walk(self.replica_folder):
                            for replica_filename in replica_filenames:
                                replica_file_path = os.path.join(replica_dirpath, replica_filename)
                                my_replica_file = File(replica_file_path)
                                list_replica_hashes.append(my_replica_file.calculate_hash())        
                
                        # If a file on source, does not exists in the replica folder is copied (even if its inside a subdirectory).
                        if hash_source_file not in list_replica_hashes:
                            logger(self.log_file, "[Warn] There is a file that does not exist in the replica folder.")
                            # Get the source and replica folder names
                            source_folder_name = self.source_folder.split("/")[-1]
                            replica_folder_name = self.replica_folder.split("/")[-1]                            
                            # Split the source_dirpath in parts                            
                            source_path_parts = os.path.normpath(source_dirpath).split(os.sep)
                            # Replace "source folder name" with "replica folder name" in the path
                            source_path_parts[source_path_parts.index(source_folder_name)] = replica_folder_name                           
                            # Join the path parts to create the destination path
                            destination_dir = os.sep.join(source_path_parts)
     
                            #Create destination directory if not created
                            os.makedirs(destination_dir, exist_ok=True)
                            #Copy source file in the replica directory
                            my_source_file.copy_file(destination_dir)
                            logger(self.log_file, "[Message] The file '{0}' was succesfully copied to {1}".format(source_filename, destination_dir))
                    
                        #Final list of hashes from files in the replica folder
                        list_replica_hashes_2 = list_replica_hashes
                        list_replica_hashes = []    
                #If all hashes in the list are the same the files are synced
                if self.compare_lists(list_replica_hashes_2, list_source_hashes):
                    logger(self.log_file, "[Synchronized] The files in both directories are identical.")
                #If a file is on the replica but not on the source folder, its deleted
                elif len(list_replica_hashes_2) > len(list_source_hashes):
                    logger(self.log_file, "[Warn] There is a file that does not exist in the source folder.")
                    diff = set(list_replica_hashes_2).difference(list_source_hashes)
                    for file_hash in diff:
                        for replica_dirpath, replica_dirnames, replica_filenames in os.walk(self.replica_folder):
                            for replica_filename in replica_filenames:
                                replica_file_path = os.path.join(replica_dirpath, replica_filename)
                                my_replica_file = File(replica_file_path)
                                if my_replica_file.calculate_hash() == file_hash:
                                    os.remove(replica_file_path)
                                    logger(self.log_file, "[Message] File: {0} deleted from replica".format(replica_filename))

                    # Get a list of all directories in the source folder
                    source_dirs = [d for d in os.listdir(self.source_folder) if os.path.isdir(os.path.join(self.source_folder, d))]
                    # Get a list of all directories in the replica folder
                    replica_dirs = [d for d in os.listdir(self.replica_folder) if os.path.isdir(os.path.join(self.replica_folder, d))]
                    # Find the directories that are in the replica folder but not in the source folder
                    dirs_to_delete = set(replica_dirs) - set(source_dirs)
                    # Delete the directories that are in the replica folder but not in the source folder
                    for dir_to_delete in dirs_to_delete:
                        shutil.rmtree(os.path.join(self.replica_folder, dir_to_delete))
                        logger(self.log_file, "[Message] Directory: {0} deleted from replica".format(os.path.join(self.replica_folder, dir_to_delete)))
             
                # Initialize       
                list_source_hashes = []
        else:
            sys.exit(1)

    #Function to verify if synchronization can be executed
    def verification(self):

        #Condition to ensure source and replica folders are different
        if self.source_folder == self.replica_folder:
            logger(self.log_file, "[Error] Source and replica cannot be the same folder")
            return False
    
        #Verify if specified folders exist
        if not os.path.exists(self.source_folder) or not os.path.exists(self.replica_folder):
            logger(self.log_file, "[Error] Either of the provided paths does not exist. Please provide an existing path.")
            return False

        #Condition to ensure folders are not contained between each other
        if os.path.commonprefix([self.source_folder, self.replica_folder]) in (self.source_folder, self.replica_folder):
            logger(self.log_file, "[Error] Source and replica cannot be inside of each other")
            return False

        #Ensure the log file exist
        if not os.path.exists(self.log_file):
            logger(self.log_file, "[Error] The specified log file path does not exist")
            return False

        return True

    # Function to verify if two lists contain exactly the same elements
    def compare_lists(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return False
        return True
