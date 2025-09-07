import pandas as pd
from decimal import Decimal
import subprocess
import time
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
from PIL import Image


"""
WRITTEN DURING MY MASTER'S THESIS AT THE EUROPEAN SOUTHERN OBSERVATORY (ESO), GARCHING &
LUDWIG MAXIMILIANS UNIVERSITY, MUNICH.

CONTACT @ AKASH GUPTA, AKASHGUPTA21097@GMAIL.COM

"""





# Read coordinates from CSV file
aprg = pd.read_csv('C:/Users/akash/Downloads/APRG_All-part1/coords.csv')

for i in range(aprg.shape[0]):
    # Format coordinates for filename matching
    radec = f"{aprg['ra'][i]:f}{aprg['dec'][i]:+f}"
    print(f"Processing {i+1}/{aprg.shape[0]}: {radec}")
    
    # GLIMPSE (Spitzer) RGB composite
    ds9_glimpse_cmd = [
        'C:\\SAOImageDS9\\ds9.exe',
        '-rgb',
        '-fits', f"C:/Users/akash/Downloads/APRG_All-part1/{radec}/fc_{radec}_spitzer_seipirac4(2.4)_reproj.fits",
        '-scale', 'ZScale',
        '-rgb', 'channel', 'green',
        '-fits', f"C:/Users/akash/Downloads/APRG_All-part1/{radec}/fc_{radec}_spitzer_seipirac2(2.4)_reproj.fits",
        '-scale', 'ZScale',
        '-rgb', 'channel', 'blue',
        '-fits', f"C:/Users/akash/Downloads/APRG_All-part1/{radec}/fc_{radec}_spitzer_seipirac1(2.4)_reproj.fits",
        '-scale', 'ZScale',
        '-zoom', 'to', 'fit',
        '-colorbar', 'no',
        '-export', f"C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/GLIMPSE/{radec}_glimpse.jpeg", '100'
    ]
    
    ds9 = subprocess.Popen(ds9_glimpse_cmd)
    time.sleep(5.0)
    ds9.terminate()
    
    # WISE RGB composite
    ds9_wise_cmd = [
        'C:\\SAOImageDS9\\ds9.exe',
        '-rgb',
        '-fits', f"C:/Users/akash/Downloads/APRG_All-part1/{radec}/fc_{radec}_wise_4_reproj.fits",
        '-scale', 'ZScale',
        '-rgb', 'channel', 'green',
        '-fits', f"C:/Users/akash/Downloads/APRG_All-part1/{radec}/fc_{radec}_wise_2_reproj.fits",
        '-scale', 'ZScale',
        '-rgb', 'channel', 'blue',
        '-fits', f"C:/Users/akash/Downloads/APRG_All-part1/{radec}/fc_{radec}_wise_1_reproj.fits",
        '-scale', 'ZScale',
        '-zoom', 'to', 'fit',
        '-colorbar', 'no',
        '-export', f"C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/WISE/{radec}_wise.jpeg", '100'
    ]
    
    ds9 = subprocess.Popen(ds9_wise_cmd)
    time.sleep(5.0)
    ds9.terminate()
    
    # 2MASS RGB composite
    ds9_2mass_cmd = [
        'C:\\SAOImageDS9\\ds9.exe',
        '-rgb',
        '-fits', f"C:/Users/akash/Downloads/APRG_All-part1/{radec}/fc_{radec}_2mass_k_reproj.fits",
        '-scale', 'ZScale',
        '-rgb', 'channel', 'green',
        '-fits', f"C:/Users/akash/Downloads/APRG_All-part1/{radec}/fc_{radec}_2mass_h_reproj.fits",
        '-scale', 'ZScale',
        '-rgb', 'channel', 'blue',
        '-fits', f"C:/Users/akash/Downloads/APRG_All-part1/{radec}/fc_{radec}_2mass_j_reproj.fits",
        '-scale', 'ZScale',
        '-zoom', 'to', 'fit',
        '-colorbar', 'no',
        '-export', f"C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/2MASS/{radec}_2mass.jpeg", '100'
    ]
    
    ds9 = subprocess.Popen(ds9_2mass_cmd)
    time.sleep(5.0)
    ds9.terminate()


######## VISUALIZATION (OPTIONAL), comment the following code to skip!!  ######

# Create a grid plot of GLIMPSE images
fig, ax = plt.subplots(4, 5, figsize=(25, 20))

for i in range(min(aprg.shape[0], 20)):  # Limit to 20 images for 4x5 grid
    size = 150 / 3600  # Size in degrees
    ra, dec = aprg['ra'][i], aprg['dec'][i]
    ra, dec = round(Decimal(ra), 6), round(Decimal(dec), 6)
    radec = f"{aprg['ra'][i]:f}{aprg['dec'][i]:+f}"
    
    # Convert to galactic coordinates
    gc = SkyCoord(ra=ra * u.degree, dec=dec * u.degree, frame='fk5', unit='deg')
    l, b = gc.galactic.l.value, gc.galactic.b.value

    # Load and display image
    img_path = f'C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/GLIMPSE/{radec}_glimpse.jpeg'
    try:
        img = Image.open(img_path)
        row, col = divmod(i, 5)
        ax[row, col].imshow(img, extent=[
            l - size * 0.5, l + size * 0.5, 
            b - size * 0.5, b + size * 0.5
        ])
        ax[row, col].set_title(f'APRG {i+1} ({l:.4f}, {b:.4f})', fontsize=15)
        ax[row, col].set_xlabel('Galactic Longitude')
        ax[row, col].set_ylabel('Galactic Latitude')
    except FileNotFoundError:
        print(f"Image not found: {img_path}")

plt.tight_layout()
plt.savefig("C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/GLIMPSE_APRG.pdf", dpi=300)
plt.show()
