# forward2
forward2 is a bash script to submit from your local machine a batch job to a slurm managed remote cluster and port forwards it back to your local machine.
Useful for jupyter notebook and tensorboard, amongst other things.

This repository was inpired by https://github.com/vsoch/forward.


## forward2 usage
```
forward2 [-u user] [-r resource] sbatchfile [path]
sbatchfile      sbatch script to submit
path            running path (default home path)
-u, --user      username
-r, --resource  cluster name (g100,marconi,leonardo,dgx)
-p, --port      port number
-h, --help      print this help
```

Optionally, `user`, `resource`, and `port` can be defined in a `params.sh` file located in the `resource` folder or in the current directory.
If even the file is not found, the script asks the values and save them in `params.sh`.
By default the batch script creates a `forward-util` directory in your cluster home where to copy the batch script and save the batch ouptut.
THis default can be changed by setting `RESOURCE_HOME` in the `params.sh` file.

### set up ssh keys
```
1. generate the RSA keys pairs on your local computer:
ssh-keygen
2. copy the public key to your resource home:
ssh-copy-id uesername@login.resource.cineca.it
3. connect to resource and repeat 1 and 2
ssh uesername@login.resource.cineca.it
ssh-keygen
ssh-copy-id localhost
```

### usage example
```
1. ./forward2 -u marco -r marconi -p 47703 jupyter-conda /marconi_work/<project_name>
2. ./forward2 jupyter-conda -r marconi
3. ./forward2 jupyter-conda /marconi_work/<project_name>
4. ./forward2 -r g100 jupyter-conda
5. ./forward2 -r dgx jupyter
```
The script will output the different steps, and finally the instruction to connect, look for logs and end:
```
== Instructions ==
1. Open a browser at: http://localhost:47703/?token=5cffb394db829a61bf8d9df95def61125c411a5ee7341ed6
2. Something went wrong? Look at logs (see instruction above)
3. Use Control-C to end, cancel job and kill tunnels (twice to skip confirmation).
```

### add new batch scripts
New batch scripts can be added in the folder corresponding to the cluster name. 
Since the bash script waits for a token, if this is not written by your application, 
you must add `echo "?token=" >&2` to your batch script, like in the tensorboard example.  



