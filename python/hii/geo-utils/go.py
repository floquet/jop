from geo_utils.satellite_utils import read_satellite_file, group_satellites, generate_latex

data = read_satellite_file("geo.txt")
grouped = group_satellites(data)
latex_code = generate_latex(grouped)
print(latex_code)
