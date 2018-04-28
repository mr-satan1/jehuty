# jehuty
Jehuty is a client/server framework for endpoint management. It is currently in pre-Alpha state.

## Capabilities
* Jehuty server runs on MacOS & Linux
* Jehuty client is currently compatible for MacOS, Linux and Windows.
* Jehuty server allows remote command execution to the Jehuty client under the users active permissions.
* Jehuty client has a persistence mechanism via user level Registry key for Windows.
* Jehuty server can spin up an on-demand HTTPS server in it's current directory to allow serving files to the Jehuty clients.

## Future Capabilities
* Adjust Jehuty server to scale out to at least 10 client endpoint connections.
* Add basic endpoint management commands, such as: shutdown, restart, run updates.

## Building Windows Client
To build the client, install PyInstaller. Then, execute:  "pyinstaller.py --noconsole JehutyClient.py". This will allow the PE to execute with no console window aka silently. 
