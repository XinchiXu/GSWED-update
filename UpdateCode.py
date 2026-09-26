import os, shutil
from openpyxl import load_workbook


def update_new_code(target_year, folder='./2023更新代码', old_year=2023, user='your_username'):
    target_folder, code_paths = f'./{target_year}更新代码', []
    shutil.copytree(folder, target_folder, dirs_exist_ok=True)
    os.remove(f"{target_folder}/BandDate2023.xlsx")
    os.remove(f"{target_folder}/后处理.txt")
    for root, _, files in os.walk(target_folder):
        code_paths.extend([os.path.join(root, f).replace('\\', '/') for f in files if f.endswith(".txt")])
    for code_path in code_paths:
        with open(code_path, 'r', encoding='utf-8') as f:
            code = f.read()
        code = code.replace(f"MOD09Q1Collection.filterDate(\"{old_year}-1-1\", \"{old_year + 1}-1-1\")",
                            f"MOD09Q1Collection.filterDate(\"{target_year}-1-1\", \"{target_year + 1}-1-1\")")
        code = code.replace(f"{old_year}/\').cat(ee.String(ee.Number(lon_start))",
                            f"{target_year}/\').cat(ee.String(ee.Number(lon_start))")
        code = code.replace(f".cat(ee.String(\'_{old_year}_Asset\')).getInfo(),",
                            f".cat(ee.String(\'_{target_year}_Asset\')).getInfo(),")
        code = code.replace(f".cat(ee.String(\'_{old_year}_Asset\'))).getInfo(),",
                            f".cat(ee.String(\'_{target_year}_Asset\'))).getInfo(),")
        with open(code_path, 'w', encoding='utf-8') as f:
            f.write(code)
    os.makedirs(f'{target_folder}/后处理', exist_ok=True)
    continents = ['Africa', 'America', 'Asia', 'Europe', 'Oceania']
    for continent in continents:
        with open(f'{folder}/后处理.txt', 'r', encoding='utf-8') as f:
            code = f.read()
        code = code.replace("var region = table.filter(ee.Filter.eq(\"CONTINENT\",\"Africa\"))",
                            f"var region = table.filter(ee.Filter.eq(\"CONTINENT\",\"{continent}\"))")
        code = code.replace("updatedWaterColAfrica",
                            f"updatedWaterCol{continent}")
        code = code.replace("var list=ee.List([2023])",
                            f"var list=ee.List([{target_year}])")
        code = code.replace("users/qianrswaterr/GSWED_Africa2023_4326v2/",
                            f"users/{user}/GSWED_{continent}{target_year}_4326v2/")
        code = code.replace("folder: \'GSWED_Africa2023_4326v2\',",
                            f"folder: \'GSWED_{continent}{target_year}_4326v2\',")
        with open(f'{target_folder}/后处理/后处理_{continent}.txt', 'w', encoding='utf-8') as f:
            f.write(code)
    wb = load_workbook(f'{folder}/BandDate2023.xlsx')
    for c in wb.active['B'][1:]: c.value = \
        f"{str(c.value).replace(f'{old_year}', f'{target_year}').split()[0].replace('-', '/')}"
    wb.save(f'{target_folder}/BandDate{target_year}.xlsx')


if __name__ == '__main__':
    update_new_code(target_year=2025)
    
