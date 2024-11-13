push_git() {
	git add .
	git commit -m "$1"
	git push
}

supergit() {
	if [[ $1 == "update" ]]; then
		if [[ -z $2 ]]; then
			echo "Por favor, proporciona un mensaje de commit."
		else
			echo "-------git add ."
			git add .
			echo "-------git commit -m '$2'"
			git commit -m "$2"
			echo "-------git push:"
			git push
		fi
	else
		echo "usage:
		- To update code in repository:
		  supergit update "message"
		  this runs: add ., commit, push"
	fi
}

ros2_pkg(){
    if [ $# -ne 2 ]; then
        echo "Uso: ros2_create_pkg <tipo_de_paquete> <nombre_del_paquete>"
        return 1
    fi
  
    local package_type="$1"
    local package_name="$2"
    
    # Verificar si ROS2 está instalado
    if ! command -v ros2 &> /dev/null; then
        echo "ROS2 no está instalado. Por favor, instala ROS2 primero."
        return 1
    fi

    # Mapear atajos a los tipos de construcción
    case "$package_type" in
        cpp)
        package_type="ament_cmake"
        ;;
        py)
        package_type="ament_python"
        ;;
        *)
        echo "Tipo de paquete no reconocido. Usa 'cpp' para ament_cmake o 'py' para ament_python."
        return 1
        ;;
    esac

    # Crear el paquete usando el comando ros2
    ros2 pkg create --build-type "$package_type" --license Apache-2.0 "$package_name"
    
    echo "Paquete ROS2 '$package_name' creado con el tipo de construcción '$package_type'."
}

cb(){
    local inpack="$1"
    local packname="$2"
    case "$inpack" in
    ps)
        package="--packages-select"
        ;;
    "")
        package=""
        ;;
    *)
        echo "Invalid input"
        return
        ;;
    esac
    colcon build $package $packname
}

alias inst_r='. install/setup.bash'
source /usr/share/gazebo/setup.sh
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=30
export ROS_LOCALHOST_ONLY=0
export TURTLEBOT3_MODEL=waffle