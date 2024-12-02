import glob

import cv2
import numpy as np

# Tamaño del tablero de ajedrez (esquinas internas)
CHECKERBOARD = (6, 4)
square_size = 2.8  # Tamaño de cada casilla en milímetros

# Definir los criterios de refinamiento
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Preparar puntos 3D del tablero
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[1], 0:CHECKERBOARD[0]].T.reshape(-1, 2)
objp *= square_size

objpoints = []  # Puntos 3D en el espacio real
imgpoints = []  # Puntos 2D en el plano de la imagen

# Cargar imágenes del tablero
images = glob.glob('calibration_images/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Mostrar imagen hasta que se presione una tecla
    # cv2.imshow('Imagen', gray)
    # cv2.waitKey(0)

    # Detectar esquinas del tablero
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1), criteria)  # Usar 'criteria'
        imgpoints.append(corners2)

        # Dibujar las esquinas detectadas
        cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        cv2.imshow('Esquinas Detectadas', img)
        cv2.waitKey(0)
    else:
        print(f"Esquinas no detectadas en {fname}")

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


cv2.destroyAllWindows()

# Verificar que se hayan detectado esquinas
if len(objpoints) == 0 or len(imgpoints) == 0:
    print("Error: No se detectaron esquinas en las imágenes.")
else:
    # Calibrar la cámara
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )
    print("Camera Matrix:\n", camera_matrix)
    print("Distortion Coefficients:\n", dist_coeffs)
