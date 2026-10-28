import countrycodes


def main() -> None:
    result = countrycodes.__name__
    expected = "countrycodes"
    if result == expected:
        print(f"Smoke test for {countrycodes.__name__}: PASSED")
    else:
        raise RuntimeError(f"Smoke test for {countrycodes.__name__}: FAILED")


if __name__ == "__main__":
    main()
