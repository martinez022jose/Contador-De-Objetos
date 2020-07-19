import cv2
import numpy as np

def enumerar(contorno,mensaje):
    area = cv2.contourArea(contorno)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if area > 100:
        M = cv2.moments(contorno)
        if (M["m00"]==0): 
            M["m00"]=1
        x = int(M["m10"]/M["m00"])
        y = int(M['m01']/M['m00'])
        cv2.putText(imagen,mensaje,(x,y), font, 0.75,(255,255,255),2,cv2.LINE_AA)
    
def iniciarConteo(mascara):
    contornos,_ = cv2.findContours(mascara,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cantidadDeElementos = 1
    for contorno in contornos:
        nuevoContorno = cv2.convexHull(contorno)
        cv2.drawContours(imagen, [nuevoContorno], 0, (255,255,255), 1)
        mensaje = "n" + str(cantidadDeElementos)
        enumerar(contorno,mensaje)
        cantidadDeElementos+=1

        cv2.imshow("Original",imagen)
        cv2.imshow("maskBinario",maskConjunto)
        print("\nPulsa cualquier tecla para enumerar mas objetos\n")
        cv2.waitKey(0)
        
        

imagen= cv2.imread("prueba.png")
imagenHSV = cv2.cvtColor(imagen,cv2.COLOR_BGR2HSV)

#Definimos rango de colores

rojoBajo1 = np.array([0, 50, 20])
rojoAlto1 = np.array([8, 255, 255])
rojoBajo2 = np.array([175, 50, 20])
rojoAlto2 = np.array([180, 255, 255])

azulBajo= np.array([100,50,50])
azulAlto = np.array([135, 255, 255])

verdeBajo = np.array([42,100,20])
verdeAlto = np.array([66,255,255])

amarrilloBajo = np.array([25,100,20])
amarrilloAlto = np.array([35,255,255])

#Generamos mascara binaria

maskAmarrillo = cv2.inRange(imagenHSV,amarrilloBajo,amarrilloAlto)

maskVerde = cv2.inRange(imagenHSV,verdeBajo,verdeAlto)

maskRojo1 = cv2.inRange(imagenHSV, rojoBajo1, rojoAlto1)
maskRojo2 = cv2.inRange(imagenHSV, rojoBajo2, rojoAlto2)

maskRojo =  cv2.add(maskRojo1, maskRojo2)

maskAzul = cv2.inRange(imagenHSV,azulBajo,azulAlto)

maskUnion1 = cv2.add(maskAzul,maskRojo)
maskUnion2 = cv2.add(maskUnion1,maskVerde)
maskConjuntoTotal = cv2.add(maskUnion2,maskAmarrillo)

kernel = np.ones((7,7))
maskConjunto = cv2.morphologyEx(maskConjuntoTotal,cv2.MORPH_OPEN,kernel)
maskConjunto = cv2.morphologyEx(maskConjuntoTotal,cv2.MORPH_CLOSE,kernel)

iniciarConteo(maskConjunto)

cv2.destroyAllWindows()