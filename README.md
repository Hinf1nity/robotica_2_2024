# robotica_2_2024

## Proyecto de Robotica 2 2024

### Librerias necesarias

Para instalar las librerias necesarias para el proyecto, ejecutar el siguiente comando:

```bash
sudo apt install ros-humble-ros2-control ros-humble-ros2-controllers ros-humble-ros2-gazebo-plugins ros-humble-ros2-gazebo-ros-pkgs
sudo apt install ros-humble-slam-toolbox ros-humble-navigation2 ros-humble-nav2-bringup
```

### Ejecucion del proyecto

Ingresar a la carpeta proyecto y ejecutar el siguiente comando:

```bash
cd proyecto_final_ws
colcon build --symlink-install
```

Para ejecutar el proyecto en modo simulacion:

```bash
ros2 launch proyecto launch_sim.launch.py world:=./src/padoru/worlds/obstacles.world
```

Para ejecutar el proyecto en modo real:

```bash
ros2 launch proyecto launch_robot.launch.py
```

Para visualizar el mapa en rviz2:

```bash
rviz2 -d src/padoru/config/padoru_full.rviz
```

Para controlar el robot:

```bash
ros2 run proyecto teleop_twist_keyboard teleop_twist_keyboard
```

### Comandos para realizar slam con slamtoolbox y navegacion con Nav2

Para realizar slam en simulacion:

```bash
ros2 launch padoru online_async_launch.py use_sim_time:=true
```

Para realizar slam en el robot real:

```bash
ros2 launch padoru online_async_launch.py
```

Para realizar navegacion en simulacion:

```bash
ros2 launch padoru navigation_launch.py use_sim_time:=true
```

Para realizar navegacion en el robot real:

```bash
ros2 launch padoru navigation_launch.py
```

### Comandos para realizar localizacion(acml) y navegacion con Nav2 en simulacion

Para realizar esta simulacion se requiere de un archivo del mapa ya creado y guardado en la carpeta proyecto_final_ws
Para realizar localizacion en simulacion:

```bash
ros2 launch padoru localization_launch.py map:=my_map_save.yaml use_sim_time:=true
```

Despues de ejecutar el comando anterior, en rviz2 se debe seleccionar la pose incial estimada en 2D del robot.
Para realizar navegacion en simulacion:

```bash
ros2 launch padoru navigation_launch.py use_sim_time:=true map_subscribee_tansient_local:=true
```

Si se desea realizar los comandos con un robot real solo cambie use_sim_tme:=true por use_sim_time:=false o elimine esta parte del comando.
