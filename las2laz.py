'''
Copyright (C) 2023 GeoTECH Group geotech@uvigo.gal
Copyright (C) 2023 Daniel Lamas Novoa daniel.lamas.novoa@uvigo.gal
This file is part of the program Automated instance and semantic 
segmentation of point clouds of large metallic truss bridges with modelling
purposes.
The program is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) 
any later version.
The program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
more details.
You should have received a copy of the GNU General Public License along 
with the program in COPYING. If not, see <https://www.gnu.org/licenses/>. 
'''

from ui_functions import Uitkinter

ui = Uitkinter()
ui.mainloop()

# Generate executable by running the following command in the console:
# pyinstaller --onefile las2laz.py