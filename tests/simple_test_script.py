from fsps import StellarPopulation


if __name__ == "__main__":
    pop = StellarPopulation(zcontinuous=1)
    print("success")

    pop.params["sfh"] = 4
    pop.params["tau"] = 1.0
    w, s = pop.get_spectrum(tage=12)