<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Sync Folders - README</title>
</head>
<body>
  <h1>Sync Folders - README</h1>
  <p>This project consists of a script that synchronizes two folders. There is a script named sync_folders.py which synchronizes the source folder with the replica folder. The script can be run by passing command-line arguments such as source folder path, replica folder path, synchronization interval and log file path.</p>
  <h2>Dependencies</h2>
  <p>The project uses the following dependencies:</p>
  <ul>
    <li>schedule</li>
  </ul>
  <p>To install these dependencies, run:</p>
  <code>pipenv shell</code>
  <p> Then run: </p>
  <code>pipenv install</code>
  <h2>How to run the script</h2>
  <p>Make sure you execute the sync_folder.py script from the source directory (src). </p>
  <p>To run the script, execute the following command in your terminal:</p>
  <code>python sync_folders.py --source path/to/source --replica path/to/replica --interval INTEGER --log path/to/logfile</code>
  <ul>
    <li><code>--source</code>: Path to the source folder.</li>
    <li><code>--replica</code>: Path to the replica folder.</li>
    <li><code>--interval</code>: Synchronization interval in seconds.</li>
    <li><code>--log</code>: Path to the log file.</li>
  </ul>
  <h2>Project Structure</h2>
   <ul>
    <li>sync_folders.py: The main script which implements the folder synchronization logic.</li>
    <li>sync.py: A module that contains the Sync class which has methods for the folder synchronization.</li>
    <li>classes/file.py: A module that contains the File class which has methods for calculating the hash of a file.</li>
    <li>folder_logger.py: A module that contains a function for logging the events that occur during synchronization.</li>  
  </ul>
  <h2>Synchronization Logic</h2>
  <ul>
    <li>The script first verifies that both source and replica folders exist..</li>
    <li>If the replica folder is empty, the script copies all files from the source folder to the replica folder.</li>
    <li>If the replica folder is not empty, the script calculates the hash of each file in both the source folder and the replica folder.</li>
    <li>If a file exists in the source folder but not in the replica folder, the script copies it to the replica folder.</li>  
    <li>The script logs all the events that occur during synchronization in the log file.</li>

  </ul>
</body>
</html>
