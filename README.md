## Análisis de la distribución geográfica de polimorfismos de CYP2D6 como predictores de reacciones adversas en el tratamiento de la depresión.  `Dash` 

De acuerdo con cifras de la Organización Mundial de la Salud (OMS), las disfunciones cognitivas y neuropsiquiátricas afectan a alrededor de 450 millones de personas en el mundo [1], siendo la depresión la enfermedad con mayor incidencia además, la OMS estima que para 2040 la depresión es será la primera causa más común de discapacidad generando perdidas económicas importantes. Por esta razón la necesidad de disminuir esta y otras afecciones de salud mental. Para este fin existe tratamientos eficaces para la depresión moderada y grave sin embargo, los pacientes con desórdenes neuropsiquiátricos pueden consumir entre 6 a 10 fármacos al día [2] con el consiguiente riesgo de interacciones farmacológicas no deseadas y efectos adversos, pues aproximadamente el 90% de los fármacos empleados como tratamiento son susceptibles de variaciones farmacocinéticas asociadas a polimorfismos en el gen CYP2D6 que codifica enzimas encargadas de descomponer los medicamentos empleados como antidepresivos [3]. De acuerdo con la cantidad de actividad que presenta esta enzima se pueden clasificar cuatro fenotipos con diferente respuesta biológica a estos fármacos. A continuación se muestra un resumen de los cuatro fenotipos asociados a la expresión de CYP2D6 por regiones geográficas así como información útil que puede ayudar en consideraciones terapéuticas y ajustes de dosis.

Para realizar este mapa empleamos los fenotipos de CYP2D6 como biomarcadores de riesgo a falla terapéutica o reacciones adversas a fármacos antidepresivos en diferentes poblaciones, utilizando los datos del Proyecto de los 1000 genomas [4] organizados en la base de conocimientos de farmacogenómica (PharmGKB)[5]

#Datos 
Los datos se encuentran disponible en la carpeta `data` puede encontrar los datos limpios en el archivo `DATA_CYP2D6.geojson`, o en la carpeta `Notebooks` en el archivo  `20210701.py` que contienen el proceso de limpieza y acomodo de los datos originales. 

## Configuración
Ejecutar el archivo, primero cree un ambiente virtual que incluya todas las dependencias y paquetes del archivo, para este fin, ejecute el archivo `./confi` el cual crea un ambiente virtual y descargar las librerías listadas en `requirements.txt`. 
linea: (Despues de haber ejecutado `./confi`.-)
```
$ ./confi
```
Para activar el ambiente en este directorio, ejecute la siguiente linea: (Después de haber ejecutado `./confi`.-)
```
$ source venv/bin/activate
```
## Ejecutar la visualización
Para ejecutar la visualización puede ejecutar el siguiente archivo de Python: 
```
$python3 app.py
```

##Previsualización

Vista inicial del dashboard:
![](./images/Visualizacion_completa.png)
En esta área se encuentra una breve introducción del tema. 

Visualización por fenotipo:
Para observar la distribución de cada fenotipo de acuerdo con la región, navegue  a la ventana *Fenotipos* y del botón despegable seleccione el fenotipo que desee visualizar. 
![](./images/Fenotipos.png)
![](./images/Fenotipos_2.png)

Efectos adversos:
Para obtener información sobre los efectos adversos, navegue a la ventana *Efectos adversos* y visualice la información. 
![](./images/Efectosadversos.png)

Ligas para obtener más información:
Para obtener las referencias, navegue hasta la ventana *Más información*, aquí encontrará información adicional y ligas que redirigen a recursos externos como guías farmacológicas.
![](./images/Mas_informacion.png)


## Recursos 

Para saber más de Dash [Dash](https://plot.ly/dash).

Esta aplicación fue desarrollada como parte de un proyecto en el programa 'Health Data SCience Program (HDS-Program) por [Anny Olivares Mundo](https://www.linkedin.com/in/anny-olivares-mundo-84261a201?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BJzXidXO%2BSweC88UtZ9zvJg%3D%3D) y [Nidia Samara Rodríguez Rivera](https://www.linkedin.com/in/nidia-rodr%C3%ADguez-rivera-60a03948/)' 

Los datos para esta aplicación fueron tomados de [Gene-specific Information Tables for cytochrome P450 2D6 (CYP2D6)](https://www.pharmgkb.org/page/cyp2d6RefMaterials) [1]

El manuscrito con información más completa puede localizarlo en la siguiente liga de GoogleDocs 'https://drive.google.com/file/d/1cCTt24htDxX25qvn7KculZTsBzxso5f2/view?usp=sharing'

[1] M. Whirl-Carrillo, E.M. McDonagh, J. M. Hebert, L. Gong, K. Sangkuhl, C.F. Thorn, R.B. Altman and T.E. Klein. "Pharmacogenomics Knowledge for Personalized Medicine" Clinical Pharmacology & Therapeutics (2012) 92(4): 414-417.

Para saber mas de Dash [Dash](https://plot.ly/dash).

Esta aplicación fue desarrollada como parte de uhn proyecto en el prorama 'Health Data SCience Program (HDS-Program) por [Anny Olivares Mundo](https://www.linkedin.com/in/anny-olivares-mundo-84261a201?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BJzXidXO%2BSweC88UtZ9zvJg%3D%3D) y [Nidia Samara Rodríguez Rivera](https://www.linkedin.com/in/nidia-rodr%C3%ADguez-rivera-60a03948/)' 

Los datos para esta aplicación fueron tomados de [Gene-specific Information Tables for cytochrome P450 2D6 (CYP2D6)](https://www.pharmgkb.org/page/cyp2d6RefMaterials) [1]

El manuscrito con información más completa puede localizarlo en la siguiente liga de GoogleDocs 'https://drive.google.com/file/d/1cCTt24htDxX25qvn7KculZTsBzxso5f2/view?usp=sharing'

[1] M. Whirl-Carrillo, E.M. McDonagh, J. M. Hebert, L. Gong, K. Sangkuhl, C.F. Thorn, R.B. Altman and T.E. Klein. "Pharmacogenomics Knowledge for Personalized Medicine" Clinical Pharmacology & Therapeutics (2012) 92(4): 414-417.

