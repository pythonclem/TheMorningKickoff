def getSeasons(starting: str, years: int):
    years_list = list(map(int, starting.split('-')))
    
    if len(years_list) == 1:
        start_year = years_list[0] - years
        print(start_year)
        seasons = [str(year) for year in range(start_year, start_year + years + 1)]
    else:
        start_year, end_year = years_list
        seasons = [f"{year - 1}-{year}" for year in range(end_year, start_year - years, -1)]

    return seasons