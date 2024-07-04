### IGENERÍA DE DATOS
En esta sección se encontrarán diferentas carpetas con notebooks de python y scripts correspondientes al área de la ingeniería de datos.

### PROCESAMIENTO DE DATOS
En las carpetas **Google** y **Yelp** se encontrarán los documentos referidos al ETL, todo lo referido a scrapping y apis esta en la carpeta que lleva el mismo nombre. Los scripts utilizados en el servicio de nube de **Google Cloud** lleva la carpeta con el mismo nombre.

### PIPELINE

<img src="/img/pipeline_mejorado.drawio.png" title="Pipeline_mejorado" alt="pipeline_mejorado" width="100" height="300"/>

En este pipeline tenemos:
- Google Cloud storage: que funciona como nuestro Data Lake donde los archivos se almacenan en buckets y en su forma cruda.
- Google Big Query: donde funciona como nuestro Data Warehouse y almacena la información ya procesada en forma de tablas, pero debemos recordar que no es un tipo de base de datos realacional.
- Google Cloud Loggin: quien se encarga de registrar eventos y activar las funciones de google dependiendo de su configuración.
- Google Cloud Functions: que ejecuta los scripts para las extracciones transformaciones y cargas.

### PROCESOS DE LAS FUNCIONES

<img src="/img/funciones.drawio.png" title="Pipeline_mejorado" alt="pipeline_mejorado" />

En términos generales podemos decir que los procesos de las funciones son los siguientes:

1) Extracción del bucket: se extraen los archivos del bucket correspondiente en base al evento que se detectó, en este caso la creación de un objeto dentro del bucket (cuando se sube un archivo).
2) Transformación de la información: se realizan las transformaciones necesarias para las necesidades del proyecto.
3) Almacenamiento de la información en Big Query: se almacena la información para su posterior uso.
4) Eliminación de duplicados entre lotes: se verifican que no haya duplicados en Big Query y si los hay se eliminan.

### PROCESO DE NEGOCIOS Y REVIEWS

<img src="/img/lotes.drawio.png" title="Lotes" alt="lotes" />

En el caso de los negocios y reviews se da algo muy particular, ya que al poder filtrar la información de los negocios por tipo y ubicación no tenemos problema para llenar la tabla correspondiente.

En lo que se refiere a reviews no se puede filtrar a menos que se cruce información con los negocios. Aquí es donde se realiza el cruce de datos y se genera la nueva tabla de análisis de sentimientos.