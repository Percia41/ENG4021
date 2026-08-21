import soma
import subtrai
import multiplica
import divide


def main():
    numero1 = float(input("Digite o primeiro número: "))
    numero2 = float(input("Digite o segundo número: "))
    operando = input("Digite o operador (+, -, *, /): ")

    if operando == "+":
        resultado = soma.somaf(numero1, numero2)
    elif operando == "-":
        resultado = subtrai.subtraif(numero1, numero2)
    elif operando == "*":
        resultado = multiplica.multiplicaf(numero1, numero2)
    elif operando == "/":
        resultado = divide.dividef(numero1, numero2)
    else:
        print("Operador inválido.")
        return

    print(f"Resultado: {resultado}")


if __name__ == "__main__":
    main()