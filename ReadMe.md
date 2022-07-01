### Instrucciones para correr el controlador pox y mininet:

1) Levantar el controlador indicando el archivo del firewall custom que queremos usar 
con el comando <br> `$ python3.9 <path_to_pox_folder>/pox.py forwarding.l2_learning firewall`.

Nota: tanto el archivo `firewall.py` como `config.json` deben ser copiados y pegados en la carpeta `<path_to_pox_folder>/pox/ext`.

2) Luego en otra terminal levantamos mininet con la topología deseada e indicandole que use el 
controlador remoto levantado previamente <br> `$ sudo mn --custom tp3-topo.py --topo TP3topo --controller=remote`.

Hay que indicarle al script la cantidad de switches que se desean usar. Para ello, se pedirá al usuario que ingrese el número por teclado.

### Comandos para probar las reglas

1) Para probar la primera regla, utilizamos `iperf` para levantar un server escuchando en el puerto 80 y luego también con `iperf` hacemos que otro host haga las veces de cliente y le envíe paquetes al host server:  

`$ h2 iperf -s -p 80 -D`  
`$ h3 iperf -c 10.0.0.2 -p 80`

Nota: para probar con paquetes UDP, se puede agregar la opción `-u` en ambos comandos.

2) Para la segunda regla, podemos utilizar comandos parecidos a los de la primera, solo que en este caso, el host cliente solo puede ser h1:

`$ h4 iperf -s -u -p 5001 -D`  
`$ h1 iperf -c 10.0.0.2 -p 5001 -u`

3) Para probar la tercera regla, primero tenemos que revisar el archivo de configuracion `config.json` para saber cuáles son los hosts que no se van a poder comunicar entre si. Luego, podemos ejecutar los siguientes comandos para probar:  

`$ h2 iperf -s -u -p 8080 -D`  
`$ h1 iperf -c 10.0.0.2 -p 8080 -u`

y en el otro sentido

`$ h1 iperf -s -p 8080 -D`  
`$ h2 iperf -c 10.0.0.1 -p 8080`

Nota: para probar con paquetes UDP, se puede agregar la opción `-u` en ambos comandos.


