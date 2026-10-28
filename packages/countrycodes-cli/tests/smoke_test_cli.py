import countrycodes_cli


def main() -> None:
    result = countrycodes_cli.__name__
    expected = "countrycodes_cli"
    if result == expected:
        print(f"Smoke test for {countrycodes_cli.__name__}: PASSED")
    else:
        raise RuntimeError(f"Smoke test for {countrycodes_cli.__name__}: FAILED")


if __name__ == "__main__":
    main()
