Primero hay que levantar el controlador pasandole el archivo del firewall custom que queremos usar 
con el comando <br> `$ python3.9 ./pox.py forwarding.l2_learning firewall`.

Luego en otra terminal levantamos mininet con la topología deseada e indicandole que use el 
controlador remoto levantado previamente <br> `$ sudo mn –custom topo-linear2.py –topo mytopo –controller=remote`.

Hay que indicarle al script la cantidad de switches que se desean usar.
