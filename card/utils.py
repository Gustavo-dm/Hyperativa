import random

def generate_lote_line():
    return "DESAFIO-HYPERATIVA           20180524LOTE0001000010   // [01-29]NOME   [30-37]DATA   [38-45]LOTE   [46-51]QTD DE REGISTROS\n"

def generate_cartao_lines():
    lines = []
    for i in range(1, 101):
        identifier = f"C{i:<4}"  # Adjusted to 4 characters wide for alignment
        card_number = f"{random.randint(1000000000000000, 9999999999999999)}"
        lines.append(f"{identifier} {card_number:<50} // [01-01]IDENTIFICADOR DA LINHA   [02-07]NUMERAÇÃO NO LOTE   [08-26]NÚMERO DE CARTAO COMPLETO\n")
    return lines

def generate_lote_footer():
    return "LOTE0001000010                                        // [01-08]LOTE   [09-14]QTD DE REGISTROS\n"

def main():
    lote_line = generate_lote_line()
    cartao_lines = generate_cartao_lines()
    lote_footer = generate_lote_footer()

    with open("output.txt", "w") as file:
        file.write(lote_line)
        file.writelines(cartao_lines)
        file.write(lote_footer)

if __name__ == "__main__":
    main()
