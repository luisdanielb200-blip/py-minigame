import random


class Personaje:
    def __init__(self, nombre, vida_maxima, defensa):
        self.__nombre = nombre
        self.__vida_maxima = vida_maxima
        self.__vida = vida_maxima
        self.__defensa = defensa

    def get_nombre(self):
        return self.__nombre

    def get_vida(self):
        return self.__vida

    def get_vida_maxima(self):
        return self.__vida_maxima

    def get_defensa(self):
        return self.__defensa

    def get_tipo(self):
        return "Personaje"

    def set_nombre(self, nombre):
        if nombre != "":
            self.__nombre = nombre

    def set_vida(self, valor):
        if valor < 0:
            valor = 0
        elif valor > self.__vida_maxima:
            valor = self.__vida_maxima
        self.__vida = valor

    def esta_vivo(self):
        return self.__vida > 0

    def porcentaje_vida(self):
        return self.__vida * 100 / self.__vida_maxima

    def recibir_dano(self, dano):
        dano_real = dano - self.__defensa
        if dano_real < 1:
            dano_real = 1
        self.set_vida(self.__vida - dano_real)
        print("   " + self.__nombre + " recibe " + str(dano_real) + " de daño")
        return dano_real

    def atacar(self, rival):
        dano = random.randint(5, 10)
        print(self.__nombre + " hace un ataque normal")
        return rival.recibir_dano(dano)

    def habilidad_disponible(self):
        return True

    def habilidad_especial(self, rival):
        print(self.__nombre + " no tiene habilidad especial")
        return self.atacar(rival)

    def mostrar_estado(self):
        print(self.__nombre + " (" + self.get_tipo() + ") - Vida: " + str(self.__vida) + "/" + str(self.__vida_maxima))


class Guerrero(Personaje):
    def __init__(self, nombre):
        super().__init__(nombre, 120, 3)

    def get_tipo(self):
        return "Guerrero"

    def atacar(self, rival):
        dano = random.randint(15, 20)
        print(self.get_nombre() + " golpea con su espada")
        return rival.recibir_dano(dano)

    def habilidad_especial(self, rival):
        print(self.get_nombre() + " usa GOLPE FURIOSO")
        if random.random() < 0.40:
            print("   El golpe furioso fallo")
            return 0
        else:
            dano = random.randint(15, 20) * 2
            return rival.recibir_dano(dano)


class Mago(Personaje):
    def __init__(self, nombre):
        super().__init__(nombre, 80, 0)
        self.__mana = 50

    def get_tipo(self):
        return "Mago"

    def get_mana(self):
        return self.__mana

    def set_mana(self, valor):
        if valor < 0:
            valor = 0
        elif valor > 50:
            valor = 50
        self.__mana = valor

    def atacar(self, rival):
        dano = random.randint(12, 18)
        print(self.get_nombre() + " lanza un rayo magico")
        return rival.recibir_dano(dano)

    def habilidad_disponible(self):
        return self.__mana >= 20

    def habilidad_especial(self, rival):
        if self.habilidad_disponible():
            self.set_mana(self.__mana - 20)
            print(self.get_nombre() + " lanza una BOLA DE FUEGO")
            return rival.recibir_dano(30)
        else:
            print("   No hay mana suficiente, se hace un ataque normal")
            return self.atacar(rival)

    def mostrar_estado(self):
        super().mostrar_estado()
        print("   Mana: " + str(self.__mana) + "/50")


class Arquero(Personaje):
    def __init__(self, nombre):
        super().__init__(nombre, 100, 1)
        self.__prob_esquiva = 0.25

    def get_tipo(self):
        return "Arquero"

    def get_prob_esquiva(self):
        return self.__prob_esquiva

    def atacar(self, rival):
        dano = random.randint(10, 16)
        print(self.get_nombre() + " dispara una flecha")
        return rival.recibir_dano(dano)

    def habilidad_especial(self, rival):
        dano = random.randint(10, 16)
        print(self.get_nombre() + " hace un DISPARO CERTERO")
        if random.random() < 0.30:
            dano = dano * 2
            print("   ¡Golpe critico! " + self.get_tipo() + " hace " + str(dano) + " de daño")
        return rival.recibir_dano(dano)

    def recibir_dano(self, dano):
        if random.random() < self.__prob_esquiva:
            print("   " + self.get_nombre() + " esquivo el golpe")
            return 0
        else:
            return super().recibir_dano(dano)


class Juego:
    def __init__(self):
        self.jugador = None
        self.enemigo = None
        self.turno = 0
        self.jugador_rendido = False
        self.victorias_jugador = 0
        self.victorias_maquina = 0

    def pedir_opcion(self, mensaje, minimo, maximo):
        while True:
            texto = input(mensaje)
            if texto.isdigit() and int(texto) >= minimo and int(texto) <= maximo:
                return int(texto)
            else:
                print("Opcion no valida, escribe un numero del " + str(minimo) + " al " + str(maximo))

    def preguntar_si_no(self, mensaje):
        while True:
            respuesta = input(mensaje).lower()
            if respuesta == "s":
                return True
            elif respuesta == "n":
                return False
            else:
                print("Escribe s o n")

    def crear_personaje(self, opcion, nombre):
        if opcion == 1:
            return Guerrero(nombre)
        elif opcion == 2:
            return Mago(nombre)
        else:
            return Arquero(nombre)

    def elegir_personaje(self):
        nombre = input("Escribe tu nombre: ")
        if nombre == "":
            nombre = "Jugador"
        print("")
        print("Elige tu personaje")
        print("1. Guerrero")
        print("2. Mago")
        print("3. Arquero")
        opcion = self.pedir_opcion("Opcion: ", 1, 3)
        self.jugador = self.crear_personaje(opcion, nombre)
        nombres = ["Morgoth", "Grimbold", "Zarok", "Vexa", "Drakon"]
        opcion_enemigo = random.randint(1, 3)
        self.enemigo = self.crear_personaje(opcion_enemigo, random.choice(nombres))
        print("")
        print("Tu enemigo es " + self.enemigo.get_nombre() + " el " + self.enemigo.get_tipo())

    def mostrar_estados(self):
        print("")
        print("------------------------------")
        lista = [self.jugador, self.enemigo]
        for personaje in lista:
            personaje.mostrar_estado()
        print("------------------------------")

    def turno_jugador(self):
        print("")
        print("Turno " + str(self.turno) + ": te toca")
        print("1. Atacar")
        print("2. Habilidad especial")
        print("3. Rendirse")
        opcion = self.pedir_opcion("Elige una accion: ", 1, 3)
        if opcion == 1:
            self.jugador.atacar(self.enemigo)
        elif opcion == 2:
            self.jugador.habilidad_especial(self.enemigo)
        else:
            self.jugador_rendido = True
            print(self.jugador.get_nombre() + " se rinde")

    def turno_enemigo(self):
        print("")
        print("Turno de " + self.enemigo.get_nombre())
        if self.enemigo.porcentaje_vida() < 30 and self.enemigo.habilidad_disponible():
            self.enemigo.habilidad_especial(self.jugador)
        else:
            self.enemigo.atacar(self.jugador)

    def hay_ganador(self):
        if self.jugador_rendido or not self.jugador.esta_vivo() or not self.enemigo.esta_vivo():
            return True
        else:
            return False

    def anunciar_ganador(self):
        print("")
        if self.jugador_rendido:
            print("Te rendiste, gana " + self.enemigo.get_nombre())
            self.victorias_maquina += 1
        elif not self.jugador.esta_vivo():
            print(self.jugador.get_nombre() + " perdio, gana " + self.enemigo.get_nombre())
            self.victorias_maquina += 1
        else:
            print("¡Ganaste! " + self.jugador.get_nombre() + " derroto a " + self.enemigo.get_nombre())
            self.victorias_jugador += 1

        print("")
        print("------------------------------")
        print("📊 MARCADOR GLOBAL DE PARTIDAS:")
        print("Tus victorias: " + str(self.victorias_jugador))
        print("Victorias de la máquina: " + str(self.victorias_maquina))
        print("------------------------------")

    def jugar_partida(self):
        self.jugador_rendido = False
        self.turno = 0
        self.elegir_personaje()
        self.mostrar_estados()
        while not self.hay_ganador():
            self.turno = self.turno + 1
            self.turno_jugador()
            if not self.hay_ganador():
                self.turno_enemigo()
            self.mostrar_estados()
        self.anunciar_ganador()

    def iniciar(self):
        print("MINI JUEGO DE COMBATE")
        while True:
            print("")
            print("1. Jugar")
            print("2. Salir")
            opcion = self.pedir_opcion("Opcion: ", 1, 2)
            if opcion == 1:
                self.jugar_partida()
                if not self.preguntar_si_no("¿Jugar de nuevo? (s/n): "):
                    break
            else:
                break
        print("Gracias por jugar")


juego = Juego()
juego.iniciar()