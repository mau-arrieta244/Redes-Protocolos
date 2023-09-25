
import time
import threading
import classes.maquina as maquina
import classes.frame as frame
from random import random

class SelectiveRepeat(maquina.Maquina):

    def __init__(self, pName, pId):
        super().__init__(pName, pId)
        self.capaRed = self.CapaRed()
        self.capaEnlace = self.CapaEnlace()
        self.pausa = False
        #self.capaFisicaRecibidos = []

    def toLinkLayer(self):
        '''
        Obtiene paquete de capaRed, lo envía a capaEnlace
        '''
        while(True):
            if not self.pausa:
                paquete = self.capaRed.enviarPaquete()
                if paquete:
                    self.capaEnlace.paquetes.append(paquete)
                    #self.capaEnlace.framesEnviar.append(paquete)
                    time.sleep(1)
            else:
                pass

    def startMachine(self,maquinaDestino:maquina.Maquina):
        
        t1 = threading.Thread(target=self.capaRed.generarPaquetes)
        t2 = threading.Thread(target=self.toLinkLayer)
        t3 = threading.Thread(target=self.capaEnlace.crearFrames)
        t4 = threading.Thread(target=lambda:self.capaEnlace.toPhysicalLayer(maquinaDestino,3))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

    def startReceiverMachine(self,maquinaDestino:maquina.Maquina):
        
        t1 = threading.Thread(target=lambda:self.capaEnlace.cicloRecibidos(maquinaDestino,0.5))
        t1.start()
        

    def pauseMachine(self):
        
        self.pausa = True
        self.capaRed.pausa = True
        self.capaEnlace.pausa = True

    def resumeMachine(self):
        
        self.pausa = False
        self.capaRed.pausa = False
        self.capaEnlace.pausa = False
        

    class CapaRed:
    
        def __init__(self):
            self.paquetes = []
            self.framesRecibidos = []
            self.pausa = False
    

        '''
        Genera paquetes con strings aleatorios
        Los almacena en self.paquetes
        De self.paquetes se enviaran a CapaEnlace
        En CapaEnlace se convierten en Frames
        En CapaEnlace se almacenan en framesEnviar
        '''
        def generarPaquetes(self):
            count = 0
            while(True):
                if not self.pausa:
                    string = str(count)+"abcd"
                    self.paquetes.append(string)
                    count+=1
                    time.sleep(1)
                else:
                    pass

        '''
        Retorna ultimo paquete generado en self.paquetes
        Lo utiliza Maquina para enviar a CapaEnlace.framesEnviar
        '''
        def enviarPaquete(self):
            if self.paquetes:
                last = self.paquetes[-1]
                self.paquetes.clear()
                return(last)

    class CapaEnlace:

        def __init__(self):
            self.framesEnviar = []
            self.window = []
            self.paquetes = []
            self.capaFisicaRecibidos = []
            self.pausa = False
        

        def sendItems(maquinaDestino:maquina.Maquina):
            pass


        '''
        Por hacer:
        -Esperar ack o nak para enviar frames de acuerdo con la ventana.
        -
        '''
        def toPhysicalLayer(self,maquinaDestino:maquina.Maquina,windowSize):
            while(True):
                if not self.pausa:
                    #checkear acks o naks que hayan llegado...(missing)
                    #si window size es 2, hasta que lleguen ambos acks o naks libero window

                    #si hay frames listos
                    if self.framesEnviar:

                        print("\n Acknowledgements:\n")
                        for elemento in self.capaFisicaRecibidos:
                            print(str(elemento.sequenceNumber)+" "+elemento.kind)

                        #vamos llenando self.window
                        if (len(self.window)<windowSize):
                            sendingFrame = self.framesEnviar.pop(0)
                            self.window.append(sendingFrame)
                            time.sleep(1)

                        #ventana llena
                        elif (len(self.window)==windowSize):
                            #los envía todos pero no vacía ventana
                            while(self.window):
                                sendingFrame = self.window.pop(0)
                                #print("\n ================== \n")
                                #print("\n Frame %s enviado a maquina B !\n" % (sendingFrame.sequenceNumber))
                                #print("\n ================== \n")
                                maquinaDestino.capaEnlace.capaFisicaRecibidos.append(sendingFrame)
                                time.sleep(1)
                            #  1) acks llegaron? limpiar window 
                            #  2) no han llegado? wait


                        else:
                            print("Condicion rara... revisar")
                            time.sleep(3)
                else:
                    pass
        '''
        Un ciclo que revisa si ha recibido paquetes de capaRed
        Si hay paquetes, los convierte a Frames y agrega a framesEnviar []
        '''
        def crearFrames(self):
            count = 0
            while(True):
                if not self.pausa:
                    if self.paquetes:
                        paquete = self.paquetes[0]
                        newFrame = frame.Frame(count,paquete,'Data')
                        self.framesEnviar.append(newFrame)
                        self.paquetes.clear()
                        #print("\n Frame %d creado en enlace.. \n" % newFrame.sequenceNumber)
                        count+=1
                        time.sleep(1)
                else:
                    pass

        '''
        Un ciclo que revisa si ha recibido frames desde otra maquina
        Si hay frames, los agrega a un buffer
        Del buffer deben convertirse en paquetes y pasar en orden a la capaRed
        '''
        def cicloRecibidos(self,maquinaDestino:maquina.Maquina,porcentaje):
            while(True):
                if not self.pausa:
                    #si hay frames recibidos
                    if self.capaFisicaRecibidos:
                        #frame recibido correctamente
                        if random()<porcentaje:
                            frameRecibido = self.capaFisicaRecibidos.pop(0)
                            print("\n Frame %d recibido por maquina B ! \n" % (frameRecibido.sequenceNumber))
                            ackFrame = frame.Frame(frameRecibido.sequenceNumber,None,'ack')
                            maquinaDestino.capaEnlace.capaFisicaRecibidos.append(ackFrame)
                            time.sleep(1)
                        #lost packets
                        else:
                            frameRecibido = self.capaFisicaRecibidos.pop(0)
                            print("\n Frame %d perdido... \n" % (frameRecibido.sequenceNumber))
                            nakFrame = frame.Frame(frameRecibido.sequenceNumber,None,'nak')
                            maquinaDestino.capaEnlace.capaFisicaRecibidos.append(nakFrame)
                            time.sleep(1)

                else:
                    time.sleep(1)
                    pass
                    
      
