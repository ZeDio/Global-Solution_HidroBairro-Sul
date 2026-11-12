from rag.pipeline import responder_com_rag

def interagir_com_hidrobairro():
    print("\n" + "=" * 55)
    print("       HIDROBAIRRO SUL — ASSISTENTE IA")
    print("=" * 55)

    print(
        "\nOlá! Sou o assistente virtual do HidroBairro Sul."
    )

    print(
        "Estou aqui para ajudar com informações sobre "
        "prevenção de alagamentos."
    )

    print("\nDigite 'sair' para encerrar.\n")

    while True:
        pergunta = input("\nVocê: ").strip()

        if pergunta.lower() in {
            "sair",
            "encerrar",
            "parar",
        }:
            print(
                "\nHidroBairro Sul: Até mais! "
                "Cuide-se e fique atento aos alertas oficiais."
            )
            break

        if not pergunta:
            continue

        try:
            resposta, fontes = responder_com_rag(
                pergunta,
                k=3,
            )

            print("\n" + "-" * 55)
            print("HIDROBAIRRO SUL:")
            print("-" * 55)

            print(resposta)

            if fontes:
                print("\nFontes consultadas:")

                for fonte in fontes:
                    print(
                        f"- {fonte['fonte']} "
                        f"(similaridade: "
                        f"{fonte['similaridade']:.4f})"
                    )

            print("-" * 55)

        except Exception as erro:
            print(
                f"\nNão foi possível responder à pergunta."
            )

            print(
                f"Detalhes técnicos: "
                f"{type(erro).__name__}: {erro}"
            )

if __name__ == "__main__":
    interagir_com_hidrobairro()