import math


EPSILON = 1e-9


def les_float(prompt: str, standard: float | None = None) -> float:
    suffix = f" [{standard}]" if standard is not None else ""

    while True:
        verdi = input(f"{prompt}{suffix}: ").strip()
        if not verdi and standard is not None:
            return standard

        try:
            return float(verdi.replace(",", "."))
        except ValueError:
            print("Ugyldig tall, prøv igjen.")


def beregn_ptfs(
    ferie_temp: float,
    hjemme_temp: float,
    alkohol_per_dag: float,
    ferie_lengde: float,
    maks_ferie_lengde: float,
    alfa: float,
    lamda: float,
    dager_siden_hjemkomst: float,
) -> float:
    if maks_ferie_lengde <= 0:
        raise ValueError("Maksimal ferielengde må være større enn 0.")
    if alkohol_per_dag < 0 or ferie_lengde < 0 or dager_siden_hjemkomst < 0:
        raise ValueError("Alkohol, ferielengde og dager siden hjemkomst må være 0 eller mer.")

    justert_hjemme_temp = hjemme_temp if hjemme_temp != 0 else EPSILON
    termisk_sjokk = ((ferie_temp - hjemme_temp) / justert_hjemme_temp) ** 2
    alkoholamplitude = math.log(1 + alkohol_per_dag)
    varighetsforfall = (ferie_lengde / maks_ferie_lengde) ** alfa
    tilfriskningsforfall = math.exp(-lamda * dager_siden_hjemkomst)
    return termisk_sjokk * alkoholamplitude * varighetsforfall * tilfriskningsforfall


def tegn_ascii_graf(verdier: list[float], bredde: int = 40) -> None:
    maksverdi = max(verdier, default=0)

    print("\nASCII-graf for PTFS-utvikling")
    for dag, verdi in enumerate(verdier):
        fyll = 0 if maksverdi == 0 else round((verdi / maksverdi) * bredde)
        print(f"Dag {dag:>2}: {'#' * fyll} {verdi:.3f}")


def tegn_graf(verdier: list[float]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nMatplotlib er ikke installert, viser graf i terminalen i stedet.")
        tegn_ascii_graf(verdier)
        return

    dager = list(range(len(verdier)))
    plt.plot(dager, verdier, marker="o")
    plt.title("Utvikling i PTFS etter hjemkomst")
    plt.xlabel("Dager siden hjemkomst")
    plt.ylabel("PTFS")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def main() -> None:
    print("PTFS-kalkulator for en konkret ferie\n")

    ferie_temp = les_float("Gjennomsnittstemperatur på ferien i °C")
    hjemme_temp = les_float("Gjennomsnittstemperatur hjemme i °C")
    alkohol_per_dag = les_float("Enheter alkohol per dag", 0.0)
    ferie_lengde = les_float("Feriens lengde i dager")
    maks_ferie_lengde = les_float("Lengden der det slutter å føles som ferie", 14.0)
    alfa = les_float("Alfa", 1.5)
    lamda = les_float("Lambda", 0.2)
    antall_dager = int(les_float("Hvor mange dager etter hjemkomst vil du vise", 14.0))

    verdier = [
        beregn_ptfs(
            ferie_temp,
            hjemme_temp,
            alkohol_per_dag,
            ferie_lengde,
            maks_ferie_lengde,
            alfa,
            lamda,
            dag,
        )
        for dag in range(antall_dager + 1)
    ]

    print(f"\nPTFS ved hjemkomst: {verdier[0]:.3f}")
    print(f"PTFS etter {antall_dager} dager: {verdier[-1]:.3f}")
    tegn_graf(verdier)


if __name__ == "__main__":
    main()