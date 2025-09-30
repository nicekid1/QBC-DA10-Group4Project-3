import os
import warnings
warnings.filterwarnings("ignore")

abs_path = os.path.abspath(os.getcwd())
script_folder = os.path.join(abs_path, 'scripts')
data_folder = os.path.join(abs_path, 'data')

try:
    os.mkdir(data_folder)
    print(f"Directory '{data_folder}' created successfully.")
except FileExistsError:
    print(f"Directory '{data_folder}' already exists.")
except OSError as e:
    print(f"Error creating directory: {e}")

print('########### Getting all players informations ###########')
os.system(f'python3 {os.path.join(script_folder, "player_crawler.py")}')
print()
print('########### Getting MVP players informations ###########')
os.system(f'python3 {os.path.join(script_folder, "mvp_player_crawler.py")}')
print()
print('########### Getting all teams informations ###########')
os.system(f'python3 {os.path.join(script_folder, "team_crawler_ali.py")}')
print()
print('########### Getting top 50 players informations ###########')
os.system(f'python3 {os.path.join(script_folder, "top50_player_ali.py")}')
print()
print('########### Getting champions informations ###########')
os.system(f'python3 {os.path.join(script_folder, "champ_team_crawler.py")}')
print("#"*70)
print('Cleaning data and adding it to the database...')
os.system(f"python3 {os.path.join(script_folder, 'clean_extract.py')}")
print()
print("All done. Enjoy!")