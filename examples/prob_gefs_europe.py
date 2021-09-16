##Python script to plot probabilistic storm tracks
#module load /usrx/local/dev/modulefiles/python/3.6.3
#module use /usrx/local/dev/modulefiles

# Anu Simon 06/2020 New
# Anu Simon 06/2020 Add Europe basin

# Anu Simon 02/2021 - Accounted for 30 ensemble members

#######################################
#########################################
from __future__ import print_function

import tkinter as tk
import os
import sys
import glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from math import radians,cos,sin,asin,sqrt
import pandas as pd
from ast import literal_eval
import ast
import datetime
import matplotlib.path as mpath
import matplotlib.ticker as mticker
import matplotlib as mpl

import csv

import cartopy.crs as ccrs
from cartopy.feature import GSHHSFeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature

#############READ DATA#########################

data_dir = ""


file_list = glob.glob(data_dir + 'prob_storm_data_file.dat')
#################################################################
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
def find_nearest(array,value):
    ###Find the nearest grid point distance
    idx=(np.abs(array-value)).argmin()
    return idx



# RE -------------------
#Initialize the empty Plot (only need to call the figure to write the map.)
fig = plt.figure()

#--------------------------
##Reads in the data
for ff in file_list:
    thinfilename    = os.path.basename(ff)
    thinfilenamedir = data_dir

    # RE: This already opens the file and formats it nicely for plotting
    a_data      = pd.read_csv(thinfilename, sep=',',skipinitialspace=True,header=None, usecols=[0,1,2,4,5,6,7,8,9,10,11,12,13,14])
    # RE ------------------------
    # rename the columns
    a_data.columns=['basin', 'stormnum', 'dtg', 'model', 'fhr', 'lat', 'lon', 'kt', 'mslp', 'initial_time', 'valid_fhr', 'valid_day_of_week', 'valid_time','domain']

######################atlantic##################################################

##This fetches the lat/lon postions
    a_data['lat1'] = a_data['lat']
    a_data['lon1'] = a_data['lon']

##This section is needed for drawing blank maps with proper name
    if((a_data.model == "NO").any()):
       a_data['mod_tit'] = "NO"
       a_data['valid_day'] = "NO"
#    elif((a_data.model == "GEFS").any()):
    else:
       a_data['mod_tit'] = "GEFS"
##Converts valid day to upper case
       a_data['valid_day'] = a_data['valid_day_of_week'].any().upper()


##################################################################################
####Sets the proper map prohection topography etc#########################
###Sets area for the selected basin - Atlantic ###########
####Europe####
if((a_data.domain == "europe").any()):
#    ax = plt.axes(projection=ccrs.Stereographic(central_longitude=10.0, central_latitude=40.0, false_easting=0.0, false_northing=0.0, true_scale_latitude=None, globe=None))

#    ax = plt.axes(projection=ccrs.EuroPP())
#    ax.set_extent([-30, 40,20, 70], crs=ccrs.EuroPP())
    ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=10.0, central_latitude=40.0, standard_parallels=(40.0, 40.0)))
    ax.set_extent([-30, 40, 25, 70], crs=ccrs.PlateCarree())

##PLS NOTE THAT THE ax_extent is diff from tick marks and that is by design
    xticks = [-50,-40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60]
    yticks = [20, 30, 40, 50, 60, 70]
    ax.gridlines(xlocs=xticks, ylocs=yticks,color='gray', alpha=0.9, linestyle='--')
###Add topography, lakes, borders etc
    ax.coastlines('10m',linewidth=0.30, color='black')
    ax.add_feature(cfeature.GSHHSFeature('low', levels=[2],
                                         facecolor='white'), color='black', linewidth=0.1)
    land_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m',
                                           edgecolor='face',
                                           facecolor='None')
    ax.add_feature(cfeature.LAKES)
    ax.add_feature(cfeature.BORDERS, linewidth=0.1)
    ax.add_feature(land_10m)
########This part is a roundabout
###for the known issues with
###cartopy LCC/Northpolarstero projection.

    plt.annotate("30N " , (0,0), (-15,73), xycoords='axes fraction', textcoords='offset points', va='top', color='Black', fontsize=6.5)
    plt.annotate("40N " , (0,0), (-15,132), xycoords='axes fraction', textcoords='offset points', va='top', color='Black', fontsize=6.5)
    plt.annotate("50N " , (0,0), (-15,196), xycoords='axes fraction', textcoords='offset points', va='top', color='Black', fontsize=6.5)

    plt.annotate("20W " , (0,0), (32,-5), xycoords='axes fraction', textcoords='offset points', va='top', color='Black', fontsize=6.5)
    plt.annotate("10W " , (0,0), (85,-5), xycoords='axes fraction', textcoords='offset points', va='top', color='Black', fontsize=6.5)
    plt.annotate("0 " , (0,0), (138,-5), xycoords='axes fraction', textcoords='offset points', va='top', color='Black', fontsize=6.5)
    plt.annotate("10E " , (0,0), (190,-5), xycoords='axes fraction', textcoords='offset points', va='top', color='Black', fontsize=6.5)
    plt.annotate("20E " , (0,0), (239,-5), xycoords='axes fraction', textcoords='offset points', va='top', color='Black', fontsize=6.5)
    plt.annotate("30E " , (0,0), (289,-5), xycoords='axes fraction', textcoords='offset points', va='top', color='Black', fontsize=6.5)
######################END OF Europe#################################################

###################################################
####Removing GFS deterministic values for computing probability
####but need it for plotting tracks###################
###Removing GEFS from the computation of prob##############

without_gfs = a_data[ a_data['model'] != "GFSO" ]
data_for_prob  = without_gfs[ without_gfs['model'] != "GEFS" ]



####To count unique members################
###Here the counts are set to 6 or more for GEFS
counts = (data_for_prob.groupby(['stormnum'])['model'].nunique())
filtered = counts[counts >= 6]
new_data = data_for_prob[data_for_prob['stormnum'].isin(filtered.index)]

#####Assigning same data for easiness in grouping#########
track_data = new_data
prob_data = new_data
mean_data = new_data
gfs_data = a_data

#######################################################
####To count unique members################
###Need to do it again for plotting GEFS control
counts = (a_data.groupby(['stormnum'])['model'].nunique())
filtered = counts[counts >= 6]
gefs_data = a_data[a_data['stormnum'].isin(filtered.index)]


#################plot member tracks################################################
##Not plotting tracks for data reasons.
##Keeping it here, so that if need be, this can be put back if there is a last minute user request
#g1 = track_data.groupby([track_data.stormnum, track_data.model])
#for label, track_data in g1:
#    plt.plot(track_data.lon1, track_data.lat1,transform=ccrs.PlateCarree(), color='black', linewidth='0.5')
#########################################################################################################
#######Plot control run track############################
g2 = gefs_data.groupby([gefs_data.stormnum, gefs_data.model])
for label, gefs_data in g2:
    if((gefs_data.model == "GEFS").any()):
      plt.plot(gefs_data.lon1, gefs_data.lat1,transform=ccrs.PlateCarree(), color='black', linewidth='1.5')
###############################################################################################################
############plot GFS deterministic track ###################
##NOT plotting GFS deterministic for now, but leaving it here just in case user needs it later
#g3 = gfs_data.groupby([gfs_data.stormnum, gfs_data.model])
#for label, gfs_data in g3:
#    if((gfs_data.model == "GFSO").any()):
#      plt.plot(gfs_data.lon1, gfs_data.lat1,transform=ccrs.PlateCarree(), color='red', linewidth='1.5')

########################################################################
##########plot probability###############################################

## If there is insufficient data assign 0
## to all grid points
## This is to have same dimension for the images
## The commnets for iines 193 to 197
if len(prob_data.index.values) == 0:
   xnew,ynew=np.mgrid[45:335:291j,20:70:51j]
   nx=np.linspace(45.0,335,291)
   ny=np.linspace(20,70,51)
   perc=np.zeros((291,51))

elif len(prob_data.index.values) > 0:

    g4= prob_data.groupby([prob_data.model])
    thislat=[]
    thislon=[]
    for label, prob_data in g4:
        lat = np.asarray(prob_data.lat)
        lon = np.asarray(prob_data.lon)
        thislat.append(lat)
        thislon.append(lon)
    xnew,ynew=np.mgrid[45:335:291j,20:70:51j]
    nx=np.linspace(45.0,335,291)
    ny=np.linspace(20,70,51)
    prob=np.zeros((len(thislat),291,51))
    print(len(thislat))
    for m in range(len(thislat)):
      for l in range(len(thislat[m][:])):
        xmin=find_nearest(nx,thislon[m][l]-5)
        xmax=find_nearest(nx,thislon[m][l]+5)
        ymax=find_nearest(ny,thislat[m][l]+5)
        ymin=find_nearest(ny,thislat[m][l]-5)
        sublon=nx[xmin:xmax]
        sublat=ny[ymin:ymax]
        for n in range(len(sublon)):
         for o in range(len(sublat)):
           dist=haversine(thislon[m][l]-360,thislat[m][l],sublon[n],sublat[o])
           if dist<150 and prob[m,xmin+n,ymin+o]==0:
             prob[m,xmin+n,ymin+o]=1.0
           else:
                 continue
    perc=(np.sum(prob,axis=0)/float(len(thislat)))*100.
##as on magtest
##Keeping the colors as is with 5% and above if there is a user request.
#colours = ['#FFFFFF', '#008000', '#00FF00', '#ADFF2F', '#1E90FF', '#00CED1', '#FFD700', '#FF8C00', '#B22222', '#FF4500', '#FFA07A']
#clevs=[0,5.,10.,20.,30.,40.,50.,60.,70.,80.,90.]

#colours = ['#ADFF2F', '#1E90FF', '#00CED1', '#FFD700', '#FF8C00', '#B22222', '#FF4500', '#FFA07A']
#clevs=[20.,30.,40.,50.,60.,70.,80.,90.]

colours = ['#FFFFFF', '#008000', '#00FF00','#1E90FF', '#00CED1', '#FFD700','#FF8C00','#FF4500', '#FFA07A']
clevs=[0, 20.,30.,40.,50.,60.,70.,80.,90.]

##########################################################################################
##This section takes care of the title
if((a_data.mod_tit == "GEFS").any()):
   plt.title(f"Probabilistic Storm Tracks from GEFS \n {a_data['initial_time'].iloc[0]}  {a_data['valid_fhr'].iloc[0]}HR  FCST VALID ON {a_data['valid_day'].iloc[0]}  {a_data['valid_time'].iloc[0]}", size=9, x=0.5)
if((a_data.mod_tit == 'NO').any()):
   plt.title(f" ")

#######Plotting the probability keeping it if needed in future
#if len(prob_data.index.values) == 0:
#   ax.annotate('No sufficient data to compute probability',
#               xy=(-0.0000215, 0.018), xytext=(0, 10),
#               xycoords=('axes fraction', 'figure fraction'),
#               textcoords='offset points',
#               size=5.3, ha='center', va='bottom', color='Black')
#if len(prob_data.index.values) > 0:
sc=plt.contourf(xnew, ynew, perc, clevs,
             transform=ccrs.PlateCarree(),colors=colours,extend='max')
cax = fig.add_axes([0.0015,0.1,0.015,0.5])
cbar = fig.colorbar(sc, cax=cax)
cbar.set_ticks([])
##Need this since the cbar is not uniform
ax.annotate('- 20',
               xy=(-0.135, 0.058), xytext=(0, 10),
               xycoords=('axes fraction', 'figure fraction'),
               textcoords='offset points',
               size=9.3, ha='center', va='bottom', color='Black')

ax.annotate('- 30',
               xy=(-0.135, 0.124), xytext=(0, 10),
               xycoords=('axes fraction', 'figure fraction'),
               textcoords='offset points',
               size=9.3, ha='center', va='bottom', color='Black')

ax.annotate('- 40',
               xy=(-0.135, 0.191), xytext=(0, 10),
               xycoords=('axes fraction', 'figure fraction'),
               textcoords='offset points',
               size=9.3, ha='center', va='bottom', color='Black')

ax.annotate('- 50',
               xy=(-0.135, 0.258), xytext=(0, 10),
               xycoords=('axes fraction', 'figure fraction'),
               textcoords='offset points',
               size=9.3, ha='center', va='bottom', color='Black')

ax.annotate('- 60',
               xy=(-0.135, 0.326), xytext=(0, 10),
               xycoords=('axes fraction', 'figure fraction'),
               textcoords='offset points',
               size=9.3, ha='center', va='bottom', color='Black')

ax.annotate('- 70',
               xy=(-0.135, 0.391), xytext=(0, 10),
               xycoords=('axes fraction', 'figure fraction'),
               textcoords='offset points',
               size=9.3, ha='center', va='bottom', color='Black')

ax.annotate('- 80',
               xy=(-0.135, 0.465), xytext=(0, 10),
               xycoords=('axes fraction', 'figure fraction'),
               textcoords='offset points',
               size=9.3, ha='center', va='bottom', color='Black')

ax.annotate('- 90',
               xy=(-0.135, 0.530), xytext=(0, 10),
               xycoords=('axes fraction', 'figure fraction'),
               textcoords='offset points',
               size=9.3, ha='center', va='bottom', color='Black')
###########################################

plt.savefig('prob_storm.png', dpi=160,bbox_inches='tight')
exit
    # ----------------------------
