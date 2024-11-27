import cv2
import numpy as np

# Constantes
KNOWN_DISTANCE = 20.0  # cm, distancia deseada
MARKER_SIZE = 17.8  # cm, tamaño real del marcador ArUco

# Inicializa el diccionario de ArUco
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
arucoParameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, arucoParameters)

# Calibración de la cámara (valores de ejemplo; reemplaza con los tuyos)
camera_matrix = np.array([[1080, 0, 540],
                          [0, 1080, 360],
                          [0, 0, 1]], dtype=np.float32)
# Ajusta esto si tienes datos reales de distorsión
dist_coeffs = np.zeros((4, 1), dtype=np.float32)

# Función personalizada para estimar pose


def my_estimatePoseSingleMarkers(corners, marker_size, mtx, distortion):
    marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
    trash = []
    rvecs = []
    tvecs = []
    for c in corners:
        nada, R, t = cv2.solvePnP(
            marker_points, c, mtx, distortion, False, cv2.SOLVEPNP_IPPE_SQUARE)
        rvecs.append(R)
        tvecs.append(t)
        trash.append(nada)
    return rvecs, tvecs, trash

# Función para calcular la distancia


def estimate_distance(tvec):
    return np.linalg.norm(tvec)


# Captura de video
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar marcadores ArUco
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        # Dibujar los bordes de los marcadores detectados
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Estimar la pose del marcador
        rvecs, tvecs, trash = my_estimatePoseSingleMarkers(
            corners, MARKER_SIZE, camera_matrix, dist_coeffs)

        for rvec, tvec in zip(rvecs, tvecs):
            # Dibujar el eje del marcador
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, 2)

            # Calcular la distancia
            distance = estimate_distance(tvec)

            distance = 0.685*distance - 2.136

            # Mostrar la distancia en la imagen
            cv2.putText(frame, f"Distance: {distance:.2f} cm", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Verificar si está cerca de 20 cm
            if abs(distance - KNOWN_DISTANCE) <= 2.0:
                print("El marcador está a aproximadamente 20 cm.")

    # Mostrar el video
    cv2.imshow("ArUco Distance Estimation", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
