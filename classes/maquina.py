
class Maquina:
    def __init__(self,pName,pId):
        
        self.name = pName
        self.id = pId
        self.capaRed = self.CapaRed(pName)
        self.capaFisica = self.CapaFisica(pName)
        self.paquetesRed_Enlace = []
        self.condicionToLinkLayer = True
        self.capaFisicaRecibidos = []
        self.pausa = False
        self.pTasaErrores = 0


    def toLinkLayer(self):
        pass

    class CapaRed:
    
        def __init__(self):
            self.paquetes = []
            self.framesRecibidos = []
            self.condicionGenerarPaquetes = True
    

        '''
        Genera paquetes con strings aleatorios
        Los almacena en self.paquetes
        De self.paquetes se enviaran a CapaFisica
        En CapaFisica se convierten en Frames
        En CapaFisica se almacenan en framesEnviar
        '''
        def generarPaquetes(self):
            pass
            

    

            
            

        #Retorna el primer paquete de self.paquetes
        #"envia" paquete a capa enlace
        def enviarPaquete(self):
            pass
            



    class CapaFisica:

        def __init__(self):
            self.framesEnviar = []
            self.framesRecibidos = []
        
        def getFramesEnviar(self):
            return(self.framesEnviar)
                
            
        
    


    
