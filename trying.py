import GetTubeInfo as GTI
DB = GTI.DB
um_index = DB["Comment"].str.extract(r"(UM)", expand=False)
final = DB[um_index.notna()].to_csv("UMTubes.txt")