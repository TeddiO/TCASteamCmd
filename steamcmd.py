import sys, time, re, os, shlex, subprocess

#TCAdmin SteamCMD middleman. Designed really to sit between TCAdmin and SteamCMD after the update when TCA could no longer interface with SteamCMD (in service mode).
#With modification you can also do any pre-processing before updating the server.
#This is console / service mode agnostic and will just work.

print("Please wait while we update your server!")
print("Preparing update...")
filePath = ""

### NOTE THE QUOTES AROUND +force_install_dir. This is basically required because why not!
### For whatever reason passing a string in raw format causes it to have issues. Nor can we pipe out sadly. 
basicInputString = './steamcmd/steamcmd.exe +@ShutdownOnFailedCommand 0 +@NoPromptForPassword 1 +login anonymous "+force_install_dir {0}" +app_update {1} validate +quit'

for arg in sys.argv:
	testString = re.search("^(.+)\.steamcmd$", arg)

	if testString:
		filePath = './' + testString.group(1) + '.steamcmd'

		testFile = os.path.isfile(filePath)
		if not testFile:
			print("An error occurred getting update details.")
			quit()

		infoFile = open(filePath, "r",  encoding='utf-8')
		fileContents = infoFile.read()
		infoFile.close()

		dirLocation = re.findall('force_install_dir "([^"]*)"', fileContents)
		if dirLocation:
			directoryLocation = os.path.abspath(dirLocation[0])
		else:
			print("An error occurred getting update details. (Err 2)")
			quit()

		appLocation = re.search('app_update (.+) validate', fileContents)
		if appLocation:
			appID = appLocation.group(1)
			print("Application ID is: ", appID)
		else:
			print("An error occurred getting update details. (Err 3)")
			quit()

		print("Preparations complete. Now attempting to update server...")

		outputString = basicInputString.format(directoryLocation, appID)

		process = subprocess.Popen(shlex.split(outputString), stderr = subprocess.PIPE)

		while True:
			output = process.stdout.readline()
			
			if output == '' and process.poll() is not None:
				break
			if output:
				print(output.strip())
				pass
			pass
	
		break

#Presuming the update all goes well, TCAdmin will automatically notice the termination of this application and will notify the user the update is complete. 