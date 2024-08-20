# TimeSyncInitial

The time client1 file is the start of Cristians algorithm and sends initial time from the client machines. Time server2 is the server's file and records all the times. Time client2 file is on the client machine but is a server type file that records all the results from server 2 and outputs the final times. No times currently are changed in the machine itself. 

The time search algorithms are designed for searching for other machines and recording transmission times. The first search file sends the messages. The second is a server on each of the other machines (also is run on host machine) and will take the initial information and send back time and proper header. The last search file records all the results asynchronously and stores them on files. All the search files are similar to the client-server files of the previous section.
