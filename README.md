<h1 align="center"> MQTT con Adafruit </h1>

</p>
<p align="center">
<img src ="./media/test.gif" alt="gif_labels" width="700"/>
</p>

En este repositorio se puede encontrar un [ejemplo oficial de Adafruit](https://github.com/adafruit/Adafruit_IO_Python/tree/master/examples/mqtt) modificado para hacer una integración con una Raspberry Pi.
</p>

### ***Instalación Adaruit***

Para instalar Adafruit se realiza:

	pip3 install adafruit-io

---
### ***Ejecución del código***

Para que el código funcione correctamente se debe modificar el nombre de usuario y la clave asignada, adicional en la sección <em>feeds</em> se deben crear <em>led</em> y <em>temperatura</em>, si se desea se puede crear un <em>dashboard</em> para poder observar los datos con los gráficos que se deseen.

	python3 mqtt.py

En la RaspberryPi se usó un sensor DS18B20 (one-wire) y un led en el pin BCM 17. 

---
## **Desarrollado por:**

✈️ Andrea Juliana Ruiz Gómez, [GitHub](https://github.com/andrearuizg), Email: andrea_ruiz@javeriana.edu.co
